"""Reproducible train/holdout split settings and row positions."""
import unittest

from education_outcomes.splitting import SplitConfig, split_positions


class SplitConfigTests(unittest.TestCase):
    def test_fixed_settings_repeat_the_same_disjoint_partition(self):
        settings = SplitConfig(seed=7, test_fraction=0.25)
        train, test = split_positions(60, settings)

        self.assertEqual((train, test), split_positions(60, settings))
        self.assertEqual((len(train), len(test)), (45, 15))
        self.assertEqual(set(train) & set(test), set())
        self.assertEqual(set(train) | set(test), set(range(60)))
        self.assertEqual(split_positions(60), split_positions(60, SplitConfig()))

    def test_rejects_invalid_seed_fraction_and_too_small_split(self):
        for seed in (-1, 2**32, 1.5, True, "42"):
            with self.subTest(seed=seed), self.assertRaisesRegex(ValueError, "Split seed"):
                SplitConfig(seed=seed)
        for fraction in (0, 1, -0.1, 1.1, float("nan"), float("inf"), True, "0.2"):
            with self.subTest(fraction=fraction), self.assertRaisesRegex(ValueError, "Test fraction"):
                SplitConfig(test_fraction=fraction)
        with self.assertRaisesRegex(ValueError, "at least two rows"):
            split_positions(1)
        with self.assertRaisesRegex(ValueError, "leaves no training rows"):
            split_positions(2, SplitConfig(test_fraction=0.99))


if __name__ == "__main__":
    unittest.main()
