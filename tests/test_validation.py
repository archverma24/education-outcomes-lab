"""Schema-report and CLI export behavior."""
from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import pandas as pd

from education_outcomes.cli import main
from education_outcomes.data import schema_validation_report, validate_data


def sample():
    return pd.DataFrame({
        "G1": list(range(20)) * 3,
        "G2": list(range(20)) * 3,
        "G3": list(range(20)) * 3,
    })


class SchemaValidationTests(unittest.TestCase):
    def test_report_names_valid_and_invalid_rules(self):
        valid = schema_validation_report(sample())
        self.assertEqual(valid["status"], "valid")
        self.assertEqual(valid["row_count"], 60)
        self.assertEqual(valid["issues"], [])

        broken = sample().drop(columns="G3").iloc[:2].assign(G1=21, G2="bad")
        report = schema_validation_report(broken)
        self.assertEqual(report["status"], "invalid")
        self.assertEqual(
            {issue["code"] for issue in report["issues"]},
            {"missing_column", "too_few_rows", "grade_out_of_range", "non_numeric_grade"},
        )
        self.assertTrue(all(issue["message"] for issue in report["issues"]))
        with self.assertRaisesRegex(ValueError, "G1"):
            validate_data(broken)

    def test_cli_writes_valid_schema_report(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "student-por.csv"
            path.write_text(sample().to_csv(sep=";", index=False))
            validation_path = root / "validation.json"
            argv = [
                "education-outcomes", "--data", str(path),
                "--output", str(root / "baseline.json"),
                "--provenance-output", str(root / "provenance.json"),
                "--validation-output", str(validation_path),
            ]
            with patch("sys.argv", argv), redirect_stdout(StringIO()):
                main()

            report = json.loads(validation_path.read_text())
            self.assertEqual(report["status"], "valid")
            self.assertEqual(report["row_count"], 60)
            self.assertEqual(report["source_sha256"], sha256(path.read_bytes()).hexdigest())
            self.assertTrue((root / "baseline.json").exists())

    def test_cli_exports_invalid_report_and_exits_with_readable_error(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / "student-por.csv"
            path.write_text(sample().assign(G1=21).to_csv(sep=";", index=False))
            validation_path = root / "validation.json"
            baseline_path = root / "baseline.json"
            argv = [
                "education-outcomes", "--data", str(path),
                "--output", str(baseline_path),
                "--provenance-output", str(root / "provenance.json"),
                "--validation-output", str(validation_path),
            ]
            stderr = StringIO()
            with patch("sys.argv", argv), redirect_stdout(StringIO()), redirect_stderr(stderr):
                with self.assertRaises(SystemExit) as raised:
                    main()

            self.assertEqual(raised.exception.code, 1)
            self.assertIn("G1", stderr.getvalue())
            self.assertIn("0 to 20", stderr.getvalue())
            report = json.loads(validation_path.read_text())
            self.assertEqual(report["status"], "invalid")
            self.assertIn("grade_out_of_range", [issue["code"] for issue in report["issues"]])
            self.assertFalse(baseline_path.exists())


if __name__ == "__main__":
    unittest.main()
