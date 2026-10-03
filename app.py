"""Local dashboard; public hosting is a later project milestone."""
from hashlib import sha256
import json
from pathlib import Path

import pandas as pd
import streamlit as st

from education_outcomes.data import schema_validation_report
from education_outcomes.model import evaluate
from education_outcomes.profile import profile_dataset

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

if validation["issues"]:
    st.error("Cannot analyze dataset: " + "; ".join(issue["message"] for issue in validation["issues"]))
    st.stop()

try:
    report = evaluate(data)
except (OSError, ValueError) as error:
    st.error(f"Cannot analyze dataset: {error}")
    st.stop()
a, b, c = st.columns(3)
a.metric("Course records", report["rows"])
b.metric("Model MAE (grade points)", f'{report["linear_regression"]["mae"]:.2f}')
c.metric("Mean baseline MAE", f'{report["mean_baseline"]["mae"]:.2f}')
st.subheader("Final-grade distribution")
st.bar_chart(data["G3"].value_counts().sort_index().rename("Records"))
st.subheader("What the model knows")
st.write("The linear model uses first- and second-period grades to estimate the final grade on a 0–20 scale. It is a late-year benchmark, not an early-warning model.")
st.dataframe(pd.DataFrame({"Feature": list(report["coefficients"]), "Coefficient": list(report["coefficients"].values())}), hide_index=True)
st.caption("Coefficients describe associations, not the effect of changing a grade.")
with st.expander("Evaluation details and limitations"):
    st.json(report)
st.download_button("Download evaluation report", data=json.dumps(report, indent=2), file_name="evaluation.json", mime="application/json")
st.markdown("Data: [Cortez (2008), UCI Student Performance](https://doi.org/10.24432/C5TG7T), CC BY 4.0. Portuguese course only; no joining across courses.")
