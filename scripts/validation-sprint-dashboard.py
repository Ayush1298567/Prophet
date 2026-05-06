#!/usr/bin/env python3
"""Combine Prophet validation target and interview scorecards into one daily view."""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any


DASHBOARD_SCHEMA_VERSION = "prophet_validation_sprint_dashboard.v0.1"
BUILD_VERDICTS = {"pilot_pull_detected", "build_next_slice"}
DEFAULT_LOG = Path("validation/private/customer-validation-log.json")
DEFAULT_TARGETS = Path("validation/private/validation-targets.json")


class ValidationDashboardError(ValueError):
    """Raised when the validation dashboard cannot be generated."""


def build_dashboard(
    *,
    log_path: str | Path = DEFAULT_LOG,
    targets_path: str | Path = DEFAULT_TARGETS,
    scripts_dir: str | Path = "scripts",
) -> dict[str, Any]:
    log = Path(log_path)
    targets = Path(targets_path)
    if not log.exists() or not targets.exists():
        missing = [str(path) for path in (log, targets) if not path.exists()]
        raise ValidationDashboardError(
            "private validation files missing: "
            + ", ".join(missing)
            + "; run python3 scripts/init-validation-sprint.py"
        )

    scripts = Path(scripts_dir)
    customer_module = _load_module(
        scripts / "customer-validation-scorecard.py",
        "customer_validation_scorecard_module",
    )
    targets_module = _load_module(
        scripts / "validation-targets-scorecard.py",
        "validation_targets_scorecard_module",
    )
    customer_scorecard = customer_module.build_scorecard(customer_module.load_json(log))
    target_scorecard = targets_module.build_scorecard(targets_module.load_json(targets))
    build_allowed = customer_scorecard["verdict"] in BUILD_VERDICTS
    next_actions = _next_actions(
        customer_scorecard=customer_scorecard,
        target_scorecard=target_scorecard,
        build_allowed=build_allowed,
    )
    return {
        "schema_version": DASHBOARD_SCHEMA_VERSION,
        "customer_validation": customer_scorecard,
        "target_pipeline": target_scorecard,
        "build_gate": {
            "allowed_to_build_next_slice": build_allowed,
            "reason": _build_gate_reason(customer_scorecard["verdict"]),
        },
        "daily_minimum": {
            "targeted_asks": 5,
            "follow_ups": 2,
            "referral_asks": 1,
            "private_log_update": 1,
        },
        "next_actions": next_actions,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Print a combined Prophet validation sprint dashboard."
    )
    parser.add_argument("--log", default=str(DEFAULT_LOG), help="Private validation log path.")
    parser.add_argument(
        "--targets",
        default=str(DEFAULT_TARGETS),
        help="Private validation target tracker path.",
    )
    parser.add_argument("--out-json", help="Optional path to write dashboard JSON.")
    args = parser.parse_args(argv)
    try:
        dashboard = build_dashboard(log_path=args.log, targets_path=args.targets)
    except Exception as exc:  # scorecard modules raise their own ValueErrors
        print(f"validation sprint dashboard failed: {exc}", file=sys.stderr)
        return 1
    rendered = json.dumps(dashboard, indent=2, sort_keys=True)
    print(rendered)
    if args.out_json:
        out_path = Path(args.out_json)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered + "\n", encoding="utf-8")
    return 0


def _load_module(path: Path, module_name: str) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ValidationDashboardError(f"could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _build_gate_reason(verdict: str) -> str:
    if verdict == "build_next_slice":
        return "Customer validation has enough qualified pull to build only the committed pilot's next required slice."
    if verdict == "pilot_pull_detected":
        return "Pilot pull exists; convert design partners before broad platform work."
    return "Customer validation has not proven enough buyer pull for more production platform work."


def _next_actions(
    *,
    customer_scorecard: dict[str, Any],
    target_scorecard: dict[str, Any],
    build_allowed: bool,
) -> list[str]:
    actions = [
        target_scorecard["next_action"],
        customer_scorecard["next_action"],
    ]
    if not build_allowed:
        actions.append("Do not build more production platform scope today.")
    actions.append("Run today's outreach block: 5 targeted asks, 2 follow-ups, 1 referral ask.")
    return actions


if __name__ == "__main__":
    raise SystemExit(main())
