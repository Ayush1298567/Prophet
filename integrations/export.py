"""Export validated Prophet evidence into safe integration handoff artifacts.

The exporter deliberately emits review templates, not production push actions.
It does not call SIEM, ticketing, or customer APIs. It writes sanitized JSON or
NDJSON files that a customer operator can review and adapt inside their own
systems.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
for rel_path in ("cyber-side", "world-side"):
    module_path = str(REPO_ROOT / rel_path)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

try:
    from evidence.bundle import (  # type: ignore
        EvidenceBundleError,
        load_json,
        load_policy,
        validate_evidence_bundle,
    )
except ImportError as exc:  # pragma: no cover - environment issue
    raise RuntimeError(
        "integrations.export requires PYTHONPATH=.:cyber-side:world-side"
    ) from exc


SCHEMA_VERSION = "prophet_integration_export.v0.1"
NO_LIVE_TARGET_DATA_ASSERTION = (
    "No live target data is included in this export; customer-owned telemetry "
    "placeholders must be filled by the customer."
)

OUTPUT_FILES = {
    "manifest": "manifest.json",
    "splunk_saved_search": "siem/splunk_saved_search.json",
    "elastic_detection_rule": "siem/elastic_detection_rule.ndjson",
    "sentinel_analytic_rule": "siem/sentinel_analytic_rule.json",
    "jira_ticket": "tickets/jira_remediation_ticket.json",
    "servicenow_task": "tickets/servicenow_remediation_task.json",
    "operator_audit_event": "audit/operator_approval_event.json",
}

INTEGRATION_EXPORT_KEYS = tuple(key for key in OUTPUT_FILES if key != "manifest")

BANNED_EXPORT_KEYS = {
    "payload",
    "payloads",
    "procedure",
    "procedures",
    "steps",
    "exploit_steps",
    "command",
    "commands",
    "shell",
    "target_host",
    "hostname",
    "ip",
    "ip_address",
    "credential",
    "credentials",
    "username",
    "password",
    "raw_text",
    "raw_scraper_text",
}

PROCEDURAL_PHRASES = (
    "curl ",
    "powershell ",
    "bash ",
    "ssh ",
    "run the following",
    "execute the following",
    "send the request",
    "paste this",
)

PAYLOAD_TOKENS = (
    "${jndi:",
    "${${",
    "ldap://",
    "rmi://",
    "dns://",
    "runtime.getruntime",
    "cmd.exe",
    "marshalsec",
    "ysoserial",
    "mimikatz",
)

IP_RE = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}"
    r"(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b"
)
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
HOSTNAME_RE = re.compile(
    r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    r"(?:com|net|org|mil|gov|edu|io|dev|local|lan|internal|corp)\b",
    re.IGNORECASE,
)


class IntegrationExportError(ValueError):
    """Raised when an integration export violates the safe handoff contract."""


def build_integration_export(
    bundle: dict[str, Any],
    *,
    generated_at: str | None = None,
    export_id: str | None = None,
    policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a safe SIEM/ticketing handoff package from validated evidence."""

    validate_evidence_bundle(bundle)
    if policy is not None:
        enforce_integration_policy(policy, export_keys=INTEGRATION_EXPORT_KEYS)
    emitted_at = _ensure_generated_at(generated_at)
    evidence_refs = _evidence_refs(bundle)
    summary = _handoff_summary(bundle)

    seed = export_id or f"{bundle['bundle_id']}:{bundle['bundle_sha256']}:{emitted_at}"
    resolved_export_id = export_id or f"pie-{_sha256_text(seed)[:16]}"
    export: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "export_id": resolved_export_id,
        "generated_at": emitted_at,
        "mode": "review_template_only",
        "evidence_refs": evidence_refs,
        "summary": summary,
        "files": dict(OUTPUT_FILES),
        "policy_restrictions": _policy_restrictions(policy),
        "siem": {
            "splunk_saved_search": _splunk_saved_search(bundle, resolved_export_id),
            "elastic_detection_rule": _elastic_detection_rule(bundle, resolved_export_id),
            "sentinel_analytic_rule": _sentinel_analytic_rule(bundle, resolved_export_id),
        },
        "tickets": {
            "jira_ticket": _jira_ticket(bundle, resolved_export_id),
            "servicenow_task": _servicenow_task(bundle, resolved_export_id),
        },
        "operator_audit_event": _operator_audit_event(bundle, resolved_export_id, emitted_at),
        "safety_attestation": {
            "review_templates_only": True,
            "no_external_api_calls": True,
            "no_live_targets": True,
            "no_live_target_data_included": True,
            "no_payloads": True,
            "no_credentials": True,
            "no_private_hostnames": True,
            "customer_placeholders_required": True,
            "data_boundary_statement": NO_LIVE_TARGET_DATA_ASSERTION,
        },
        "hashes": {},
    }

    export["hashes"] = _artifact_hashes(export)
    export["hashes"]["export_body_sha256"] = _export_body_sha256(export)
    validate_integration_export(export)
    return export


