"""Training-only repeated validation and fixed outer holdout coverage."""
import unittest
from math import sqrt

import pandas as pd

from education_outcomes.splitting import SplitConfig, split_positions
from education_outcomes.validation import evaluate_training_folds, summarize_fold_scores


def sample():
    return pd.DataFrame({
        "G1": list(range(20)) * 3,
        "G2": list(range(20)) * 3,
        "G3": list(range(20)) * 3,
    })


class RepeatedValidationTests(unittest.TestCase):
    def test_repeats_cover_only_outer_training_rows(self):
        frame = sample()
        settings = SplitConfig(seed=7, test_fraction=0.25)
        report = evaluate_training_folds(
            frame, settings, n_splits=3, n_repeats=2, cv_seed=11
        )
        outer_train, holdout = split_positions(len(frame), settings)

        self.assertEqual(report, evaluate_training_folds(
            frame, settings, n_splits=3, n_repeats=2, cv_seed=11
        ))
        self.assertEqual((report["outer_training_count"], report["reserved_holdout_count"]), (45, 15))
        self.assertEqual(len(report["folds"]), 6)
        self.assertEqual(report["features"], ["G1", "G2"])
        for repeat in (1, 2):
            seen = []
            for fold in (item for item in report["folds"] if item["repeat"] == repeat):
                positions = fold["validation_positions"]
                self.assertEqual(fold["training_count"] + fold["validation_count"], 45)
                self.assertEqual(fold["validation_count"], len(positions))
                self.assertFalse(set(positions) & set(holdout))
                self.assertTrue(set(positions) <= set(outer_train))
                self.assertGreaterEqual(fold["linear_regression"]["mae"], 0)
                self.assertGreaterEqual(fold["mean_baseline"]["mae"], 0)
                seen.extend(positions)
            self.assertEqual(sorted(seen), sorted(outer_train))

    def test_holdout_target_changes_do_not_change_validation_scores(self):
        frame = sample()
        _, holdout = split_positions(len(frame))
        unchanged = evaluate_training_folds(frame)
        altered = frame.copy(deep=True)
        altered.iloc[holdout, altered.columns.get_loc("G3")] = 20
        self.assertEqual(unchanged, evaluate_training_folds(altered))

    def test_residuals_cover_each_training_row_and_ignore_holdout_targets(self):
        frame = sample()
        settings = SplitConfig(seed=7, test_fraction=0.25)
        report = evaluate_training_folds(frame, settings, n_splits=3, n_repeats=2, cv_seed=11)
        diagnostics = report["residual_diagnostics"]
        outer_train, holdout = split_positions(len(frame), settings)
        points = diagnostics["points"]

        self.assertEqual(diagnostics["row_count"], len(outer_train))
        self.assertEqual([point["row_position"] for point in points], sorted(outer_train))
        self.assertFalse({point["row_position"] for point in points} & set(holdout))
        self.assertEqual(diagnostics["zero_reference"], 0.0)
        self.assertIn("Predicted", diagnostics["x_label"])
        self.assertIn("Actual minus predicted", diagnostics["y_label"])
        for point in points:
            actual = frame.iloc[point["row_position"]]["G3"]
            self.assertAlmostEqual(
                point["residual_grade_points"],
                actual - point["predicted_grade"],
            )

        altered = frame.copy(deep=True)
        altered.iloc[holdout, altered.columns.get_loc("G3")] = 20
        self.assertEqual(
            diagnostics,
            evaluate_training_folds(
                altered, settings, n_splits=3, n_repeats=2, cv_seed=11
            )["residual_diagnostics"],
        )

    def test_summary_reports_known_fold_spread_without_interval_claim(self):
        folds = [
            {"linear_regression": {"mae": 1.0, "rmse": 2.0},
             "mean_baseline": {"mae": 2.0, "rmse": 3.0}},
            {"linear_regression": {"mae": 3.0, "rmse": 4.0},
             "mean_baseline": {"mae": 4.0, "rmse": 5.0}},
        ]
        summary = summarize_fold_scores(folds)
        self.assertEqual(summary["fold_count"], 2)
        self.assertEqual(summary["unit"], "grade points")
        self.assertIn("not a confidence interval", summary["interpretation"])
        linear_mae = summary["models"]["linear_regression"]["mae"]
        self.assertEqual(linear_mae["mean"], 2.0)
        self.assertAlmostEqual(linear_mae["sample_standard_deviation"], sqrt(2))
        self.assertEqual((linear_mae["minimum"], linear_mae["maximum"]), (1.0, 3.0))
        self.assertEqual(summary["models"]["mean_baseline"]["rmse"]["mean"], 4.0)
        with self.assertRaisesRegex(ValueError, "At least two"):
            summarize_fold_scores(folds[:1])

    def test_invalid_fold_settings_fail_clearly(self):
        frame = sample()
        for count in (1, 1000, True, 2.5):
            with self.subTest(count=count), self.assertRaisesRegex(ValueError, "Fold count"):
                evaluate_training_folds(frame, n_splits=count)
        for repeats in (0, -1, True, 1.5):
            with self.subTest(repeats=repeats), self.assertRaisesRegex(ValueError, "Repeat count"):
                evaluate_training_folds(frame, n_repeats=repeats)
        with self.assertRaisesRegex(ValueError, "Split seed"):
            evaluate_training_folds(frame, cv_seed=-1)


if __name__ == "__main__":
    unittest.main()
