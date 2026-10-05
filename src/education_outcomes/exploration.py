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