def validate_integration_export(export: dict[str, Any] | str) -> None:
    """Validate shape, safety, and hashes for an integration handoff export."""

    value = json.loads(export) if isinstance(export, str) else export
    if not isinstance(value, dict):
        raise IntegrationExportError("integration export must be an object")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise IntegrationExportError(f"schema_version must be {SCHEMA_VERSION}")
    for key in (
        "export_id",
        "generated_at",
        "mode",
        "evidence_refs",
        "summary",
        "files",
        "policy_restrictions",
        "siem",
        "tickets",
        "operator_audit_event",
        "safety_attestation",
        "hashes",
    ):
        if key not in value:
            raise IntegrationExportError(f"integration export missing {key}")
    if value["mode"] != "review_template_only":
        raise IntegrationExportError("integration export mode must be review_template_only")
    _validate_iso(_required_str(value, "generated_at", "export"), "generated_at")
    _scan_export_safety(value, "export")

    refs = _required_object(value, "evidence_refs", "export")
    for key in ("bundle_id", "bundle_sha256", "forecast_id", "artifact_id"):
        _required_str(refs, key, "evidence_refs")
    if not _is_sha256(refs["bundle_sha256"]):
        raise IntegrationExportError("evidence_refs.bundle_sha256 must be SHA-256")
    policy_sha = refs.get("policy_sha256")
    if policy_sha is not None and not _is_sha256(_str(policy_sha, "")):
        raise IntegrationExportError("evidence_refs.policy_sha256 must be SHA-256")
    approval_record_hash = refs.get("approval_record_hash")
    if approval_record_hash is not None and not _is_sha256(_str(approval_record_hash, "")):
        raise IntegrationExportError("evidence_refs.approval_record_hash must be SHA-256")

    restrictions = _required_object(value, "policy_restrictions", "export")
    if restrictions.get("enforced") is not True and restrictions.get("enforced") is not False:
        raise IntegrationExportError("policy_restrictions.enforced must be boolean")
    allowed_exports = restrictions.get("allowed_integration_exports")
    if not isinstance(allowed_exports, list) or not all(
        isinstance(item, str) and item.strip() for item in allowed_exports
    ):
        raise IntegrationExportError("policy_restrictions.allowed_integration_exports must be list[str]")

    safety = _required_object(value, "safety_attestation", "export")
    for flag in (
        "review_templates_only",
        "no_external_api_calls",
        "no_live_targets",
        "no_live_target_data_included",
        "no_payloads",
        "no_credentials",
        "no_private_hostnames",
        "customer_placeholders_required",
    ):
        if safety.get(flag) is not True:
            raise IntegrationExportError(f"safety_attestation.{flag} must be true")
    if not _str(safety.get("data_boundary_statement"), ""):
        raise IntegrationExportError("safety_attestation.data_boundary_statement must be non-empty")

    hashes = _required_object(value, "hashes", "export")
    expected_hashes = _artifact_hashes(value)
    for key, expected in expected_hashes.items():
        if hashes.get(key) != expected:
            raise IntegrationExportError(f"hashes.{key} does not match artifact body")
    expected_export_hash = _export_body_sha256(value)
    if hashes.get("export_body_sha256") != expected_export_hash:
        raise IntegrationExportError("hashes.export_body_sha256 does not match export body")


