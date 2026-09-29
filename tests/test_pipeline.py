import unittest
from datetime import datetime, timezone
from hashlib import sha256
from unittest.mock import patch
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import pandas as pd
from education_outcomes.data import (
    build_provenance_manifest,
    download_data,
    validate_data,
)
from education_outcomes.model import evaluate


def sample():
    return pd.DataFrame({"G1": list(range(20))*3, "G2": list(range(20))*3,
                         "G3": list(range(20))*3, "sex": ["F"]*60})


class PipelineTests(unittest.TestCase):
    def test_schema_failures(self):
        for frame in [sample().drop(columns="G3"), sample().iloc[:2],
                      sample().assign(G1=21), sample().assign(G1=float("nan")),
                      sample().assign(G2="10"), sample().assign(G2=3.5)]:
            with self.subTest(frame=frame.head(1).to_dict()):
                with self.assertRaises(ValueError):
                    validate_data(frame)

    def test_evaluation_is_repeatable_and_uses_only_prior_grades(self):
        report = evaluate(sample())
        self.assertEqual(report, evaluate(sample()))
        self.assertEqual(report["features"], ["G1", "G2"])
        self.assertEqual(report["train_rows"] + report["test_rows"], 60)
        self.assertLess(report["linear_regression"]["mae"], 1e-10)
        self.assertGreater(report["mean_baseline"]["mae"], 1)

    def test_provenance_manifest_matches_file_and_records_attribution(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "student-por.csv"
            payload = b"G1;G2;G3\n1;2;3\n"
            path.write_bytes(payload)
            retrieved_at = datetime(2026, 9, 28, 16, 0, tzinfo=timezone.utc)

            manifest = build_provenance_manifest(path, retrieved_at)

            self.assertEqual(manifest["manifest_version"], 1)
            self.assertEqual(manifest["course"], "Portuguese")
            self.assertEqual(manifest["file_name"], "student-por.csv")
            self.assertEqual(manifest["retrieved_at_utc"], "2026-09-28T16:00:00Z")
            self.assertEqual(manifest["sha256"], sha256(payload).hexdigest())
            self.assertIn("CC BY 4.0", manifest["license"])
            self.assertTrue(manifest["license_url"].startswith("https://"))

    def test_provenance_requires_timezone_aware_retrieval_time(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "student-por.csv"
            path.write_bytes(b"dataset")
            with self.assertRaisesRegex(ValueError, "must include a timezone"):
                build_provenance_manifest(path, datetime(2026, 9, 28, 16, 0))

    def test_download_reads_only_expected_file(self):
        inner = BytesIO()
        with ZipFile(inner, "w") as z:
            z.writestr("student-por.csv", sample().to_csv(sep=";", index=False))
            z.writestr("../escape.txt", "should not be extracted")
        outer = BytesIO()
        with ZipFile(outer, "w") as z:
            z.writestr("student.zip", inner.getvalue())
        with TemporaryDirectory() as folder:
            target = Path(folder)/"raw"/"student-por.csv"
            with patch("education_outcomes.data.urlopen", return_value=BytesIO(outer.getvalue())):
                download_data(target)
            self.assertEqual(len(pd.read_csv(target, sep=";")), 60)
            manifest = build_provenance_manifest(
                target, datetime(2026, 9, 28, 16, 0, tzinfo=timezone.utc)
            )
            self.assertEqual(
                manifest["sha256"], sha256(target.read_bytes()).hexdigest()
            )
            self.assertFalse((Path(folder)/"escape.txt").exists())


if __name__ == "__main__":
    unittest.main()
