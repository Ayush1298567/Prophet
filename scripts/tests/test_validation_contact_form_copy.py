from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTREACH_SCRIPT = ROOT / "scripts" / "validation-outreach-block.py"
MESSAGE_SCRIPT = ROOT / "scripts" / "validation-message-pack.py"
CONTACT_FORM_SCRIPT = ROOT / "scripts" / "validation-contact-form-copy.py"
APPLY_SCRIPT = ROOT / "scripts" / "validation-apply-draft-update.py"
EXAMPLE = ROOT / "docs" / "validation-targets.example.json"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


outreach_block = _load_module("validation_outreach_block_for_contact_form", OUTREACH_SCRIPT)
message_pack = _load_module("validation_message_pack_for_contact_form", MESSAGE_SCRIPT)
contact_form_copy = _load_module("validation_contact_form_copy", CONTACT_FORM_SCRIPT)


class ValidationContactFormCopyTests(unittest.TestCase):
    def test_writes_compact_contact_form_files_for_verified_pending_drafts(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "contact-form-copy"

            manifest = contact_form_copy.write_contact_form_copy(
                pack,
                targets,
                out_dir=out_dir,
                require_date="2026-05-10",
            )

            self.assertEqual(
                manifest["schema_version"],
                contact_form_copy.CONTACT_FORM_COPY_SCHEMA_VERSION,
            )
            self.assertEqual(manifest["generated_for"], "2026-05-10")
            self.assertFalse(manifest["outbound_safe"])
            self.assertTrue(manifest["copy_files_outbound_safe"])
            self.assertFalse(manifest["operator_metadata_outbound_safe"])
            self.assertTrue(manifest["private_metadata"])
            self.assertEqual(
                manifest["send_boundary"],
                "copy_contact_form_txt_contents_only",
            )
            self.assertEqual(manifest["contact_form_max_chars"], 650)
            self.assertEqual(manifest["copy_file_count"], 8)
            self.assertEqual(manifest["dry_run_verified_count"], 8)
            first = manifest["files"][0]
            self.assertEqual(first["target_label"], "target-dib-platform-001")
            self.assertEqual(first["path"], str(out_dir / "01.txt"))
            self.assertLessEqual(first["char_count"], 650)
            rendered = Path(first["path"]).read_text(encoding="utf-8")
            self.assertEqual(first["char_count"], len(rendered))
            self.assertEqual(
                first["sha256"],
                hashlib.sha256(rendered.encode("utf-8")).hexdigest(),
            )
            self.assertTrue(rendered.startswith("Subject: "))
            self.assertIn("Who owns hardening-priority evidence?", rendered)
            self.assertIn("Hi,", rendered)
            self.assertIn("No live data ask", rendered)
            self.assertNotIn("<first name>", rendered)
            self.assertNotRegex(rendered, r"<[^>\n]+>")
            self.assertNotIn("target-dib-platform-001", rendered)
            self.assertNotIn("make validation-apply-draft", rendered)
            self.assertNotIn("Tracker update command", rendered)
            self.assertNotIn("CONFIRM_SENT", rendered)
            self.assertNotIn("@", rendered)
            self.assertNotIn("http://", rendered)
            self.assertNotIn("https://", rendered)

            readme = Path(manifest["readme_path"]).read_text(encoding="utf-8")
            self.assertIn("public contact form needs compact text", readme)
            self.assertIn("make validation-contact-form-copy-check DATE=2026-05-10", readme)
            self.assertIn("Do not store recipient names", readme)
            self.assertNotIn("target-dib-platform-001", readme)
            self.assertNotIn("@", readme)
            checklist = Path(manifest["checklist_path"]).read_text(encoding="utf-8")
            self.assertIn("Prophet Contact-Form Copy Checklist", checklist)
            self.assertIn("`target-dib-platform-001`", checklist)
            self.assertIn(
                "`make validation-pre-send-check TARGET=target-dib-platform-001 DATE=2026-05-10`",
                checklist,
            )
            index = Path(manifest["index_path"]).read_text(encoding="utf-8")
            self.assertIn("Prophet Contact-Form Copy Index", index)
            self.assertIn("intentionally omits target labels", index)
            self.assertNotIn("target-dib-platform-001", index)
            self.assertNotIn("make validation-", index)
            do_not_send = Path(manifest["do_not_send_path"]).read_text(encoding="utf-8")
            self.assertIn("# Do Not Send", do_not_send)
            self.assertIn("Only the contents of the numbered `.txt` files", do_not_send)
            self.assertIn("CONFIRM_SENT=1", do_not_send)

    def test_check_contact_form_directory_validates_existing_batch(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "contact-form-copy"
            manifest = contact_form_copy.write_contact_form_copy(
                pack,
                targets,
                out_dir=out_dir,
                require_date="2026-05-10",
            )
            manifest_path = out_dir / "manifest.json"
            manifest["manifest_path"] = str(manifest_path)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            summary = contact_form_copy.check_contact_form_copy_directory(
                out_dir,
                require_date="2026-05-10",
            )

            self.assertEqual(summary["copy_file_count"], 8)
            self.assertTrue(summary["copy_files_outbound_safe"])
            self.assertFalse(summary["operator_metadata_outbound_safe"])
            self.assertTrue(summary["operator_metadata_private_by_design"])
            self.assertEqual(summary["send_boundary"], "copy_contact_form_txt_contents_only")
            self.assertTrue(summary["readme_matches_manifest"])
            self.assertTrue(summary["checklist_matches_manifest"])
            self.assertTrue(summary["index_matches_manifest"])
            self.assertTrue(summary["do_not_send_matches_manifest"])
            self.assertTrue(
                all(file["char_count"] <= 650 for file in summary["checked_files"])
            )

    def test_check_rejects_stale_metadata(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "contact-form-copy"
            manifest = contact_form_copy.write_contact_form_copy(
                pack,
                targets,
                out_dir=out_dir,
                require_date="2026-05-10",
            )
            manifest_path = out_dir / "manifest.json"
            manifest["manifest_path"] = str(manifest_path)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            (out_dir / "CONTACT_FORM_INDEX.md").write_text("stale\n", encoding="utf-8")

            with self.assertRaisesRegex(
                contact_form_copy.ContactFormCopyError,
                "metadata file is stale",
            ):
                contact_form_copy.check_contact_form_copy_directory(
                    out_dir,
                    require_date="2026-05-10",
                )

    def test_rejects_contact_form_copy_over_character_limit(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(
                contact_form_copy.ContactFormCopyError,
                "exceeds 500 characters",
            ):
                contact_form_copy.write_contact_form_copy(
                    pack,
                    targets,
                    out_dir=Path(tmp),
                    require_date="2026-05-10",
                    max_chars=500,
                )

    def test_cli_writes_manifest_and_files(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            pack_path = tmp_path / "pack.json"
            targets_path = tmp_path / "targets.json"
            out_dir = tmp_path / "contact-form-copy"
            manifest_path = out_dir / "manifest.json"
            pack_path.write_text(json.dumps(pack), encoding="utf-8")
            targets_path.write_text(json.dumps(targets), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(CONTACT_FORM_SCRIPT),
                    "--message-pack",
                    str(pack_path),
                    "--targets",
                    str(targets_path),
                    "--require-date",
                    "2026-05-10",
                    "--out-dir",
                    str(out_dir),
                    "--manifest-out",
                    str(manifest_path),
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            manifest = json.loads(completed.stdout)
            self.assertEqual(manifest["copy_file_count"], 8)
            self.assertEqual(manifest["manifest_path"], str(manifest_path))
            self.assertEqual(json.loads(manifest_path.read_text(encoding="utf-8")), manifest)
            self.assertTrue((out_dir / "08.txt").exists())
            self.assertTrue((out_dir / "README.md").exists())
            self.assertTrue((out_dir / "CHECKLIST.md").exists())
            self.assertTrue((out_dir / "CONTACT_FORM_INDEX.md").exists())
            self.assertTrue((out_dir / "DO_NOT_SEND.md").exists())

    def test_cli_check_dir_validates_existing_batch_without_writing(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "contact-form-copy"
            manifest = contact_form_copy.write_contact_form_copy(
                pack,
                targets,
                out_dir=out_dir,
                require_date="2026-05-10",
            )
            manifest_path = out_dir / "manifest.json"
            manifest["manifest_path"] = str(manifest_path)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(CONTACT_FORM_SCRIPT),
                    "--check-dir",
                    str(out_dir),
                    "--require-date",
                    "2026-05-10",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertEqual(summary["copy_file_count"], 8)
            self.assertTrue(summary["copy_files_outbound_safe"])

    def test_apply_draft_accepts_contact_form_manifest_for_confirmed_write(self) -> None:
        targets, pack = _targets_and_pack()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            targets_path = tmp_path / "targets.json"
            pack_path = tmp_path / "pack.json"
            out_dir = tmp_path / "contact-form-copy"
            manifest_path = out_dir / "manifest.json"
            targets_path.write_text(json.dumps(targets), encoding="utf-8")
            pack_path.write_text(json.dumps(pack), encoding="utf-8")
            manifest = contact_form_copy.write_contact_form_copy(
                pack,
                targets,
                out_dir=out_dir,
                require_date="2026-05-10",
            )
            manifest["manifest_path"] = str(manifest_path)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            completed = subprocess.run(
                [
                    sys.executable,
                    str(APPLY_SCRIPT),
                    "--message-pack",
                    str(pack_path),
                    "--targets",
                    str(targets_path),
                    "--target-label",
                    "target-dib-platform-001",
                    "--require-date",
                    "2026-05-10",
                    "--require-copy-artifact",
                    "--contact-form-copy-manifest",
                    str(manifest_path),
                    "--confirm-sent",
                ],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            summary = json.loads(completed.stdout)
            self.assertTrue(summary["would_write"])
            self.assertEqual(
                summary["copy_artifact_verification"]["kind"],
                "contact_form_copy",
            )
            updated_targets = json.loads(targets_path.read_text(encoding="utf-8"))
            first = updated_targets["targets"][0]
            self.assertEqual(first["status"], "outreach_sent")
            self.assertEqual(first["last_touch"], "2026-05-10")


def _targets_and_pack():
    targets = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    block = outreach_block.build_outreach_block(targets, run_date="2026-05-10")
    pack = message_pack.build_message_pack(block)
    return targets, pack


if __name__ == "__main__":
    unittest.main()