def write_integration_export(export: dict[str, Any], out_dir: str | Path) -> dict[str, str]:
    """Write export files and return relative path to SHA-256 mapping."""

    validate_integration_export(export)
    root = Path(out_dir)
    files = export["files"]
    payloads: dict[str, str] = {
        files["manifest"]: _pretty_json(export) + "\n",
        files["splunk_saved_search"]: _pretty_json(export["siem"]["splunk_saved_search"]) + "\n",
        files["elastic_detection_rule"]: _compact_json(export["siem"]["elastic_detection_rule"]) + "\n",
        files["sentinel_analytic_rule"]: _pretty_json(export["siem"]["sentinel_analytic_rule"]) + "\n",
        files["jira_ticket"]: _pretty_json(export["tickets"]["jira_ticket"]) + "\n",
        files["servicenow_task"]: _pretty_json(export["tickets"]["servicenow_task"]) + "\n",
        files["operator_audit_event"]: _pretty_json(export["operator_audit_event"]) + "\n",
    }
    written: dict[str, str] = {}
    for rel_path, payload in payloads.items():
        path = root / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
        written[rel_path] = _sha256_text(payload)
    return dict(sorted(written.items()))


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        bundle = load_json(args.bundle)
        export = build_integration_export(
            bundle,
            generated_at=args.generated_at,
            export_id=args.export_id,
            policy=load_policy(args.policy) if args.policy else None,
        )
        if args.out_dir:
            written = write_integration_export(export, args.out_dir)
            print(_pretty_json({"ok": True, "out_dir": str(args.out_dir), "files": written}))
        else:
            print(_pretty_json(export))
        return 0
    except (OSError, json.JSONDecodeError, ValueError, EvidenceBundleError) as exc:
        print(f"integrations.export: {_safe_error(exc)}", file=sys.stderr)
        return 1


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python3 -m integrations.export",
        description="Export validated Prophet evidence into safe SIEM/ticket handoff files.",
    )
    parser.add_argument("--bundle", required=True, type=Path, help="Prophet evidence bundle JSON")
    parser.add_argument("--out-dir", type=Path, help="Directory for generated handoff files")
    parser.add_argument("--generated-at", help="ISO 8601 timestamp for deterministic output")
    parser.add_argument("--export-id", help="Explicit integration export id")
    parser.add_argument("--policy", type=Path, help="Optional prophet_pilot_policy.v0.1 gate")
    return parser


def enforce_integration_policy(policy: dict[str, Any], *, export_keys: tuple[str, ...]) -> None:
    allowed = _string_list(policy.get("allowed_integration_exports"))
    if not allowed:
        raise IntegrationExportError(
            "policy.allowed_integration_exports is required for integration export"
        )
    unknown = sorted(set(allowed) - set(INTEGRATION_EXPORT_KEYS))
    if unknown:
        raise IntegrationExportError(
            f"policy.allowed_integration_exports has unknown values: {', '.join(unknown)}"
        )
    blocked = sorted(key for key in export_keys if key not in allowed)
    if blocked:
        raise IntegrationExportError(
            f"policy does not allow integration exports: {', '.join(blocked)}"
        )


