import unittest
import pandas as pd

from education_outcomes.profile import audit_duplicate_rows, profile_dataset


class DatasetProfileTests(unittest.TestCase):
    def test_known_fixture_counts_types_missing_values_and_numeric_summary(self):
        frame = pd.DataFrame(
            {
                "G1": [10, 12, 14],
                "G2": [11.0, float("nan"), 15.0],
                "school": ["GP", "MS", "GP"],
            }
        )
        original = frame.copy(deep=True)

        profile = profile_dataset(frame)

        self.assertEqual(profile["row_count"], 3)
        self.assertEqual(profile["column_count"], 3)
        self.assertEqual(profile["column_types"]["G1"], "int64")
        self.assertEqual(profile["column_types"]["school"], "object")
        self.assertEqual(profile["missing_counts"], {"G1": 0, "G2": 1, "school": 0})
        self.assertEqual(profile["numeric_summary"]["G1"]["mean"], 12.0)
        self.assertEqual(profile["numeric_summary"]["G1"]["median"], 12.0)
        self.assertEqual(profile["numeric_summary"]["G2"]["count"], 2)
        self.assertEqual(profile["numeric_summary"]["G2"]["min"], 11.0)
        self.assertEqual(profile["numeric_summary"]["G2"]["max"], 15.0)
        self.assertNotIn("school", profile["numeric_summary"])
        pd.testing.assert_frame_equal(frame, original)

    def test_all_missing_numeric_column_has_json_safe_summary(self):
        frame = pd.DataFrame({"G1": [float("nan"), float("nan")]})

        profile = profile_dataset(frame)

        self.assertEqual(profile["missing_counts"]["G1"], 2)
        self.assertEqual(profile["numeric_summary"]["G1"]["count"], 0)
        self.assertIsNone(profile["numeric_summary"]["G1"]["mean"])
        self.assertIsNone(profile["numeric_summary"]["G1"]["std"])

    def test_exact_duplicate_audit_keeps_rows_and_checks_every_column(self):
        frame = pd.DataFrame(
            {
                "G1": [10, 10, 10, 10, 10],
                "G2": [11, 11, 11, 12, 11],
                "school": ["GP", "GP", "GP", "GP", "MS"],
            }
        )
        original = frame.copy(deep=True)

        audit = audit_duplicate_rows(frame)

        self.assertEqual(audit["rows_checked"], 5)
        self.assertEqual(audit["exact_duplicate_rows"], 2)
        self.assertEqual(audit["rows_removed"], 0)
        self.assertIn("every source column", audit["comparison"])
        self.assertIn("do not prove", audit["interpretation"])
        self.assertEqual(profile_dataset(frame)["duplicate_audit"], audit)
        pd.testing.assert_frame_equal(frame, original)

    def test_missing_values_can_be_part_of_an_exact_duplicate(self):
        frame = pd.DataFrame({"G1": [None, None], "school": ["GP", "GP"]})
        self.assertEqual(audit_duplicate_rows(frame)["exact_duplicate_rows"], 1)

    def test_duplicate_column_names_fail_clearly(self):
        frame = pd.DataFrame([[10, 11]], columns=["G1", "G1"])

        with self.assertRaisesRegex(ValueError, "unique column names"):
            profile_dataset(frame)
        with self.assertRaisesRegex(ValueError, "unique column names"):
            audit_duplicate_rows(frame)


if __name__ == "__main__":
    unittest.main()
