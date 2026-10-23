"""Local dashboard; public hosting is a later project milestone."""
from hashlib import sha256
import json
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

from education_outcomes.comparison import comparison_tables
from education_outcomes.data import schema_validation_report
from education_outcomes.exploration import (
    grade_distribution,
    grade_outlier_summary,
    school_grade_summary_csv,
    school_grade_summary_table,
)
from education_outcomes.model import evaluate
from education_outcomes.profile import profile_dataset
from education_outcomes.validation import evaluate_training_folds


@st.cache_data(show_spinner=False)
def evaluate_full_dataset(frame: pd.DataFrame) -> dict:
    """Reuse unchanged full-dataset model results across chart-filter reruns."""
    return evaluate(frame)


@st.cache_data(show_spinner=False)
def evaluate_training_dataset(frame: pd.DataFrame) -> dict:
    """Cache training-only validation and residual diagnostics across chart reruns."""
    return evaluate_training_folds(frame)


st.set_page_config(page_title="Education Outcomes Lab", page_icon="📊", layout="wide")
st.title("Education Outcomes Lab")
st.caption("Public-data learning project • Reproducible analytics • Model quality")
st.info("Historical Portuguese-school data. This demo does not assess current students or recommend decisions.")
path = Path(__file__).parent / "data/raw/student-por.csv"
if not path.exists():
    st.warning("Dataset not installed. Run: education-outcomes --download")
    st.stop()

try:
    data = pd.read_csv(path, sep=";")
    validation = schema_validation_report(data)
    validation["source_sha256"] = sha256(path.read_bytes()).hexdigest()
    profile = profile_dataset(data) if data.columns.is_unique else None
except (OSError, ValueError) as error:
    st.error(f"Cannot inspect dataset: {error}")
    st.stop()

st.subheader("Data quality")
quality_a, quality_b, quality_c = st.columns(3)
quality_a.metric("Rows checked", validation["row_count"])
quality_b.metric("Schema checks", "Passed" if validation["status"] == "valid" else "Failed")
quality_c.metric(
    "Exact duplicate rows",
    profile["duplicate_audit"]["exact_duplicate_rows"] if profile else "Unavailable",
)
if profile:
    st.caption(profile["duplicate_audit"]["interpretation"])
else:
    st.caption("Duplicate-row count is unavailable until column names are unique.")
with st.expander("Full data-quality report"):
    st.json({"validation": validation, "profile": profile})

st.subheader("Missing values by column")
missing_counts = data.isna().sum()
st.metric("Missing cells", int(missing_counts.sum()))
st.dataframe(
    pd.DataFrame({
        "Column": [str(column) for column in missing_counts.index],
        "Missing records": [int(count) for count in missing_counts],
    }),
    hide_index=True,
)
nonzero_missing = missing_counts[missing_counts > 0]
if nonzero_missing.empty:
    st.success("No missing values in the current dataset.")
else:
    st.bar_chart(
        nonzero_missing.rename("Missing records"),
        x_label="Dataset column",
        y_label="Missing course records",
    )
st.caption(
    "The table lists missing course records for every column; the chart appears only "
    "for columns with missing values. No source rows are removed."
)

if validation["issues"]:
    st.error("Cannot analyze dataset: " + "; ".join(issue["message"] for issue in validation["issues"]))
    st.stop()

try:
    report = evaluate_full_dataset(data)
except (OSError, ValueError) as error:
    st.error(f"Cannot analyze dataset: {error}")
    st.stop()
a, b, c = st.columns(3)
a.metric("Course records", report["rows"])
b.metric("Historical holdout model MAE (grade points)", f'{report["linear_regression"]["mae"]:.2f}')
c.metric("Historical holdout mean MAE (grade points)", f'{report["mean_baseline"]["mae"]:.2f}')
st.subheader("Final-grade distribution")
school_options = sorted(data["school"].dropna().unique()) if "school" in data else []
if school_options:
    selected_school = st.selectbox(
        "School for grade chart", ["All schools", *school_options], key="grade_school"
    )
    school = None if selected_school == "All schools" else selected_school
else:
    school = None
    st.caption("School filter unavailable because this dataset has no school column.")
