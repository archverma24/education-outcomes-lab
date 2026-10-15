"""Training-only repeated validation and fixed outer holdout coverage."""
import unittest

import pandas as pd

from education_outcomes.splitting import SplitConfig, split_positions
from education_outcomes.validation import evaluate_training_folds
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