def _policy_restrictions(policy: dict[str, Any] | None) -> dict[str, Any]:
    if policy is None:
        return {
            "enforced": False,
            "allowed_integration_exports": list(INTEGRATION_EXPORT_KEYS),
        }
    return {
        "enforced": True,
        "policy_id": _str(policy.get("policy_id"), "unknown-policy"),
        "allowed_integration_exports": _string_list(policy.get("allowed_integration_exports")),
    }


def _evidence_refs(bundle: dict[str, Any]) -> dict[str, Any]:
    input_refs = _object(bundle.get("input_refs"))
    policy = _object(bundle.get("policy"))
    approval = _object(bundle.get("operator_approval"))
    refs = {
        "bundle_id": _str(bundle.get("bundle_id"), "unknown-bundle"),
        "bundle_sha256": _str(bundle.get("bundle_sha256"), ""),
        "forecast_id": _str(input_refs.get("forecast_id"), "unknown-forecast"),
        "artifact_id": _str(input_refs.get("artifact_id"), "unknown-artifact"),
        "portfolio_id": _str(input_refs.get("portfolio_id"), "unknown-portfolio"),
        "run_id": _str(input_refs.get("run_id"), "unknown-run"),
    }
    if policy:
        refs["policy_id"] = _str(policy.get("policy_id"), "unknown-policy")
        refs["policy_sha256"] = _str(policy.get("policy_sha256"), "")
    approval_event_id = _str(approval.get("approval_event_id"), "")
    approval_record_hash = _str(approval.get("approval_record_hash"), "")
    if approval_event_id:
        refs["approval_event_id"] = approval_event_id
    if approval_record_hash:
        refs["approval_record_hash"] = approval_record_hash
    return refs


def _handoff_summary(bundle: dict[str, Any]) -> dict[str, Any]:
    forecast = _object(bundle.get("forecast_summary"))
    vector = _object(forecast.get("vector"))
    window = _object(forecast.get("strike_window"))
    prediction = _object(bundle.get("prediction_summary"))
    defense = _object(bundle.get("defense_summary"))
    validation = _object(bundle.get("validation_summary"))
    asset_seed = _object(bundle.get("asset_seed_summary"))
    return {
        "title": _safe_text(
            f"Prophet defense handoff for {_str(vector.get('vector_class'), 'priority exposure class')}"
        ),
        "strike_window": {
            "start_date": _str(window.get("start_date"), "unknown"),
            "end_date": _str(window.get("end_date"), "unknown"),
            "confidence": _str(window.get("confidence"), "unknown"),
        },
        "vector_class": _safe_text(_str(vector.get("vector_class"), "unknown")),
        "target_scope": _safe_text(
            _str(_object(forecast.get("strategic_frame")).get("target_scope"), "sector-level")
        ),
        "top_zero_day_class": _safe_text(
            _str(prediction.get("top_zero_day_class"), "unknown zero-day class")
        ),
        "top_one_day_class": _safe_text(
            _str(prediction.get("top_one_day_class"), "unknown one-day class")
        ),
        "patch_summary": _safe_text(_str(defense.get("patch_summary"), "Review defense guidance.")),
        "detection_title": _safe_text(
            _str(_object(defense.get("sigma")).get("title"), "Prophet detection review")
        ),
        "validation_status": _str(validation.get("post_patch_status"), "unknown"),
        "owner_queues": _safe_list(asset_seed.get("owner_queues")),
    }


def _splunk_saved_search(bundle: dict[str, Any], export_id: str) -> dict[str, Any]:
    summary = _handoff_summary(bundle)
    return {
        "schema_version": "prophet.splunk_handoff.v0.1",
        "name": f"{export_id}_prophet_priority_exposure_watch",
        "type": "splunk_saved_search_review_template",
        "description": _safe_text(
            f"Review template for {summary['vector_class']} during the Prophet strike window."
        ),
        "customer_placeholders": [
            "<customer_security_index>",
            "<edge_or_identity_logs>",
            "<approved_owner_queue>",
        ],
        "search": (
            "index=<customer_security_index> sourcetype=<edge_or_identity_logs> "
            "earliest=-24h | stats count by user, action, result | where count >= 1"
        ),
        "schedule_hint": "Customer-defined; align with the evidence strike window.",
        "review_notes": [
            "Replace placeholders inside the customer SIEM.",
            "Tune fields and thresholds against customer-owned telemetry.",
            "Keep the Prophet evidence bundle hash attached to the change record.",
        ],
    }


