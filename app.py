"""Local dashboard; public hosting is a later project milestone."""
from pathlib import Path
import pandas as pd
import streamlit as st
from education_outcomes.data import load_data
from education_outcomes.model import evaluate

st.set_page_config(page_title="Education Outcomes Lab", page_icon="📊", layout="wide")
st.title("Education Outcomes Lab")
st.caption("Public-data learning project • Reproducible analytics • Model quality")
st.info("Historical Portuguese-school data. This demo does not assess current students or recommend decisions.")
path = Path(__file__).parent / "data/raw/student-por.csv"
if not path.exists():
    st.warning("Dataset not installed. Run: education-outcomes --download")
    st.stop()
try:
    data = load_data(path)
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
st.download_button("Download evaluation report", data=__import__("json").dumps(report, indent=2), file_name="evaluation.json", mime="application/json")
st.markdown("Data: [Cortez (2008), UCI Student Performance](https://doi.org/10.24432/C5TG7T), CC BY 4.0. Portuguese course only; no joining across courses.")
