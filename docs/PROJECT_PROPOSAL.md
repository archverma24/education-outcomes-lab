# Project proposal: Education Outcomes Lab

## Deliverable

A public dashboard and reproducible Python pipeline exploring education data, comparing explainable models, and showing data/model-quality evidence. First scope: predict final grades from earlier grades using the small UCI Student Performance Portuguese-course dataset. The application explains evaluation and limitations rather than making decisions about real students.

## Fit and manageable scope

This develops predictive modeling, data collection, analysis, communication, automated validation, and CI/CD. A linear model and a simple tree are sufficient; cloud-native deployment can be learned with one small hosting target. Kubernetes, multiple clouds, LLM fine-tuning and agent orchestration are not needed for the MVP. The offer letter lists several responsibility areas, not a requirement to put every technology into one project.

Existing resume projects cover interview preparation, a Django review app, SQL infrastructure analysis and booking workflows. This project adds ML evaluation and data/model QA, making it distinct while connecting with QA career interests. No claim is made that a particular technology guarantees hiring demand.

## Source-document interpretation

The offer letter describes a Data Science Fellow role from September 21, 2026 through July 12, 2027 with approximately 21–25 hours per week, remote and flexible. The requested automation is only a 90-day project window within that broader period; it does not track or certify those hours.

The guidance requires a novel role-relevant portfolio project, a public live URL, daily professional journaling, and weekly accountability. It describes collaborative project scoping with the supervisor. This is a proposal and working prototype; supervisor acceptance has not been obtained or represented. A repository is not the final public deliverable.

The guidance also includes networking, LinkedIn posting, reporting forms, and weekday-work preferences. Those remain document context. The user requested daily coding, PRs and briefs; no social posting, outreach or form submission is authorized by the documents. The user's daily cadence takes precedence for this automation.

## Stack

Python, pandas, scikit-learn, Streamlit, unittest, GitHub Actions. Add Docker and one free hosting route only if they improve deployment. Avoid authentication, private data collection, paid APIs, and infrastructure beyond the project needs.

## Success criteria

1. Reproducible ingestion with source and license documentation.
2. Clear data contract and useful quality failures.
3. Valid train/test evaluation against a simple baseline, with uncertainty and leakage checks.
4. A usable accessible dashboard with aggregate visualizations and model explanations.
5. Passing checks and small reviewable PRs.
6. A verified public URL and concise portfolio write-up.

## Scope limits

Historical Portuguese school data is not representative of today's Chicago students. Coefficients are associations, not causal effects. Grade prediction does not establish the efficacy of an intervention. Use synthetic data for input demos and avoid collecting identifiable student data. Prefer a small trustworthy demonstration over claims of production-grade risk intelligence.