def _elastic_detection_rule(bundle: dict[str, Any], export_id: str) -> dict[str, Any]:
    summary = _handoff_summary(bundle)
    return {
        "schema_version": "prophet.elastic_handoff.v0.1",
        "rule_id": f"{export_id}-elastic-priority-exposure-watch",
        "type": "query",
        "name": _safe_text(f"Prophet priority exposure watch: {summary['vector_class']}"),
        "description": _safe_text(
            "Review template for customer-owned Elastic data views. It is not a deployed rule."
        ),
        "severity": _severity_from_confidence(summary["strike_window"]["confidence"]),
        "risk_score": _risk_score(summary["strike_window"]["confidence"]),
        "index": ["<customer-security-data-view>"],
        "query": (
            "event.dataset:(authentication or vpn or network) "
            "and event.outcome:(failure or success)"
        ),
        "tags": [
            "prophet",
            "review-template",
            "defensive-prioritization",
        ],
        "required_customer_actions": [
            "Replace the data view placeholder.",
            "Map customer field names before deployment.",
            "Attach evidence and policy hashes to the approval record.",
        ],
    }


def _sentinel_analytic_rule(bundle: dict[str, Any], export_id: str) -> dict[str, Any]:
    summary = _handoff_summary(bundle)
    return {
        "schema_version": "prophet.sentinel_handoff.v0.1",
        "id": f"{export_id}-sentinel-priority-exposure-watch",
        "kind": "Scheduled",
        "displayName": _safe_text(f"Prophet priority exposure watch: {summary['vector_class']}"),
        "description": _safe_text(
            "Review template for Microsoft Sentinel. Customer must map tables and fields."
        ),
        "severity": _sentinel_severity(summary["strike_window"]["confidence"]),
        "enabled": False,
        "query": (
            "<CustomerSecurityTable> | summarize EventCount=count() "
            "by Activity, Account, Computer | where EventCount >= 1"
        ),
        "queryFrequency": "PT1H",
        "queryPeriod": "P1D",
        "triggerOperator": "GreaterThan",
        "triggerThreshold": 0,
        "tactics": ["InitialAccess", "DefenseEvasion"],
        "requiredCustomerActions": [
            "Replace table placeholder.",
            "Tune threshold and entity mapping.",
            "Route through the customer change approval process.",
        ],
    }


def _jira_ticket(bundle: dict[str, Any], export_id: str) -> dict[str, Any]:
    summary = _handoff_summary(bundle)
    return {
        "schema_version": "prophet.jira_handoff.v0.1",
        "type": "jira_issue_review_template",
        "projectKey": "<CUSTOMER_PROJECT>",
        "issueType": "Task",
        "summary": _safe_text(f"Review Prophet defense package: {summary['vector_class']}"),
        "description": _ticket_description(bundle, summary),
        "priority": _ticket_priority(summary["strike_window"]["confidence"]),
        "labels": [
            "prophet",
            "defensive-prioritization",
            "review-template",
        ],
        "assigneeHint": _first(summary["owner_queues"], "<customer-owner-queue>"),
        "evidence": _evidence_refs(bundle),
        "acceptanceCriteria": [
            "Evidence bundle reviewed by authorized operator.",
            "Detection template mapped to customer telemetry or explicitly rejected.",
            "Remediation owner records decision and residual risk.",
        ],
        "export_id": export_id,
    }


