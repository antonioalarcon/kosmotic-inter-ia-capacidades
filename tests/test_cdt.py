"""Pruebas sintéticas y sin dependencias externas."""
import unittest
from cdt import inspect_records, normalize_records


class TestCDT(unittest.TestCase):
    def test_inspection_does_not_mutate(self):
        rows = [{"id": " 01 ", "name": " Ana "}, {"id": "01", "name": ""}, {"name": None}]
        before = [dict(r) for r in rows]
        report = inspect_records(rows, required=("id", "name"), unique_key="id")
        self.assertEqual(report["rows"], 3)
        self.assertEqual(report["duplicate_keys"], 1)
        self.assertEqual(report["missing_by_column"]["name"], 2)
        self.assertEqual(report["missing_unique_keys"], 1)
        self.assertEqual(rows, before)
        self.assertNotIn("Ana", str(report))

    def test_normalization_is_copy_only(self):
        rows = [{"name": " Ana ", "id": " 1 "}]
        cleaned = normalize_records(rows, ("name",))
        self.assertEqual(cleaned[0]["name"], "Ana")
        self.assertEqual(cleaned[0]["id"], " 1 ")
        self.assertEqual(rows[0]["name"], " Ana ")

    def test_empty_dataset_and_required_fields(self):
        report = inspect_records([], required=("id",))
        self.assertEqual(report["missing_by_column"]["id"], 0)


if __name__ == "__main__":
    unittest.main()
