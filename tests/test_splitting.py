"""Reproducible train/holdout split settings and row positions."""
import unittest

from education_outcomes.splitting import SplitConfig, build_split_manifest, split_positions


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

    def test_manifest_binds_complete_disjoint_partition_to_source(self):
        source_hash = "A" * 64
        settings = SplitConfig(seed=7, test_fraction=0.25)
        manifest = build_split_manifest(60, source_hash, settings)
        train = manifest["train_positions"]
        test = manifest["test_positions"]

        self.assertEqual(manifest, build_split_manifest(60, source_hash, settings))
        self.assertEqual((train, test), split_positions(60, settings))
        self.assertEqual(manifest["source_sha256"], source_hash.lower())
        self.assertEqual((manifest["train_count"], manifest["test_count"]), (45, 15))
        self.assertEqual(len(set(train)), len(train))
        self.assertEqual(len(set(test)), len(test))
        self.assertFalse(set(train) & set(test))
        self.assertEqual(set(train) | set(test), set(range(60)))
        self.assertIn("not a student ID", manifest["row_identifier"])
        self.assertNotIn("G3", manifest)

    def test_manifest_rejects_invalid_hash_and_split(self):
        for invalid in ("", "z" * 64, "a" * 63, None):
            with self.subTest(invalid=invalid), self.assertRaisesRegex(
                ValueError, "Source SHA-256"
            ):
                build_split_manifest(60, invalid)
        with self.assertRaisesRegex(ValueError, "at least two rows"):
            build_split_manifest(1, "a" * 64)


if __name__ == "__main__":
    unittest.main()
