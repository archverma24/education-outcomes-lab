# Education Outcomes Lab

An education analytics and model-quality portfolio project for a Data Science fellowship. It explores public student-performance data and demonstrates reproducible modeling, data validation, and automated QA.

## Why this project

The fellowship letter emphasizes predictive analytics, interpretable models, and educational social impact. The professional-development guidance requires new skills and an end-to-end publicly accessible deliverable. This project adds practical machine-learning evaluation to an existing Python and QA background without repeating an interview-preparation app or database project.

**Initial question:** How accurately can first- and second-period grades predict final grades in a historical dataset, compared with a simple average-grade baseline?

This is a learning and model-quality demonstration, not a tool for determining real students' eligibility, access, or support. It is not a validated Chicago student model. The baseline uses grades available late in the year and must not be marketed as an early-warning system.

## Run locally

Python 3.10+ required; CI runs Python 3.11.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[app]'
education-outcomes --download
python -m unittest discover -s tests -v
streamlit run app.py
```

The explicit download command retrieves the public UCI data and creates `reports/baseline.json` and `reports/provenance.json`. The versioned provenance manifest records the UCI source, CC BY 4.0 license, Portuguese course, retrieval time in UTC, and SHA-256 of the downloaded CSV. Once downloaded, analysis works offline. Raw data and generated reports are excluded from Git. The benchmark report also includes aggregate row counts, column types, missing-value counts, and numeric summaries.

For a checksum obtained from a trusted source, add `--expected-sha256 YOUR_64_CHARACTER_SHA256`. A mismatch stops analysis, and a rejected download does not replace an existing data file. The expected checksum is never silently changed.

## Implemented

- Named-file download from the public UCI archive, including its nested ZIP.
- Required-column, numeric-type, integer-grade, range, and missing-value checks.
- Optional SHA-256 verification against an explicitly supplied trusted checksum.
- Reusable dataset profile with counts, types, missing values and numeric summaries.
- Fixed train/test split; linear regression vs. a training-only mean baseline.
- MAE/RMSE, model coefficients, source URL and source-file SHA-256 in the CLI report.
- Versioned data provenance manifest with attribution, UTC retrieval time, and a hash tied to the downloaded file.
- Streamlit dashboard with grade distribution, model metrics, coefficients and report export.
- Pipeline unit tests and a GitHub Actions workflow.

The first 649-row run used 519 training and 130 test records. Holdout MAE was 0.733 grade points for linear regression and 2.395 for the mean baseline. These are exploratory results on one split, not evidence of generalization to a new population.

## Data and attribution

Cortez, P. (2008). *Student Performance*. UCI Machine Learning Repository. https://doi.org/10.24432/C5TG7T. License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Use only `student-por.csv` initially. Math and Portuguese course records can overlap; do not concatenate them as independent students. The model uses only G1 and G2 as features and G3 as the target. No demographic, health, family, or alcohol-use attributes are model inputs.

See [project proposal](docs/PROJECT_PROPOSAL.md), [90-day roadmap](docs/ROADMAP.md), [daily workflow](docs/DAILY_WORKFLOW.md), and [progress](docs/progress/2026-09-27.md).

## Delivery status

Local implementation exists. A public hosted dashboard is a planned milestone, not yet deployed. Repository: https://github.com/archverma24/education-outcomes-lab. Feature work is delivered through reviewable pull requests. Daily automation is scheduled in the project chat at 09:00 America/Los_Angeles through 2026-12-25. Keep the computer on and the desktop app running for local scheduled work.
