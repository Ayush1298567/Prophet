#!/usr/bin/env python3
"""Write compact contact-form copy for verified Prophet outreach drafts."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


CONTACT_FORM_COPY_SCHEMA_VERSION = "prophet_validation_contact_form_copy.v0.1"
DEFAULT_MESSAGE_PACK = Path("validation/private/today-message-pack.json")
DEFAULT_TARGETS = Path("validation/private/validation-targets.json")
DEFAULT_MAX_CHARS = 650


class ContactFormCopyError(ValueError):
    """Raised when compact contact-form copy cannot be written safely."""


def write_contact_form_copy(
    pack: dict[str, Any],
    targets_value: dict[str, Any],
    *,
    out_dir: Path,
    require_date: str | None = None,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> dict[str, Any]:
    if require_date is not None:
        _validate_date(require_date)
    _validate_max_chars(max_chars)
    status_module = _load_module("validation-outreach-status.py", "validation_outreach_status")
    message_module = _load_module("validation-message-pack.py", "validation_message_pack")
    status = status_module.build_status(
        pack,
        targets_value,
        verify_dry_run_commands=True,
        require_date=require_date,
    )
    if status["counts"]["needs_attention"]:
        labels = [
            item["target_label"]
            for item in status["items"]
            if item["state"] == "needs_attention"
        ]
        raise ContactFormCopyError(
            "outreach pack needs attention before contact-form copy can be written: "
            + ", ".join(labels)
        )
    pending = [
        item
        for item in status["items"]
        if item["state"] == "pending_send_or_update"
        and item.get("dry_run_verification", {}).get("ok") is True
    ]
    if not pending:
        raise ContactFormCopyError("no pending verified outreach drafts")

    drafts_by_label = {
        draft["target_label"]: draft
        for draft in pack.get("drafts", [])
    }
    target_labels = set(drafts_by_label)
    out_dir.mkdir(parents=True, exist_ok=True)
    _remove_generated_files(out_dir)

    files = []
    for ordinal, item in enumerate(pending, start=1):
        draft = drafts_by_label.get(item["target_label"])
        if draft is None:
            raise ContactFormCopyError(f"draft not found for target: {item['target_label']}")
        rendered = render_contact_form_text(
            draft,
            target_labels=target_labels,
            message_module=message_module,
            max_chars=max_chars,
        )
        path = out_dir / f"{ordinal:02d}.txt"
        path.write_text(rendered, encoding="utf-8")
        files.append(
            {
                "ordinal": ordinal,
                "target_label": item["target_label"],
                "group": item["group"],
                "path": str(path),
                "subject": _subject_from_copy_text(rendered),
                "char_count": len(rendered),
                "sha256": hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
                "dry_run_apply_command": item.get("dry_run_apply_command"),
                "pre_send_check_command": draft.get(
                    "pre_send_check_command",
                    "make validation-pre-send-check "
                    f"TARGET={item['target_label']} DATE={status['generated_for']}",
                ),
                "confirmed_apply_command": item.get("confirmed_apply_command"),
            }
        )

    readme_path = out_dir / "README.md"
    checklist_path = out_dir / "CHECKLIST.md"
    index_path = out_dir / "CONTACT_FORM_INDEX.md"
    do_not_send_path = out_dir / "DO_NOT_SEND.md"
    readme_path.write_text(
        _render_readme(
            generated_for=status["generated_for"],
            copy_file_count=len(files),
            max_chars=max_chars,
        ),
        encoding="utf-8",
    )
    checklist_path.write_text(
        _render_checklist(generated_for=status["generated_for"], files=files),
        encoding="utf-8",
    )
    index_path.write_text(
        _render_index(generated_for=status["generated_for"], files=files),
        encoding="utf-8",
    )
    do_not_send_path.write_text(
        _render_do_not_send(
            generated_for=status["generated_for"],
            copy_file_count=len(files),
            max_chars=max_chars,
        ),
        encoding="utf-8",
    )

    return {
        "schema_version": CONTACT_FORM_COPY_SCHEMA_VERSION,
        "message_pack_schema_version": pack["schema_version"],
        "status_schema_version": status["schema_version"],
        "generated_for": status["generated_for"],
        "outbound_safe": False,
        "copy_files_outbound_safe": True,
        "operator_metadata_outbound_safe": False,
        "private_metadata": True,
        "send_boundary": "copy_contact_form_txt_contents_only",
        "out_dir": str(out_dir),
        "readme_path": str(readme_path),
        "checklist_path": str(checklist_path),
        "index_path": str(index_path),
        "do_not_send_path": str(do_not_send_path),
        "contact_form_max_chars": max_chars,
        "copy_file_count": len(files),
        "pending_send_or_update_count": status["counts"]["pending_send_or_update"],
        "needs_attention_count": status["counts"]["needs_attention"],
        "dry_run_verified_count": status["dry_run_verified_count"],
        "files": files,
        "operator_notes": [
            "Use these files only when a public contact form needs shorter copy.",
            "Each numbered file is outbound copy; do not attach the file.",
            "Do not send the manifest, README, checklist, index, or DO_NOT_SEND guard.",
            "Run the matching dry-run and pre-send check before sending each file's contents.",
            "Run the matching CONFIRM_SENT=1 command only after that message was actually sent.",
        ],
    }


def check_contact_form_copy_directory(
    out_dir: Path,
    *,
    require_date: str | None = None,
    max_chars: int | None = None,
) -> dict[str, Any]:
    if require_date is not None:
        _validate_date(require_date)
    if not out_dir.is_dir():
        raise ContactFormCopyError(f"contact-form copy directory not found: {out_dir}")
    message_module = _load_module("validation-message-pack.py", "validation_message_pack")
    manifest_path = out_dir / "manifest.json"
    manifest = _load_json_object(manifest_path, "contact-form copy manifest")
    if manifest.get("schema_version") != CONTACT_FORM_COPY_SCHEMA_VERSION:
        raise ContactFormCopyError("contact-form copy manifest schema_version is unsupported")
    generated_for = str(manifest.get("generated_for") or "")
    if require_date is not None and generated_for != require_date:
        raise ContactFormCopyError(
            f"contact-form copy date {generated_for} does not match required date {require_date}"
        )
    manifest_max_chars = _int_field(
        manifest,
        "contact_form_max_chars",
        default=DEFAULT_MAX_CHARS,
    )
    effective_max_chars = max_chars if max_chars is not None else manifest_max_chars
    _validate_max_chars(effective_max_chars)
    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        raise ContactFormCopyError("contact-form copy manifest must list copy files")
    target_labels = {
        str(file.get("target_label"))
        for file in files
        if isinstance(file, dict) and file.get("target_label")
    }
    checked_files = []
    for file in files:
        if not isinstance(file, dict):
            raise ContactFormCopyError("contact-form copy file entries must be objects")
        path = Path(str(file.get("path") or ""))
        if not path.is_absolute():
            path = out_dir / path.name
        if path.parent.resolve() != out_dir.resolve():
            raise ContactFormCopyError(
                f"contact-form copy file must stay inside directory: {path}"
            )
        if not re.fullmatch(r"[0-9][0-9]\.txt", path.name):
            raise ContactFormCopyError(
                f"contact-form copy file name must be neutral and numbered: {path.name}"
            )
        rendered = path.read_text(encoding="utf-8")
        _validate_contact_form_text(
            rendered,
            target_labels=target_labels,
            message_module=message_module,
            max_chars=effective_max_chars,
        )
        expected_sha = str(file.get("sha256") or "")
        actual_sha = hashlib.sha256(rendered.encode("utf-8")).hexdigest()
        if expected_sha != actual_sha:
            raise ContactFormCopyError(f"contact-form copy sha256 mismatch: {path.name}")
        if int(file.get("char_count", -1)) != len(rendered):
            raise ContactFormCopyError(f"contact-form copy char_count mismatch: {path.name}")
        checked_files.append(
            {
                "path": str(path),
                "char_count": len(rendered),
                "sha256": actual_sha,
            }
        )
    actual_names = sorted(path.name for path in out_dir.glob("[0-9][0-9].txt"))
    manifest_names = sorted(Path(str(file["path"])).name for file in files)
    if actual_names != manifest_names:
        raise ContactFormCopyError("contact-form copy file list does not match manifest")

    readme_path = _metadata_path(
        manifest.get("readme_path"),
        out_dir=out_dir,
        expected_name="README.md",
    )
    checklist_path = _metadata_path(
        manifest.get("checklist_path"),
        out_dir=out_dir,
        expected_name="CHECKLIST.md",
    )
    index_path = _metadata_path(
        manifest.get("index_path"),
        out_dir=out_dir,
        expected_name="CONTACT_FORM_INDEX.md",
    )
    do_not_send_path = _metadata_path(
        manifest.get("do_not_send_path"),
        out_dir=out_dir,
        expected_name="DO_NOT_SEND.md",
    )
    _assert_metadata_body(
        readme_path,
        _render_readme(
            generated_for=generated_for,
            copy_file_count=len(files),
            max_chars=manifest_max_chars,
        ),
    )
    _assert_metadata_body(
        checklist_path,
        _render_checklist(generated_for=generated_for, files=files),
    )
    _assert_metadata_body(
        index_path,
        _render_index(generated_for=generated_for, files=files),
    )
    _assert_metadata_body(
        do_not_send_path,
        _render_do_not_send(
            generated_for=generated_for,
            copy_file_count=len(files),
            max_chars=manifest_max_chars,
        ),
    )
    return {
        "schema_version": "prophet_validation_contact_form_copy_check.v0.1",
        "generated_for": generated_for,
        "out_dir": str(out_dir),
        "copy_file_count": len(checked_files),
        "copy_files_outbound_safe": True,
        "operator_metadata_outbound_safe": False,
        "operator_metadata_private_by_design": True,
        "send_boundary": "copy_contact_form_txt_contents_only",
        "contact_form_max_chars": manifest_max_chars,
        "readme_exists": True,
        "readme_matches_manifest": True,
        "checklist_exists": True,
        "checklist_matches_manifest": True,
        "index_exists": True,
        "index_matches_manifest": True,
        "do_not_send_exists": True,
        "do_not_send_matches_manifest": True,
        "checked_files": checked_files,
    }


def render_contact_form_text(
    draft: dict[str, Any],
    *,
    target_labels: set[str],
    message_module: Any,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    rendered = "\n".join(
        [
            f"Subject: {_contact_subject(draft)}",
            "",
            _contact_body(draft),
            "",
        ]
    )
    _validate_contact_form_text(
        rendered,
        target_labels=target_labels,
        message_module=message_module,
        max_chars=max_chars,
    )
    return rendered


def expected_contact_form_text(
    pack: dict[str, Any],
    *,
    target_label: str,
    max_chars: int = DEFAULT_MAX_CHARS,
) -> str:
    message_module = _load_module("validation-message-pack.py", "validation_message_pack")
    draft = _draft_by_label(pack, target_label)
    return render_contact_form_text(
        draft,
        target_labels={
            str(item["target_label"])
            for item in pack.get("drafts", [])
            if isinstance(item, dict) and item.get("target_label")
        },
        message_module=message_module,
        max_chars=max_chars,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Write compact contact-form copy for verified validation outreach drafts."
    )
    parser.add_argument(
        "--check-dir",
        help="Validate an existing contact-form copy directory without writing files.",
    )
    parser.add_argument(
        "--message-pack",
        default=str(DEFAULT_MESSAGE_PACK),
        help="Path to prophet_validation_message_pack.v0.1 JSON.",
    )
    parser.add_argument(
        "--targets",
        default=str(DEFAULT_TARGETS),
        help="Path to prophet_validation_targets.v0.1 JSON.",
    )
    parser.add_argument(
        "--require-date",
        help="Require the message pack generated_for date to match YYYY-MM-DD.",
    )
    parser.add_argument(
        "--out-dir",
        help="Directory for compact copy files. Defaults to validation/private/contact-form-copy-YYYY-MM-DD.",
    )
    parser.add_argument(
        "--manifest-out",
        help="Optional path for the private JSON manifest. Defaults to OUT_DIR/manifest.json.",
    )
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help="Maximum character count allowed for each numbered copy file.",
    )
    args = parser.parse_args(argv)

    try:
        if args.check_dir:
            summary = check_contact_form_copy_directory(
                Path(args.check_dir),
                require_date=args.require_date,
                max_chars=args.max_chars,
            )
            print(json.dumps(summary, indent=2, sort_keys=True))
            return 0
        pack = _load_json_object(Path(args.message_pack), "message pack")
        targets = _load_json_object(Path(args.targets), "target tracker")
        run_date = args.require_date or str(pack.get("generated_for", ""))
        _validate_date(run_date)
        out_dir = Path(args.out_dir) if args.out_dir else Path(
            f"validation/private/contact-form-copy-{run_date}"
        )
        manifest = write_contact_form_copy(
            pack,
            targets,
            out_dir=out_dir,
            require_date=args.require_date,
            max_chars=args.max_chars,
        )
        manifest_out = Path(args.manifest_out) if args.manifest_out else out_dir / "manifest.json"
        manifest["manifest_path"] = str(manifest_out)
        manifest_out.parent.mkdir(parents=True, exist_ok=True)
        manifest_out.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except (OSError, json.JSONDecodeError, ContactFormCopyError) as exc:
        print(f"validation contact-form copy failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


def _contact_subject(draft: dict[str, Any]) -> str:
    if draft.get("kind") == "referral":
        return "Intro to a security leader with priority pain?"
    persona = _contact_persona_label(str(draft.get("persona_label", "")))
    if "security architecture" in persona:
        return "Who owns security-architecture evidence?"
    if "vulnerability management" in persona:
        return "Who owns vulnerability-priority evidence?"
    if "platform security" in persona:
        return "Who owns platform hardening evidence?"
    if draft.get("source") == "cold_outreach":
        return "Did a vuln event need a why-this-first packet?"
    return "Who owns hardening-priority evidence?"


def _contact_body(draft: dict[str, Any]) -> str:
    persona = _contact_persona_label(str(draft.get("persona_label", "")))
    if draft.get("kind") == "referral":
        return (
            "Hi,\n\n"
            "I'm looking for one operationally honest intro, not broad feedback.\n\n"
            "The person I need to learn from owns vulnerability prioritization, "
            "product security, platform security, CTI, or mission assurance and has "
            "personally had to answer: why are we hardening this exposure class first?\n\n"
            "Do you know someone who has had to build that evidence for leadership, "
            "a customer, CMMC, or a government requirement?\n\n"
            "No live data ask, no offensive work, no sales deck."
        )
    if draft.get("source") == "warm_intro_needed":
        return (
            "Hi,\n\n"
            f"I'm trying to reach someone in {persona} who has recently had to justify "
            "which exposure class or product family should be hardened first under "
            "KEV, CMMC, customer, mission, or audit pressure.\n\n"
            "The discovery question is narrow: does the team still manually turn "
            "scanner or exposure-management output into a leadership/SOC-ready "
            "evidence packet?\n\n"
            "I'm asking for 20 minutes on the last painful prioritization workflow, "
            "not a demo. No live data ask, no exploit tooling, no sales deck."
        )
    return (
        "Hi,\n\n"
        f"I'm trying to learn from {persona} teams that have recently had to justify "
        "what exposure class or product family gets hardened first.\n\n"
        "When KEV, CMMC, customer, mission, or audit pressure hits, does your workflow "
        "already produce the evidence packet leadership or SOC teams trust, or is "
        "there still manual assembly after scanner/exposure-management output?\n\n"
        "Could I ask 20 minutes about that workflow? No live data ask, no exploit "
        "tooling, no sales deck."
    )


def _contact_persona_label(persona: str) -> str:
    normalized = persona.strip()
    lower = normalized.lower()
    if "product security" in lower:
        return "product security"
    if "security engineering" in lower:
        return "security engineering"
    if "platform security" in lower:
        return "platform security"
    if "mission assurance" in lower:
        return "mission assurance"
    if "vulnerability management" in lower:
        return "vulnerability management"
    if "security architecture" in lower:
        return "security architecture"
    if "ciso" in lower or "security leadership" in lower:
        return "security leadership"
    if "cti" in lower:
        return "CTI"
    if "soc" in lower:
        return "SOC"
    return normalized or "security"


def _validate_contact_form_text(
    rendered: str,
    *,
    target_labels: set[str],
    message_module: Any,
    max_chars: int,
) -> None:
    _validate_max_chars(max_chars)
    if len(rendered) > max_chars:
        raise ContactFormCopyError(
            f"contact-form copy exceeds {max_chars} characters: {len(rendered)}"
        )
    subject_count = sum(1 for line in rendered.splitlines() if line.startswith("Subject: "))
    if subject_count != 1 or not rendered.startswith("Subject: "):
        raise ContactFormCopyError("contact-form copy must contain exactly one leading Subject line")
    blocked_literals = (
        "make validation-",
        "python3 scripts/validation-",
        "CONFIRM_SENT",
        "target-",
        "validation/private",
        "manifest.json",
        "README.md",
        "CHECKLIST.md",
        "CONTACT_FORM_INDEX.md",
        "DO_NOT_SEND.md",
        "Tracker update command",
        "Safe dry-run",
        "Confirmed-send",
        "Dry-run command",
    )
    for target_label in target_labels:
        if target_label in rendered:
            raise ContactFormCopyError(
                f"contact-form copy contains target label: {target_label}"
            )
    for literal in blocked_literals:
        if literal in rendered:
            raise ContactFormCopyError(
                f"contact-form copy contains tracker metadata: {literal}"
            )
    if re.search(r"<[^>\n]+>", rendered):
        raise ContactFormCopyError("contact-form copy contains placeholder text")
    for regex_name, label in (
        ("EMAIL_RE", "email-like text"),
        ("URL_RE", "URL-like text"),
        ("PHONE_RE", "phone-like text"),
        ("PRIVATE_HOST_RE", "private hostname-like text"),
    ):
        regex = getattr(message_module, regex_name, None)
        if regex is not None and regex.search(rendered):
            raise ContactFormCopyError(f"contact-form copy contains {label}")
    if re.search(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", rendered):
        raise ContactFormCopyError("contact-form copy contains IP-like text")
    if "No live data ask" not in rendered:
        raise ContactFormCopyError("contact-form copy must keep the no-live-data boundary")


def _render_readme(*, generated_for: str, copy_file_count: int, max_chars: int) -> str:
    return "\n".join(
        [
            "# Prophet Contact-Form Copy Batch",
            "",
            f"Date: {generated_for}",
            f"Copy files: {copy_file_count}",
            f"Max characters per file: {max_chars}",
            "",
            "## Outbound Boundary",
            "",
            "- Use these shorter files only when a public contact form needs compact text.",
            "- Open each numbered `.txt` file and copy only its contents into the outreach channel.",
            "- Do not attach the `.txt` files; filenames and this directory are private operator workflow.",
            "- Do not send `manifest.json`, `CHECKLIST.md`, `CONTACT_FORM_INDEX.md`, `DO_NOT_SEND.md`, or this README.",
            "- Do not paste target labels, tracker commands, or contact-route notes into a buyer form.",
            "- Do not store recipient names or private contact details in repo files.",
            "",
            "## Tracker Boundary",
            "",
            f"- Before using an existing batch, run `make validation-contact-form-copy-check DATE={generated_for}`.",
            "- Run each matching dry-run command from the manifest before sending.",
            "- Run each matching pre-send check command immediately before sending.",
            "- Run each matching confirmed command only after that message was actually sent.",
            f"- Rerun `make validation-status DATE={generated_for}` after confirmed tracker updates.",
            "",
        ]
    )


def _render_checklist(*, generated_for: str, files: list[dict[str, Any]]) -> str:
    lines = [
        "# Prophet Contact-Form Copy Checklist",
        "",
        f"Date: {generated_for}",
        "",
        "This is private tracker/audit metadata. Do not send this checklist, target labels, or commands to buyers.",
        "",
        f"Before sending, run `make validation-contact-form-copy-check DATE={generated_for}` and proceed only if it passes.",
        "",
        "| Sent | File | Group | Target | Dry-run command | Pre-send check command | Confirmed-send command |",
        "|---|---|---|---|---|---|---|",
    ]
    for file in files:
        lines.append(
            "| [ ] "
            f"| `{Path(str(file['path'])).name}` "
            f"| `{file['group']}` "
            f"| `{file['target_label']}` "
            f"| `{file['dry_run_apply_command']}` "
            f"| `{file['pre_send_check_command']}` "
            f"| `{file['confirmed_apply_command']}` |"
        )
    lines.extend(
        [
            "",
            "After confirmed sends, rerun:",
            "",
            f"- `make validation-status DATE={generated_for}`",
            f"- `make validation-dashboard DATE={generated_for}`",
            "",
        ]
    )
    return "\n".join(lines)


def _render_index(*, generated_for: str, files: list[dict[str, Any]]) -> str:
    lines = [
        "# Prophet Contact-Form Copy Index",
        "",
        f"Date: {generated_for}",
        "",
        "This index intentionally omits target labels and tracker commands.",
        "Use it only to step through the numbered compact copy files.",
        "",
        "| File | Draft group | Characters | Outbound contents |",
        "|---|---|---:|---|",
    ]
    for file in files:
        lines.append(
            f"| `{Path(str(file['path'])).name}` "
            f"| `{file['group']}` "
            f"| {file['char_count']} "
            "| Copy the file contents only. |"
        )
    lines.extend(
        [
            "",
            "Do not attach this index, the manifest, checklist, README, DO_NOT_SEND guard, or the `.txt` files.",
            "",
        ]
    )
    return "\n".join(lines)


def _render_do_not_send(*, generated_for: str, copy_file_count: int, max_chars: int) -> str:
    return "\n".join(
        [
            "# Do Not Send",
            "",
            f"Date: {generated_for}",
            f"Copy files: {copy_file_count}",
            f"Max characters per file: {max_chars}",
            "",
            "This file is private operator metadata.",
            "",
            "Do not copy, attach, or send this file to a buyer.",
            "Do not send `manifest.json`, `CHECKLIST.md`, `CONTACT_FORM_INDEX.md`,",
            "or `README.md`.",
            "",
            "Only the contents of the numbered `.txt` files are outbound copy, and",
            "only after the contact-form copy check and pre-send check pass.",
            "",
            "After each actual send, use the matching confirmed tracker command in",
            "`CHECKLIST.md`. Do not run `CONFIRM_SENT=1` before the message is",
            "actually sent.",
            "",
        ]
    )


def _remove_generated_files(out_dir: Path) -> None:
    generated = {
        *out_dir.glob("[0-9][0-9].txt"),
        out_dir / "README.md",
        out_dir / "CHECKLIST.md",
        out_dir / "CONTACT_FORM_INDEX.md",
        out_dir / "DO_NOT_SEND.md",
    }
    for path in generated:
        if path.is_file():
            path.unlink()


def _subject_from_copy_text(rendered: str) -> str:
    first_line = rendered.splitlines()[0] if rendered.splitlines() else ""
    return first_line.removeprefix("Subject: ").strip()


def _draft_by_label(pack: dict[str, Any], target_label: str) -> dict[str, Any]:
    for draft in pack.get("drafts", []):
        if isinstance(draft, dict) and draft.get("target_label") == target_label:
            return draft
    raise ContactFormCopyError(f"target_label not found in message pack: {target_label}")


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ContactFormCopyError(f"{label} must be a JSON object")
    return value


def _metadata_path(value: object, *, out_dir: Path, expected_name: str) -> Path:
    path = Path(str(value or ""))
    if not path.is_absolute():
        path = out_dir / path.name
    if path.parent.resolve() != out_dir.resolve() or path.name != expected_name:
        raise ContactFormCopyError(
            f"metadata path must be {expected_name} inside contact-form copy directory"
        )
    if not path.is_file():
        raise ContactFormCopyError(f"metadata file is missing: {expected_name}")
    return path


def _assert_metadata_body(path: Path, expected: str) -> None:
    actual = path.read_text(encoding="utf-8")
    if actual != expected:
        raise ContactFormCopyError(f"metadata file is stale: {path.name}")


def _int_field(value: dict[str, Any], field: str, *, default: int) -> int:
    raw = value.get(field, default)
    if not isinstance(raw, int):
        raise ContactFormCopyError(f"{field} must be an integer")
    return raw


def _validate_max_chars(value: int) -> None:
    if value < 400:
        raise ContactFormCopyError("max-chars must be at least 400")
    if value > 2000:
        raise ContactFormCopyError("max-chars must be at most 2000")


def _validate_date(value: str) -> None:
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ContactFormCopyError(f"require-date must be YYYY-MM-DD: {value}") from exc


def _load_module(filename: str, module_name: str) -> Any:
    script_path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if spec is None or spec.loader is None:
        raise ContactFormCopyError(f"could not load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
