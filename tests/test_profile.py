import unittest
import pandas as pd

from education_outcomes.profile import profile_dataset


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

    def test_duplicate_column_names_fail_clearly(self):
        frame = pd.DataFrame([[10, 11]], columns=["G1", "G1"])

        with self.assertRaisesRegex(ValueError, "unique column names"):
            profile_dataset(frame)


if __name__ == "__main__":
    unittest.main()
