"""A fixed-split, late-year grade prediction benchmark, not a decision system."""
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split
from education_outcomes.data import FEATURES, TARGET, validate_data


def evaluate(frame: pd.DataFrame, seed: int = 42) -> dict:
    validate_data(frame)
    x_train, x_test, y_train, y_test = train_test_split(
        frame[FEATURES], frame[TARGET], test_size=0.2, random_state=seed
    )
    linear = LinearRegression().fit(x_train, y_train)
    baseline = DummyRegressor(strategy="mean").fit(x_train, y_train)

    def scores(model):
        prediction = model.predict(x_test)
        return {"mae": float(mean_absolute_error(y_test, prediction)),
                "rmse": float(mean_squared_error(y_test, prediction) ** 0.5)}

    return {
        "dataset": "UCI Student Performance: Portuguese course only",
        "rows": len(frame), "train_rows": len(x_train), "test_rows": len(x_test),
        "seed": seed, "features": FEATURES.copy(), "target": TARGET,
        "timing": "After second-period grades are available; not early-warning prediction",
        "linear_regression": scores(linear), "mean_baseline": scores(baseline),
        "coefficients": dict(zip(FEATURES, map(float, linear.coef_))),
        "intercept": float(linear.intercept_),
        "limitations": ["Historical data from two Portuguese schools; not validated for Chicago students.",
                        "One random holdout; scores are exploratory, not production evidence.",
                        "Associations are not causal effects. No student-level decisions."],
    }
