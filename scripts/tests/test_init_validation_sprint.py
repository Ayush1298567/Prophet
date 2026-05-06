from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "init-validation-sprint.py"
SPEC = importlib.util.spec_from_file_location("init_validation_sprint", SCRIPT)
assert SPEC and SPEC.loader
init_validation_sprint = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = init_validation_sprint
SPEC.loader.exec_module(init_validation_sprint)


class InitValidationSprintTests(unittest.TestCase):
    def test_initializes_private_workspace_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "customer-validation-log.example.json").write_text('{"interviews": []}\n')
            (docs / "validation-targets.example.json").write_text('{"targets": []}\n')

            summary = init_validation_sprint.initialize_workspace(repo_root=root)

            private_dir = root / "validation/private"
            self.assertTrue((private_dir / "customer-validation-log.json").exists())
            self.assertTrue((private_dir / "validation-targets.json").exists())
            self.assertTrue((private_dir / "README.md").exists())
            self.assertEqual(len(summary["written"]), 3)

            second = init_validation_sprint.initialize_workspace(repo_root=root)
            self.assertEqual(second["written"], [])
            self.assertEqual(len(second["skipped_existing"]), 3)

    def test_force_overwrites_private_templates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "customer-validation-log.example.json").write_text('{"interviews": []}\n')
            (docs / "validation-targets.example.json").write_text('{"targets": []}\n')
            init_validation_sprint.initialize_workspace(repo_root=root)
            target = root / "validation/private/customer-validation-log.json"
            target.write_text('{"changed": true}\n')

            init_validation_sprint.initialize_workspace(repo_root=root, force=True)

            self.assertEqual(target.read_text(), '{"interviews": []}\n')


if __name__ == "__main__":
    unittest.main()