def _servicenow_task(bundle: dict[str, Any], export_id: str) -> dict[str, Any]:
    summary = _handoff_summary(bundle)
    return {
        "schema_version": "prophet.servicenow_handoff.v0.1",
        "type": "servicenow_remediation_task_review_template",
        "table": "sn_si_task",
        "short_description": _safe_text(f"Review Prophet defense package: {summary['vector_class']}"),
        "description": _ticket_description(bundle, summary),
        "priority": _servicenow_priority(summary["strike_window"]["confidence"]),
        "assignment_group": _first(summary["owner_queues"], "<customer-assignment-group>"),
        "state": "draft_review",
        "evidence": _evidence_refs(bundle),
        "work_notes": [
            "Generated from validated Prophet evidence.",
            "Customer operator must map telemetry and approve deployment separately.",
            "No live target details or credentials are included.",
        ],
        "export_id": export_id,
    }


def _operator_audit_event(
    bundle: dict[str, Any],
    export_id: str,
    generated_at: str,
) -> dict[str, Any]:
    approval = _object(bundle.get("operator_approval"))
    approval_record_hash = _str(approval.get("approval_record_hash"), "")
    return {
        "schema_version": "prophet.operator_audit_event.v0.1",
        "event_type": "integration_handoff_exported",
        "generated_at": generated_at,
        "export_id": export_id,
        "bundle_id": _str(bundle.get("bundle_id"), "unknown-bundle"),
        "bundle_sha256": _str(bundle.get("bundle_sha256"), ""),
        "approval_decision": _str(approval.get("decision"), "unknown"),
        "approval_mode": _str(approval.get("approval_mode"), "unknown"),
        "operator_label": _str(approval.get("operator_label"), "unknown"),
        "approval_event_id": _str(approval.get("approval_event_id"), "unknown-approval-event"),
        "approval_record_hash": approval_record_hash,
        "policy": {
            "policy_id": _str(_object(bundle.get("policy")).get("policy_id"), "unknown-policy"),
            "policy_sha256": _str(_object(bundle.get("policy")).get("policy_sha256"), ""),
        },
        "attestation": "Generated safe review templates only; no external systems were called.",
    }


def _ticket_description(bundle: dict[str, Any], summary: dict[str, Any]) -> str:
    refs = _evidence_refs(bundle)
    window = summary["strike_window"]
    return _safe_text(
        "Prophet generated a defensive evidence package for "
        f"{summary['vector_class']} covering {window['start_date']} to {window['end_date']} "
        f"with {window['confidence']} confidence. Validation status: "
        f"{summary['validation_status']}. Patch summary: {summary['patch_summary']}. "
        f"Evidence bundle: {refs['bundle_id']} / {refs['bundle_sha256']}. "
        "Review templates require customer telemetry mapping before deployment."
    )


def _artifact_hashes(export: dict[str, Any]) -> dict[str, str]:
    return {
        "splunk_saved_search_sha256": _sha256_normalized(
            _object(_object(export.get("siem")).get("splunk_saved_search"))
        ),
        "elastic_detection_rule_sha256": _sha256_normalized(
            _object(_object(export.get("siem")).get("elastic_detection_rule"))
        ),
        "sentinel_analytic_rule_sha256": _sha256_normalized(
            _object(_object(export.get("siem")).get("sentinel_analytic_rule"))
        ),
        "jira_ticket_sha256": _sha256_normalized(
            _object(_object(export.get("tickets")).get("jira_ticket"))
        ),
        "servicenow_task_sha256": _sha256_normalized(
            _object(_object(export.get("tickets")).get("servicenow_task"))
        ),
        "operator_audit_event_sha256": _sha256_normalized(
            _object(export.get("operator_audit_event"))
        ),
    }


