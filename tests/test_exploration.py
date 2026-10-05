"""Grade-chart subset behavior."""
import unittest

import pandas as pd

from education_outcomes.exploration import grade_distribution


class GradeDistributionTests(unittest.TestCase):
    def test_school_filter_counts_rows_without_changing_source(self):
        frame = pd.DataFrame({
            "school": ["GP", "MS", "GP", "MS", "GP"],
            "G3": [10, 11, 10, 12, 15],
        })
        original = frame.copy(deep=True)

        all_rows = grade_distribution(frame)
        gp = grade_distribution(frame, "GP")
        ms = grade_distribution(frame, "MS")

        self.assertEqual(all_rows, {"row_count": 5, "grade_counts": {10: 2, 11: 1, 12: 1, 15: 1}})
        self.assertEqual(gp, {"row_count": 3, "grade_counts": {10: 2, 15: 1}})
        self.assertEqual(ms, {"row_count": 2, "grade_counts": {11: 1, 12: 1}})
        for result in (all_rows, gp, ms):
            self.assertEqual(sum(result["grade_counts"].values()), result["row_count"])
        pd.testing.assert_frame_equal(frame, original)

    def test_unknown_school_and_missing_grade_fail_clearly(self):
        frame = pd.DataFrame({"school": ["GP"], "G3": [10]})
        with self.assertRaisesRegex(ValueError, "Unknown school"):
            grade_distribution(frame, "MS")
        with self.assertRaisesRegex(ValueError, "requires G3"):
            grade_distribution(frame.drop(columns="G3"))
        with self.assertRaisesRegex(ValueError, "non-missing G3"):
            grade_distribution(frame.assign(G3=float("nan")))
        with self.assertRaisesRegex(ValueError, "Unknown school"):
            grade_distribution(frame.drop(columns="school"), "GP")


if __name__ == "__main__":
    unittest.main()