distribution = grade_distribution(data, school)
st.metric("Records in chart", distribution["row_count"])
st.bar_chart(
    pd.Series(distribution["grade_counts"], name="Course records").sort_index(),
    x_label="Final grade (grade points, 0–20)",
    y_label="Course records",
)
st.caption(
    "Each bar counts course records with one final grade. "
    f"The chart shows {distribution['row_count']} of {report['rows']} course records. "
    "Historical holdout scores above use the full dataset split and do not change with this chart filter."
)
st.subheader("School-level grade summaries")
if school_options:
    school_summary = school_grade_summary_table(data)
    st.dataframe(school_summary, hide_index=True)
    st.caption(
        "Historical Portuguese-course grades, listed by school name with sample sizes. "
        "Range is the highest minus the lowest final grade in each school. "
        "These summaries do not rank schools or show that a school caused a difference."
    )
    st.download_button(
        "Download school summary (CSV)",
        data=school_grade_summary_csv(school_summary),
        file_name="school_grade_summary.csv",
        mime="text/csv",
    )
else:
    st.caption("School summary unavailable because this dataset has no school column.")
st.subheader("Final-grade outlier inspection")
outliers = grade_outlier_summary(data)
flagged = outliers["counts"]["Below lower fence"] + outliers["counts"]["Above upper fence"]
st.metric("Records outside IQR fences", flagged)
st.bar_chart(
    pd.Series(outliers["counts"], name="Course records"),
    x_label="Grade category under 1.5×IQR rule",
    y_label="Course records",
)
st.caption(
    "Each bar counts grades below, within, or above the descriptive fences. "
    f"All {outliers['row_count']} Portuguese-course records are counted. "
    "Using the 1.5×IQR rule, "
    f"Q1 is {outliers['q1']:.1f}, Q3 is {outliers['q3']:.1f}, "
    f"and grades strictly below {outliers['lower_fence']:.1f} or above "
    f"{outliers['upper_fence']:.1f} are flagged."
)
st.caption(
    "These are descriptive flags, not data errors or reasons to remove records. "
    "The chart does not change model training or scores."
)
try:
    training_validation = evaluate_training_dataset(data)
    validation_table, holdout_table = comparison_tables(training_validation, report)
except (OSError, ValueError, KeyError) as error:
    st.error(f"Cannot compare model results: {error}")
    st.stop()

st.subheader("Training-validation comparison")
st.dataframe(validation_table, hide_index=True)
st.caption(
    f"All three benchmarks use the same {training_validation['score_summary']['fold_count']} "
    f"repeated folds within {training_validation['outer_training_count']} outer-training "
    "course records. Lower MAE and RMSE mean smaller errors. Fold spread is descriptive, "
    "not a confidence interval."
)
st.subheader("Historical holdout results")
st.dataframe(holdout_table, hide_index=True)
st.caption(
    f"These scores come from the separate {training_validation['reserved_holdout_count']}-record "
    "historical holdout already viewed on Day 1. No G2-copy holdout score is reported. "
    "This is not untouched external validation, and these scores should not select a model."
)
st.subheader("Training-only residual diagnostics")
diagnostics = training_validation["residual_diagnostics"]
residual_frame = pd.DataFrame(diagnostics["points"])
st.metric("Training residual points", diagnostics["row_count"])
residual_points = alt.Chart(residual_frame).mark_circle(size=45, opacity=0.55).encode(
    x=alt.X("predicted_grade:Q", title=diagnostics["x_label"]),
    y=alt.Y("residual_grade_points:Q", title=diagnostics["y_label"]),
)
zero_line = alt.Chart(pd.DataFrame({"zero": [diagnostics["zero_reference"]]})).mark_rule(
    color="#B44B41", strokeDash=[5, 4]
).encode(y="zero:Q")
st.altair_chart((residual_points + zero_line).properties(height=300), use_container_width=True)
st.caption(
    "Each point is one outer-training record predicted by a model that did not fit on "
    "that record (first validation repeat only). Residual is actual minus predicted; "
    "the dashed line marks zero. Reserved test rows are excluded. "
    "This is a historical model check, not a student-level decision tool."
)
st.subheader("What the model knows")
st.write("The linear model uses first- and second-period grades to estimate the final grade on a 0–20 scale. It is a late-year benchmark, not an early-warning model.")
st.dataframe(pd.DataFrame({"Feature": list(report["coefficients"]), "Coefficient": list(report["coefficients"].values())}), hide_index=True)
st.caption("Coefficients describe associations, not the effect of changing a grade.")
with st.expander("Evaluation details and limitations"):
    st.json(report)
st.download_button("Download evaluation report", data=json.dumps(report, indent=2), file_name="evaluation.json", mime="application/json")
st.markdown("Data: [Cortez (2008), UCI Student Performance](https://doi.org/10.24432/C5TG7T), CC BY 4.0. Portuguese course only; no joining across courses.")