def _scan_export_safety(value: Any, path: str) -> None:
    if isinstance(value, dict):
        for key, inner in value.items():
            lowered = str(key).lower()
            if lowered in BANNED_EXPORT_KEYS:
                raise IntegrationExportError(f"{path} contains banned key: {key}")
            _scan_export_safety(inner, f"{path}.{key}")
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            _scan_export_safety(item, f"{path}[{idx}]")
    elif isinstance(value, str):
        lowered = value.lower()
        for phrase in PROCEDURAL_PHRASES:
            if phrase in lowered:
                raise IntegrationExportError(f"{path} contains procedural phrase: {phrase!r}")
        for token in PAYLOAD_TOKENS:
            if token in lowered:
                raise IntegrationExportError(f"{path} contains payload-like token: {token!r}")
        if IP_RE.search(value):
            raise IntegrationExportError(f"{path} contains IP-like text")
        if EMAIL_RE.search(value):
            raise IntegrationExportError(f"{path} contains email-like text")
        if HOSTNAME_RE.search(value):
            raise IntegrationExportError(f"{path} contains hostname-like text")


def _safe_text(value: str) -> str:
    out = re.sub(r"\s+", " ", str(value or "")).strip()
    out = IP_RE.sub("[IP-REDACTED]", out)
    out = EMAIL_RE.sub("[EMAIL-REDACTED]", out)
    out = HOSTNAME_RE.sub("[HOSTNAME-REDACTED]", out)
    for token in PAYLOAD_TOKENS:
        out = re.sub(re.escape(token), "[REDACTED-TOKEN]", out, flags=re.IGNORECASE)
    return out[:1200]


def _safe_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    out: list[str] = []
    for item in value:
        if not isinstance(item, str):
            continue
        clean = _safe_text(item)
        if clean and clean not in out:
            out.append(clean)
    return out


def _severity_from_confidence(confidence: str) -> str:
    return {"high": "high", "medium": "medium", "low": "low"}.get(confidence, "low")


def _sentinel_severity(confidence: str) -> str:
    return {"high": "High", "medium": "Medium", "low": "Low"}.get(confidence, "Low")


def _risk_score(confidence: str) -> int:
    return {"high": 73, "medium": 47, "low": 21}.get(confidence, 21)


def _ticket_priority(confidence: str) -> str:
    return {"high": "High", "medium": "Medium", "low": "Low"}.get(confidence, "Low")


def _servicenow_priority(confidence: str) -> str:
    return {"high": "2", "medium": "3", "low": "4"}.get(confidence, "4")


def _export_body_sha256(export: dict[str, Any]) -> str:
    body = copy.deepcopy(export)
    if isinstance(body.get("hashes"), dict):
        body["hashes"].pop("export_body_sha256", None)
    return _sha256_normalized(body)


def _sha256_normalized(value: Any) -> str:
    return _sha256_text(_canonical_json(value))


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _pretty_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def _compact_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _ensure_generated_at(value: str | None) -> str:
    if value:
        _validate_iso(value, "generated_at")
        return value
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_iso(value: str, path: str) -> None:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise IntegrationExportError(f"{path} must be ISO 8601") from exc


def _required_object(value: dict[str, Any], key: str, path: str) -> dict[str, Any]:
    item = value.get(key)
    if not isinstance(item, dict):
        raise IntegrationExportError(f"{path}.{key} must be object")
    return item


def _required_str(value: dict[str, Any], key: str, path: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item.strip():
        raise IntegrationExportError(f"{path}.{key} must be non-empty string")
    return item.strip()


def _object(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _str(value: Any, default: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return default


def _string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item.strip() for item in value if isinstance(item, str) and item.strip()]


def _first(values: Any, default: str) -> str:
    if isinstance(values, list):
        for value in values:
            if isinstance(value, str) and value.strip():
                return value.strip()
    return default


def _is_sha256(value: str) -> bool:
    return bool(re.fullmatch(r"[0-9a-f]{64}", value))


def _safe_error(exc: BaseException) -> str:
    return _safe_text(str(exc)).replace("\n", " ")[:800]


if __name__ == "__main__":
    raise SystemExit(main())
