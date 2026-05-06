#!/usr/bin/env python3
"""Initialize a gitignored local workspace for Prophet validation sprint data."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any


PRIVATE_DIR = Path("validation/private")
DEFAULT_FILES = (
    ("docs/customer-validation-log.example.json", "customer-validation-log.json"),
    ("docs/validation-targets.example.json", "validation-targets.json"),
)


class ValidationSprintInitError(ValueError):
    """Raised when the private validation workspace cannot be initialized."""


def initialize_workspace(
    *,
    repo_root: str | Path = ".",
    private_dir: str | Path = PRIVATE_DIR,
    force: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root)
    destination_root = root / private_dir
    written: list[str] = []
    skipped: list[str] = []

    destination_root.mkdir(parents=True, exist_ok=True)
    for source_rel, dest_name in DEFAULT_FILES:
        source = root / source_rel
        destination = destination_root / dest_name
        if not source.exists():
            raise ValidationSprintInitError(f"missing template: {source}")
        if destination.exists() and not force:
            skipped.append(str(destination))
            continue
        shutil.copyfile(source, destination)
        written.append(str(destination))

    readme = destination_root / "README.md"
    if not readme.exists() or force:
        readme.write_text(_private_readme(), encoding="utf-8")
        written.append(str(readme))
    else:
        skipped.append(str(readme))

    return {
        "ok": True,
        "private_dir": str(destination_root),
        "written": written,
        "skipped_existing": skipped,
        "next_commands": [
            "python3 scripts/validation-targets-scorecard.py --targets validation/private/validation-targets.json",
            "python3 scripts/customer-validation-scorecard.py --log validation/private/customer-validation-log.json",
            "python3 scripts/validation-sprint-dashboard.py",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Create gitignored private files for Prophet customer validation."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing docs/customer-validation-log.example.json.",
    )
    parser.add_argument(
        "--private-dir",
        default=str(PRIVATE_DIR),
        help="Gitignored directory for private validation files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing private validation templates.",
    )
    args = parser.parse_args(argv)
    try:
        summary = initialize_workspace(
            repo_root=args.repo_root,
            private_dir=args.private_dir,
            force=args.force,
        )
    except (OSError, ValidationSprintInitError) as exc:
        print(f"validation sprint init failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


def _private_readme() -> str:
    return """# Private Prophet Validation Workspace

This directory is gitignored. Keep real prospect and customer discovery notes
here, not in committed docs.

Allowed:

- anonymized account labels
- segment/persona labels
- outreach status
- sanitized workflow notes
- scorecard fields

Do not store:

- names
- emails
- phone numbers
- LinkedIn URLs
- private hostnames
- IPs
- screenshots
- transcripts
- raw customer exports
- secrets

Run:

```bash
python3 scripts/validation-sprint-dashboard.py
```
"""


if __name__ == "__main__":
    raise SystemExit(main())
