"""Repeated validation confined to the fixed outer training partition."""
from numbers import Integral
from statistics import fmean, stdev

import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import RepeatedKFold

from education_outcomes.data import FEATURES, TARGET, validate_data
from education_outcomes.splitting import SplitConfig, split_positions


def summarize_fold_scores(folds: list[dict]) -> dict:
    """Describe variation among fold scores without claiming an interval estimate."""
    if len(folds) < 2:
        raise ValueError("At least two fold scores are required for a spread summary.")
    models = {}
    for model in ("linear_regression", "mean_baseline"):
        metrics = {}
        for metric in ("mae", "rmse"):
            values = [fold[model][metric] for fold in folds]
            metrics[metric] = {
                "mean": float(fmean(values)),
                "sample_standard_deviation": float(stdev(values)),
                "minimum": float(min(values)),
                "maximum": float(max(values)),
            }
        models[model] = metrics
    return {
        "summary_version": 1,
        "fold_count": len(folds),
        "unit": "grade points",
        "method": "Unweighted fold-score mean and sample standard deviation",
        "interpretation": (
            "Descriptive variability across repeated training folds; not a confidence "
            "interval or an estimate for a new population. Repeated folds share records."
        ),
        "models": models,
    }


def evaluate_training_folds(
    frame: pd.DataFrame,
    split_config: SplitConfig | None = None,
    *,
    n_splits: int = 5,
    n_repeats: int = 3,
    cv_seed: int = 17,
) -> dict:
    """Score fixed folds without fitting or validating on the outer holdout."""
    validate_data(frame)
    settings = split_config if split_config is not None else SplitConfig()
    outer_train_positions, holdout_positions = split_positions(len(frame), settings)
    if isinstance(n_splits, bool) or not isinstance(n_splits, Integral) or not 2 <= n_splits <= len(outer_train_positions):
        raise ValueError("Fold count must be an integer from 2 through the outer training row count.")
    if isinstance(n_repeats, bool) or not isinstance(n_repeats, Integral) or n_repeats < 1:
        raise ValueError("Repeat count must be a positive integer.")
    SplitConfig(seed=cv_seed)  # Apply the same seed range rules as the outer split.

    folds = []
    splitter = RepeatedKFold(
        n_splits=int(n_splits), n_repeats=int(n_repeats), random_state=int(cv_seed)
    )
    for index, (fit_indices, validation_indices) in enumerate(
        splitter.split(outer_train_positions)
    ):
        fit_positions = [outer_train_positions[position] for position in fit_indices]
        validation_positions = [
            outer_train_positions[position] for position in validation_indices
        ]
        fit_rows = frame.iloc[fit_positions]
        validation_rows = frame.iloc[validation_positions]
        x_fit, y_fit = fit_rows[FEATURES], fit_rows[TARGET]
        x_validation, y_validation = (
            validation_rows[FEATURES], validation_rows[TARGET]
        )

        def scores(model) -> dict:
            prediction = model.fit(x_fit, y_fit).predict(x_validation)
            return {
                "mae": float(mean_absolute_error(y_validation, prediction)),
                "rmse": float(mean_squared_error(y_validation, prediction) ** 0.5),
            }

        fold = {
            "repeat": index // n_splits + 1,
            "fold": index % n_splits + 1,
            "training_count": len(fit_positions),
            "validation_count": len(validation_positions),
            "validation_positions": validation_positions,
            "linear_regression": scores(LinearRegression()),
            "mean_baseline": scores(DummyRegressor(strategy="mean")),
        }
        folds.append(fold)

    return {
        "validation_version": 1,
        "method": "RepeatedKFold",
        "n_splits": int(n_splits),
        "n_repeats": int(n_repeats),
        "cv_seed": int(cv_seed),
        "outer_split_seed": int(settings.seed),
        "outer_test_fraction": float(settings.test_fraction),
        "row_count": len(frame),
        "outer_training_count": len(outer_train_positions),
        "reserved_holdout_count": len(holdout_positions),
        "features": FEATURES.copy(),
        "target": TARGET,
        "folds": folds,
        "score_summary": summarize_fold_scores(folds),
        "limitations": [
            "Validation uses historical training rows only; the reserved holdout is excluded.",
            "Fold scores are exploratory and do not establish performance for new populations.",
        ],
    }
