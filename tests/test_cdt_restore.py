"""Prueba de restauración sintética aislada, sin red."""
import tempfile
import unittest
from pathlib import Path
from cdt.restore_probe import create, verify


class RestoreProbeTests(unittest.TestCase):
    def test_roundtrip_and_corruption(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "package"
            create(destination)
            self.assertTrue(verify(destination))
            with self.assertRaises(FileExistsError):
                create(destination)
            (destination / "synthetic_data.json").write_text("corrupted", encoding="utf-8")
            with self.assertRaises(ValueError):
                verify(destination)


if __name__ == "__main__":
    unittest.main()
