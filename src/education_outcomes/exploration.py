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
        record_count="size", mean_grade="mean", median_grade="median",
        minimum_grade="min", maximum_grade="max"
    )
    rows = [
        {
            "school": "(missing school)" if pd.isna(school) else str(school),
            "record_count": int(values["record_count"]),
            "mean_grade": float(values["mean_grade"]),
            "median_grade": float(values["median_grade"]),
            "grade_range": float(values["maximum_grade"] - values["minimum_grade"]),
        }
        for school, values in grouped.iterrows()
    ]
    return sorted(rows, key=lambda row: row["school"])


SCHOOL_SUMMARY_COLUMNS = (
    "School",
    "Course records",
    "Mean G3 (grade points)",
    "Median G3 (grade points)",
    "Range G3 (grade points)",
)


def school_grade_summary_table(frame: pd.DataFrame) -> pd.DataFrame:
    """Prepare the displayed aggregate table, with stable public column names."""
    return pd.DataFrame(school_grade_summary(frame)).rename(columns={
        "school": SCHOOL_SUMMARY_COLUMNS[0],
        "record_count": SCHOOL_SUMMARY_COLUMNS[1],
        "mean_grade": SCHOOL_SUMMARY_COLUMNS[2],
        "median_grade": SCHOOL_SUMMARY_COLUMNS[3],
        "grade_range": SCHOOL_SUMMARY_COLUMNS[4],
    }).reindex(columns=SCHOOL_SUMMARY_COLUMNS)


def school_grade_summary_csv(summary_table: pd.DataFrame) -> str:
    """Export exactly the displayed aggregate columns, excluding the row index."""
    if list(summary_table.columns) != list(SCHOOL_SUMMARY_COLUMNS):
        raise ValueError("School summary export requires the displayed aggregate columns.")
    return summary_table.to_csv(index=False)
