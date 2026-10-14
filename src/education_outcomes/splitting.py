"""Reproducible row-position splits for the historical benchmark."""
from dataclasses import dataclass
from math import ceil, isfinite
from numbers import Integral, Real
import re

from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class SplitConfig:
    """Settings for one train/holdout partition; defaults preserve the baseline."""
    seed: int = 42
    test_fraction: float = 0.2

    def __post_init__(self) -> None:
        if isinstance(self.seed, bool) or not isinstance(self.seed, Integral) or not 0 <= self.seed < 2**32:
            raise ValueError("Split seed must be an integer from 0 through 2**32 - 1.")
        if (
            isinstance(self.test_fraction, bool)
            or not isinstance(self.test_fraction, Real)
            or not isfinite(float(self.test_fraction))
            or not 0 < self.test_fraction < 1
        ):
            raise ValueError("Test fraction must be a finite number strictly between 0 and 1.")


def split_positions(row_count: int, config: SplitConfig | None = None) -> tuple[list[int], list[int]]:
    """Return disjoint train and holdout row positions for a fixed configuration."""
    if isinstance(row_count, bool) or not isinstance(row_count, Integral) or row_count < 2:
        raise ValueError("A split requires at least two rows.")
    settings = config if config is not None else SplitConfig()
    if ceil(row_count * float(settings.test_fraction)) >= row_count:
        raise ValueError("Test fraction leaves no training rows.")
    train_positions, test_positions = train_test_split(
        list(range(row_count)),
        test_size=float(settings.test_fraction),
        random_state=int(settings.seed),
    )
    return train_positions, test_positions


def build_split_manifest(
    row_count: int, source_sha256: str, config: SplitConfig | None = None
) -> dict:
    """Describe the benchmark partition without exporting student records."""
    if not isinstance(source_sha256, str) or re.fullmatch(
        r"[0-9a-fA-F]{64}", source_sha256
    ) is None:
        raise ValueError("Source SHA-256 must contain 64 hexadecimal characters.")
    settings = config if config is not None else SplitConfig()
    train_positions, test_positions = split_positions(row_count, settings)
    return {
        "manifest_version": 1,
        "source_sha256": source_sha256.lower(),
        "row_count": int(row_count),
        "row_identifier": "Zero-based CSV row position, excluding the header; not a student ID",
        "seed": int(settings.seed),
        "test_fraction": float(settings.test_fraction),
        "train_count": len(train_positions),
        "test_count": len(test_positions),
        "train_positions": train_positions,
        "test_positions": test_positions,
    }
