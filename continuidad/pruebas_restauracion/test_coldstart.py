"""Pruebas offline de lógica. NO acreditan una descarga remota en frío."""
import json
from pathlib import Path
import tempfile
import unittest

from continuidad.pruebas_restauracion.restore_exp0001_coldstart import (
    restore, sha256, MANIFEST_PATH, ARTIFACT_PATH, EXPECTED_SHA256, EXPECTED_SIZE,
)

FIXTURE = (Path(__file__).resolve().parents[2] /
           "experiments/federacion-documental/EXP-0001/replica/EXP-0001.md")


def fixture_fetch(path):
    if path == MANIFEST_PATH:
        return json.dumps({"gid": "KOS-IIA-EXP-0001", "vid": "V0.1",
                           "sha256": EXPECTED_SHA256, "size_bytes": EXPECTED_SIZE}).encode()
    if path == ARTIFACT_PATH:
        return FIXTURE.read_bytes()
    raise ValueError("Ruta de fixture no autorizada")


class ColdStartTests(unittest.TestCase):
    def test_fixture_integrity(self):
        self.assertEqual(len(FIXTURE.read_bytes()), EXPECTED_SIZE)
        self.assertEqual(sha256(FIXTURE.read_bytes()), EXPECTED_SHA256)

    def test_restore_fixture_positive(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "restored"
            certificate = restore(target, fetcher=fixture_fetch, clock=lambda: "2026-10-19T00:00:00+00:00")
            self.assertEqual(certificate["result"], "PASS")
            self.assertEqual(certificate["fetch_method"], "TEST_FIXTURE")
            self.assertEqual((target / "EXP-0001.md").read_bytes(), FIXTURE.read_bytes())
            self.assertEqual(json.loads((target / "certificado.json").read_text())["sha256_restored"], EXPECTED_SHA256)

    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "restored"
            restore(target, fetcher=fixture_fetch)
            with self.assertRaises(FileExistsError):
                restore(target, fetcher=fixture_fetch)

    def test_manifest_mismatch_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "new"
            with self.assertRaises(ValueError):
                restore(target, fetcher=lambda _: b'{"gid":"WRONG"}')
            self.assertFalse(target.exists())

    def test_corrupt_replica_rejected(self):
        def corrupt(path):
            return fixture_fetch(path) if path == MANIFEST_PATH else b"corrupted"
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "new"
            with self.assertRaises(ValueError):
                restore(target, fetcher=corrupt)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
