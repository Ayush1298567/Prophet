from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGET_DOC = ROOT / "docs/SANDBOX_CONTAINER_TARGET.md"
RUNNER = ROOT / "sandbox_runner/runner.py"
RUN_MANIFEST_SCHEMA = ROOT / "sandbox_runner/sandbox-run-manifest.schema.json"
RUNNER_TESTS = ROOT / "sandbox_runner/tests/test_runner.py"
OPERATOR_TODO = ROOT / "docs/PROPHET_TODO.md"
MASTER_TODO = ROOT / "docs/PROPHET_MASTER_TODO.md"


class SandboxContainerTargetDocsTests(unittest.TestCase):
    def test_target_doc_keeps_container_mode_future_and_fail_closed(self) -> None:
        target = TARGET_DOC.read_text(encoding="utf-8")
        runner = RUNNER.read_text(encoding="utf-8")
        runner_tests = RUNNER_TESTS.read_text(encoding="utf-8")
        operator_todo = OPERATOR_TODO.read_text(encoding="utf-8")
        master_todo = MASTER_TODO.read_text(encoding="utf-8")
        run_manifest_schema = json.loads(RUN_MANIFEST_SCHEMA.read_text(encoding="utf-8"))

        for required in (
            "does not package or run a public\ncontainer profile",
            "does not enable live validation",
            "mode: fixture",
            "PROPHET_ENABLE_SANDBOX_RUNNER=1",
            "no public\n  container profiles are packaged",
            "safety.no_network_egress: true",
            "image digest",
            "CPU quota",
            "memory limit",
            "pids limit",
            "hard timeout",
            "read-only filesystem",
            "no privileged mode",
            "sanitized customer approval",
            "Do not describe Prophet as having a reproducible, no-egress, resource-limited\nsandbox container",
        ):
            with self.subTest(required=required):
                self.assertIn(required, target)

        self.assertEqual(
            run_manifest_schema["properties"]["mode"]["enum"],
            ["fixture"],
        )
        self.assertIn("PROPHET_ENABLE_SANDBOX_RUNNER", runner)
        self.assertIn("no container profiles are packaged in the public repo", runner)
        self.assertIn("test_container_mode_is_disabled_by_default", runner_tests)
        self.assertIn(
            "test_container_mode_still_has_no_public_packaged_profile_after_approval",
            runner_tests,
        )
        self.assertIn("docs/SANDBOX_CONTAINER_TARGET.md", operator_todo)
        self.assertIn("- [ ] Package `sandbox_runner` as a reproducible container.", operator_todo)
        self.assertIn("- [ ] Package sandbox runner as a reproducible container.", master_todo)
        self.assertIn("- [ ] Add container image hash to sandbox artifacts.", master_todo)


if __name__ == "__main__":
    unittest.main()
