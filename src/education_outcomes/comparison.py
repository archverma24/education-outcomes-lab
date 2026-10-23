"""Present like-for-like training validation and separately labeled historical holdout scores."""
import pandas as pd


def comparison_tables(validation: dict, holdout: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build display tables only when the two reports describe the same outer split."""
    if (
        validation["row_count"] != holdout["rows"]
        or validation["outer_training_count"] != holdout["train_rows"]
        or validation["reserved_holdout_count"] != holdout["test_rows"]
        or validation["outer_split_seed"] != holdout["seed"]
        or validation["outer_test_fraction"] != holdout["test_fraction"]
        or validation["features"] != holdout["features"]
    ):
        raise ValueError("Validation and historical holdout reports use different data or splits.")

    summary = validation["score_summary"]
    models = (
        ("Mean baseline", "mean_baseline"),
        ("Copy second-period grade", "g2_copy"),
        ("Linear regression", "linear_regression"),
    )
    training_rows = [
        {
            "Model": label,
            "Mean MAE (grade points)": summary["models"][key]["mae"]["mean"],
            "MAE fold SD (grade points)": summary["models"][key]["mae"]["sample_standard_deviation"],
            "Mean RMSE (grade points)": summary["models"][key]["rmse"]["mean"],
            "Folds": summary["fold_count"],
        }
        for label, key in models
    ]
    holdout_rows = [
        {
            "Model": label,
            "MAE (grade points)": holdout[key]["mae"],
            "RMSE (grade points)": holdout[key]["rmse"],
            "Holdout records": holdout["test_rows"],
        }
        for label, key in (
            ("Mean baseline", "mean_baseline"),
            ("Linear regression", "linear_regression"),
        )
    ]
    return pd.DataFrame(training_rows), pd.DataFrame(holdout_rows)
