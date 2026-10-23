"""Comparison view keeps training validation and historical holdout results separate."""
import unittest

import pandas as pd

from education_outcomes.comparison import comparison_tables
from education_outcomes.model import evaluate
from education_outcomes.validation import evaluate_training_folds


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        grades = list(range(20)) * 3
        frame = pd.DataFrame({"G1": grades, "G2": grades, "G3": grades})
        self.validation = evaluate_training_folds(frame)
        self.holdout = evaluate(frame)

    def test_validation_table_uses_same_fold_summary_for_all_three_models(self):
        training, historical = comparison_tables(self.validation, self.holdout)
        self.assertEqual(
            list(training["Model"]),
            ["Mean baseline", "Copy second-period grade", "Linear regression"],
        )
        self.assertEqual(list(training["Folds"]), [15, 15, 15])
        for label, key in (
            ("Mean baseline", "mean_baseline"),
            ("Copy second-period grade", "g2_copy"),
            ("Linear regression", "linear_regression"),
        ):
            row = training.set_index("Model").loc[label]
            summary = self.validation["score_summary"]["models"][key]
            self.assertEqual(row["Mean MAE (grade points)"], summary["mae"]["mean"])
            self.assertEqual(row["MAE fold SD (grade points)"], summary["mae"]["sample_standard_deviation"])
            self.assertEqual(row["Mean RMSE (grade points)"], summary["rmse"]["mean"])
        self.assertEqual(list(historical["Model"]), ["Mean baseline", "Linear regression"])
        self.assertEqual(list(historical["Holdout records"]), [self.holdout["test_rows"]] * 2)
        self.assertEqual(
            historical.set_index("Model").loc["Linear regression", "MAE (grade points)"],
            self.holdout["linear_regression"]["mae"],
        )
        self.assertNotIn("Copy second-period grade", set(historical["Model"]))

    def test_mismatched_outer_split_cannot_be_combined(self):
        changed = {**self.holdout, "seed": self.holdout["seed"] + 1}
        with self.assertRaisesRegex(ValueError, "different data or splits"):
            comparison_tables(self.validation, changed)


if __name__ == "__main__":
    unittest.main()
