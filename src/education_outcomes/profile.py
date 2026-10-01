"""Reusable aggregate description of a loaded dataset."""
import pandas as pd


def _number_or_none(value):
    return None if pd.isna(value) else float(value)


def profile_dataset(frame: pd.DataFrame) -> dict:
    """Summarize structure, missing values, and numeric columns without changing rows."""
    if not frame.columns.is_unique:
        raise ValueError("Dataset profile requires unique column names.")

    numeric_summary = {}
    for column in frame.select_dtypes(include="number").columns:
        values = frame[column]
        numeric_summary[column] = {
            "count": int(values.count()),
            "mean": _number_or_none(values.mean()),
            "median": _number_or_none(values.median()),
            "std": _number_or_none(values.std()),
            "min": _number_or_none(values.min()),
            "max": _number_or_none(values.max()),
        }

    return {
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "column_types": {column: str(dtype) for column, dtype in frame.dtypes.items()},
        "missing_counts": {
            column: int(count) for column, count in frame.isna().sum().items()
        },
        "numeric_summary": numeric_summary,
    }
