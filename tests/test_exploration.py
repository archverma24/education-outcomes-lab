"""Aggregate chart, school summary, outlier, and CSV export behavior."""
from io import StringIO
import unittest

import pandas as pd

from education_outcomes.exploration import (
    grade_distribution,
    grade_outlier_summary,
    school_grade_summary,
    school_grade_summary_csv,
    school_grade_summary_table,
)


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


class SchoolGradeSummaryTests(unittest.TestCase):
    def test_counts_and_grade_summaries_are_alphabetical_without_mutation(self):
        frame = pd.DataFrame({
            "school": ["MS", "GP", "GP", "MS", "GP"],
            "G3": [14, 10, 20, 16, 12],
        })
        original = frame.copy(deep=True)

        summary = school_grade_summary(frame)

        self.assertEqual(summary, [
            {"school": "GP", "record_count": 3, "mean_grade": 14.0, "median_grade": 12.0, "grade_range": 10.0},
            {"school": "MS", "record_count": 2, "mean_grade": 15.0, "median_grade": 15.0, "grade_range": 2.0},
        ])
        self.assertEqual(sum(row["record_count"] for row in summary), len(frame))
        pd.testing.assert_frame_equal(frame, original)

    def test_missing_school_is_labeled_and_invalid_grades_fail(self):
        frame = pd.DataFrame({"school": ["GP", None], "G3": [10, 12]})
        self.assertEqual(school_grade_summary(frame), [
            {"school": "(missing school)", "record_count": 1, "mean_grade": 12.0, "median_grade": 12.0, "grade_range": 0.0},
            {"school": "GP", "record_count": 1, "mean_grade": 10.0, "median_grade": 10.0, "grade_range": 0.0},
        ])
        with self.assertRaisesRegex(ValueError, "requires school and G3"):
            school_grade_summary(frame.drop(columns="school"))
        with self.assertRaisesRegex(ValueError, "requires school and G3"):
            school_grade_summary(frame.drop(columns="G3"))
        with self.assertRaisesRegex(ValueError, "non-missing G3"):
            school_grade_summary(frame.assign(G3=[10, float("nan")]))

    def test_csv_matches_displayed_aggregate_values_without_raw_rows(self):
        frame = pd.DataFrame({
            "school": ["MS", "GP", "GP", "MS", "GP"],
            "G3": [14, 10, 20, 16, 12],
            "unused_student_attribute": ["a", "b", "c", "d", "e"],
        })
        table = school_grade_summary_table(frame)
        csv_text = school_grade_summary_csv(table)
        exported = pd.read_csv(StringIO(csv_text))

        self.assertEqual(list(table.columns), [
            "School", "Course records", "Mean G3 (grade points)",
            "Median G3 (grade points)", "Range G3 (grade points)",
        ])
        pd.testing.assert_frame_equal(exported, table)
        self.assertEqual(exported["Course records"].sum(), len(frame))
        self.assertNotIn("unused_student_attribute", csv_text)
        self.assertNotIn("Unnamed: 0", exported.columns)
        with self.assertRaisesRegex(ValueError, "displayed aggregate columns"):
            school_grade_summary_csv(table.drop(columns="Range G3 (grade points)"))


class GradeOutlierSummaryTests(unittest.TestCase):
    def test_counts_low_and_high_grades_without_removing_rows(self):
        frame = pd.DataFrame({"G3": [0, 8, 9, 10, 10, 10, 11, 12, 20]})
        original = frame.copy(deep=True)

        result = grade_outlier_summary(frame)

        self.assertEqual(result["row_count"], 9)
        self.assertEqual((result["q1"], result["q3"]), (9.0, 11.0))
        self.assertEqual((result["lower_fence"], result["upper_fence"]), (6.0, 14.0))
        self.assertEqual(result["counts"], {
            "Below lower fence": 1,
            "Within fences": 7,
            "Above upper fence": 1,
        })
        self.assertEqual(sum(result["counts"].values()), len(frame))
        pd.testing.assert_frame_equal(frame, original)

    def test_requires_complete_numeric_grades(self):
        frame = pd.DataFrame({"G3": [10, 11]})
        with self.assertRaisesRegex(ValueError, "requires G3"):
            grade_outlier_summary(frame.drop(columns="G3"))
        with self.assertRaisesRegex(ValueError, "non-missing numeric G3"):
            grade_outlier_summary(frame.iloc[:0])
        with self.assertRaisesRegex(ValueError, "non-missing numeric G3"):
            grade_outlier_summary(frame.assign(G3=[10, float("nan")]))
        with self.assertRaisesRegex(ValueError, "non-missing numeric G3"):
            grade_outlier_summary(frame.assign(G3=["ten", "eleven"]))


if __name__ == "__main__":
    unittest.main()
