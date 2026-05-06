from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "validation-sprint-dashboard.py"
SPEC = importlib.util.spec_from_file_location("validation_sprint_dashboard", SCRIPT)
assert SPEC and SPEC.loader
dashboard = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dashboard
SPEC.loader.exec_module(dashboard)


class ValidationSprintDashboardTests(unittest.TestCase):
    def test_combines_example_scorecards_and_keeps_build_gate_closed(self) -> None:
        summary = dashboard.build_dashboard(
            log_path=ROOT / "docs/customer-validation-log.example.json",
            targets_path=ROOT / "docs/validation-targets.example.json",
            scripts_dir=ROOT / "scripts",
        )

        self.assertEqual(summary["schema_version"], dashboard.DASHBOARD_SCHEMA_VERSION)
        self.assertEqual(summary["customer_validation"]["verdict"], "insufficient_data")
        self.assertFalse(summary["build_gate"]["allowed_to_build_next_slice"])
        self.assertTrue(any("Do not build" in action for action in summary["next_actions"]))

    def test_missing_private_files_points_to_initializer(self) -> None:
        with self.assertRaisesRegex(dashboard.ValidationDashboardError, "init-validation-sprint"):
            dashboard.build_dashboard(
                log_path=ROOT / "validation/private/missing-log.json",
                targets_path=ROOT / "validation/private/missing-targets.json",
                scripts_dir=ROOT / "scripts",
            )


if __name__ == "__main__":
    unittest.main()
