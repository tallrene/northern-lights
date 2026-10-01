import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lookup_dashboard as ld  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "lookup_dashboard.py"


class NormalisationTests(unittest.TestCase):
    def test_normalise_strips_spaces_and_hyphens(self):
        self.assertEqual(ld.normalise_plate("mh 15 ab 1234"), "MH15AB1234")
        self.assertEqual(ld.normalise_plate("MH-15-AB-1234"), "MH15AB1234")

    def test_validate_plate_accepts_common_shapes(self):
        self.assertTrue(ld.validate_plate("MH15AB1234"))
        self.assertTrue(ld.validate_plate("DL3CAB1234"))
        self.assertTrue(ld.validate_plate("MH15A1234"))

    def test_validate_plate_rejects_junk(self):
        self.assertFalse(ld.validate_plate("NOTAPLATE"))
        self.assertFalse(ld.validate_plate("1234"))
        self.assertFalse(ld.validate_plate(""))


class MaskOwnerNameTests(unittest.TestCase):
    def test_masks_each_name_part_to_initial(self):
        self.assertEqual(ld.mask_owner_name("Rene Gaikwad"), "R*** G***")

    def test_empty_name(self):
        self.assertEqual(ld.mask_owner_name(""), "")

    def test_never_leaks_full_name(self):
        masked = ld.mask_owner_name("Someone Fullname")
        self.assertNotIn("Someone", masked)
        self.assertNotIn("Fullname", masked)


class NoKeyBehaviourTests(unittest.TestCase):
    """Without a Surepass key, every field must say so -- never fabricate data."""

    def test_echallan_not_configured_without_key(self):
        r = ld.check_echallan("MH15AB1234", None)
        self.assertEqual(r["status"], "not_configured")
        self.assertIn("Surepass", r["reason"])

    def test_puc_not_configured_without_key(self):
        r = ld.check_puc("MH15AB1234", None)
        self.assertEqual(r["status"], "not_configured")
        self.assertIn("Surepass", r["reason"])

    def test_rc_not_configured_without_key(self):
        r = ld.check_rc("MH15AB1234", None)
        self.assertEqual(r["status"], "not_configured")
        self.assertIsNone(r["owner_name_masked"])

    def test_run_checks_returns_all_three_fields(self):
        result = ld.run_checks("MH15AB1234", None)
        self.assertEqual(set(result.keys()), {"plate", "echallan", "puc", "rc"})
        for field in ("echallan", "puc", "rc"):
            self.assertEqual(result[field]["status"], "not_configured")


class WithKeyBehaviourTests(unittest.TestCase):
    """With a key present, the stub must say it is unwired -- never a fake result."""

    def test_echallan_stub_with_key(self):
        r = ld.check_echallan("MH15AB1234", "fake-key")
        self.assertEqual(r["status"], "stub_not_implemented")

    def test_rc_stub_with_key_has_no_owner_name(self):
        r = ld.check_rc("MH15AB1234", "fake-key")
        self.assertEqual(r["status"], "stub_not_implemented")
        self.assertIsNone(r["owner_name_masked"])


class CliTests(unittest.TestCase):
    def test_cli_json_output_no_key(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "MH15AB1234", "--json"],
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(proc.returncode, 0)
        data = json.loads(proc.stdout)
        self.assertEqual(data["plate"], "MH15AB1234")
        self.assertEqual(data["echallan"]["status"], "not_configured")

    def test_cli_rejects_invalid_plate(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "NOTAPLATE"],
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(proc.returncode, 2)
        self.assertIn("does not look like", proc.stderr)

    def test_cli_text_output(self):
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "mh 15 ab 1234"],
            capture_output=True,
            text=True,
            env={"PATH": "/usr/bin:/bin"},
        )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Plate: MH15AB1234", proc.stdout)
        self.assertIn("[ECHALLAN]", proc.stdout)


if __name__ == "__main__":
    unittest.main()
