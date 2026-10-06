"""Aggregate exploration helpers for the historical Portuguese-course data."""
import pandas as pd


def grade_distribution(frame: pd.DataFrame, school: str | None = None) -> dict:
    """Count final grades in all rows or one school, without changing the input."""
    if "G3" not in frame.columns:
        raise ValueError("Final-grade distribution requires G3.")
    if frame["G3"].isna().any():
        raise ValueError("Final-grade distribution requires non-missing G3 values.")
    if school is not None:
        if "school" not in frame.columns or school not in set(frame["school"].dropna()):
            raise ValueError(f"Unknown school selection: {school}.")
        selected = frame.loc[frame["school"] == school]
    else:
        selected = frame

    counts = selected["G3"].value_counts().sort_index()
    return {
        "row_count": int(len(selected)),
        "grade_counts": {int(grade): int(count) for grade, count in counts.items()},
    }


def school_grade_summary(frame: pd.DataFrame) -> list[dict]:
    """Summarize historical final grades by school without ranking groups."""
    if "school" not in frame.columns or "G3" not in frame.columns:
        raise ValueError("School summary requires school and G3 columns.")
    if frame["G3"].isna().any():
        raise ValueError("School summary requires non-missing G3 values.")

    grouped = frame.groupby("school", dropna=False)["G3"].agg(
        record_count="size", mean_grade="mean", median_grade="median"
    )
    rows = [
        {
            "school": "(missing school)" if pd.isna(school) else str(school),
            "record_count": int(values["record_count"]),
            "mean_grade": float(values["mean_grade"]),
            "median_grade": float(values["median_grade"]),
        }
        for school, values in grouped.iterrows()
    ]
    return sorted(rows, key=lambda row: row["school"])
