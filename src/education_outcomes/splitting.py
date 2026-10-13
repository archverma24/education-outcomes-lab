"""Reproducible row-position splits for the historical benchmark."""
from dataclasses import dataclass
from math import ceil, isfinite
from numbers import Integral, Real

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
