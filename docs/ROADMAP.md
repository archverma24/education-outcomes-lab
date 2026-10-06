# Education Outcomes Lab: 90-day task plan

**Dates:** September 27–December 25, 2026, inclusive. **Daily run:** 9:00 AM America/Los_Angeles, including weekends. Day 1 is already complete; the remaining entries are planned work, not completed features.

**Goal:** Deliver a small, understandable education analytics application with public-data validation, explainable models, automated quality checks, a publicly accessible URL, and a reproducible portfolio handoff.

## How to use this plan

- Each day delivers one small useful increment and the evidence in its “Done when” column. Keep Python, pandas, scikit-learn and Streamlit; no paid infrastructure, private student data, LLMs or Kubernetes.
- Follow the sequence because later tasks depend on earlier outputs. Review existing progress first; never repeat a completed task just because its calendar date arrives.
- If work is delayed, prioritize unfinished prerequisites and the public deliverable. Record the reason, revised next step and any deferred lower-priority item. Do not mark work done without evidence or extend the December 25 end date.
- Every implementation goes through a reviewed PR into `main`, passing latest-commit checks, then a squash merge. Mark a task complete only after its acceptance result is verified and its PR is merged. Record the PR and evidence in the dated progress log.
- Give three short daily points: **Added**, **Checked**, **Merged**. Include a short weekly summary on Days 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77 and 84, and a final handoff on Day 90.
- Review/release days prioritize useful fixes and verification. If no code change is warranted, report that honestly; do not manufacture a cosmetic PR.

## Evaluation rules

Use only the Portuguese-course dataset initially. G1 and G2 are predictors and G3 is the target. Keep a fixed final holdout separate; select models and settings using training-only validation. Day 1 holdout results are already visible, so disclose that historical exposure and never present the final result as a completely untouched external validation. Freeze the final candidate before Day 87 and do not tune after its final evaluation. The application demonstrates historical associations, not early intervention or decisions about real students.

## Milestones

| Days | Focus | Result |
| --- | --- | --- |
| Days 1–7 | Trusted data foundation | Source metadata, validation, integrity checks and a quality panel. |
| Days 8–14 | Understand the data | Useful aggregate charts and tested exports. |
| Days 15–21 | Evaluate fairly | Reproducible splits and validation-only comparisons. |
| Days 22–28 | Compare simple models | Linear, ridge and shallow-tree models with valid training pipelines. |
| Days 29–35 | Test model behavior | Leakage, input, prediction-range and small-group checks. |
| Days 36–42 | Make the dashboard easy to use | Clear navigation, explanations and accessibility checks. |
| Days 43–49 | Make runs reproducible | Locked dependencies, stable configuration and recovery behavior. |
| Days 50–56 | Prepare deployment | A tested package, free-host configuration and fallback report. |
| Days 57–63 | Deliver a public URL | A live dashboard or accessible static fallback, verified without sign-in. |
| Days 64–70 | Demonstrate monitoring | Synthetic distribution-change examples and tested quality rules. |
| Days 71–77 | Explain the work | Exported figures, model card, contract and repeatable walkthrough. |
| Days 78–84 | Improve reliability | Evidence-led fixes and fresh-install/public-link checks. |
| Days 85–90 | Finish and hand over | Final evaluation, portfolio summary, reproducible handoff and schedule stop. |

## Daily tasks

“Planned” means work remains. “Done” means verified and merged. All dates are in 2026.

### Foundation and provenance

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 01 | 2026-09-27 | Done | Initial pipeline, baseline and dashboard | The pipeline downloads and validates data, compares a linear model with a mean baseline, and renders the dashboard; source/license are documented and tests pass. Completed in PR #1. |
| 02 | 2026-09-28 | Done | Dataset provenance manifest | A versioned manifest records the source, license, course, retrieval time and file hash; generated metadata matches the downloaded file. Completed in PR #3. |
| 03 | 2026-09-29 | Done | Integrity check against a known source hash | A changed-byte fixture fails integrity verification with a clear message; the approved file passes without silently replacing its expected hash. Completed in PR #4. |
| 04 | 2026-09-30 | Done | Reusable dataset profile | A reusable function returns record counts, column types, missing counts and numeric summaries on both a known fixture and the real dataset. Completed in PR #5. |
| 05 | 2026-10-01 | Done | Duplicate-row audit without blind deletion | The report counts exact duplicate rows and explains that duplicate values do not prove duplicate students; source rows remain intact. Completed in PR #6. |
| 06 | 2026-10-02 | Done | Schema validation report export | The CLI exports a machine-readable validation report; invalid input returns a nonzero status and readable errors. Completed in PR #7. |
| 07 | 2026-10-03 | Done | Data-quality panel and first weekly review | The dashboard displays the quality report and sample counts; the first weekly summary links completed PRs and outstanding issues. Completed in PR #8. |

### Data exploration

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 08 | 2026-10-04 | Done | Grade-distribution filters | Users can filter the grade distribution by school; displayed record counts match the selected subset without retraining models. Completed in PR #9. |
| 09 | 2026-10-05 | Done | Missingness visualization | The dashboard shows missing-value counts; a synthetic missing-value fixture renders correctly even though the real data has no missing grades. Completed in PR #10. |
| 10 | 2026-10-06 | Planned | School-level aggregate comparison with sample sizes | School-level grade summaries show sample counts and avoid ranking schools or claiming differences are causal. |
| 11 | 2026-10-07 | Planned | Summary-statistics export | Users can download aggregate count, mean, median and spread; exported values match the displayed summary. |
| 12 | 2026-10-08 | Planned | Outlier inspection | A chart identifies unusually low or high grades using a stated descriptive rule; no rows are automatically removed. |
| 13 | 2026-10-09 | Planned | Chart captions and units | Every exploration chart has a descriptive title, labeled units and a sentence explaining what it shows. |
| 14 | 2026-10-10 | Planned | EDA regression checks | Fixture-based checks catch wrong filter counts, missingness totals and summary exports; the weekly review records results. |

### Evaluation quality

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 15 | 2026-10-11 | Planned | Reusable split configuration | A split configuration accepts a seed and test fraction, rejects invalid fractions, and reproduces the same partition. |
| 16 | 2026-10-12 | Planned | Train/test split manifest | A manifest records source hash and train/test row identifiers; tests verify no row appears in both partitions. |
| 17 | 2026-10-13 | Planned | Repeated cross-validation | Cross-validation runs only on the training partition with fixed seeds; fold scores and sample counts are exported. |
| 18 | 2026-10-14 | Planned | Uncertainty summaries | Reports show mean and spread of validation scores, labeled as fold variability rather than a confidence interval for real-world performance. |
| 19 | 2026-10-15 | Planned | Residual diagnostics | Out-of-fold training predictions produce residual plots with labeled axes and zero reference; the final holdout is not used to tune models. |
| 20 | 2026-10-16 | Planned | Simple grade-copy benchmark | A baseline predicts the final grade by copying G2; it uses the same validation partitions as other candidates. |
| 21 | 2026-10-17 | Planned | Evaluation comparison panel | A comparison view presents mean, G2-copy and linear baselines using identical validation metrics and clearly separated historical holdout results. |

### Interpretable modeling

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 22 | 2026-10-18 | Planned | Regularized linear baseline | Ridge regression is added as a candidate with scaling fit only inside training folds; it need not outperform the simpler model. |
| 23 | 2026-10-19 | Planned | Small decision-tree baseline | A shallow decision-tree candidate has a fixed seed and bounded depth; it is evaluated on the same validation folds. |
| 24 | 2026-10-20 | Planned | Training-only preprocessing pipeline | Preprocessing and estimation use a single fitted pipeline; a test confirms validation rows never fit preprocessing statistics. |
| 25 | 2026-10-21 | Planned | Hyperparameter selection on training folds | A small fixed search over ridge strength and tree depth uses training-only folds; chosen settings and selection metric are recorded. |
| 26 | 2026-10-22 | Planned | Permutation importance on validation data | Held-out training-fold permutation importance is shown with variability and an explanation that importance is not causation. |
| 27 | 2026-10-23 | Planned | Coefficient stability analysis | Standardized coefficients are compared across training folds; the report identifies instability without consulting the final holdout. |
| 28 | 2026-10-24 | Planned | Model comparison regression tests | Tests verify all candidates share splits, report the same metrics and keep the final target out of their input features. |

### Model QA

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 29 | 2026-10-25 | Planned | Target-leakage contract tests | Tests reject G3 or unapproved columns as predictor inputs and verify training/validation separation throughout selection. |
| 30 | 2026-10-26 | Planned | Grade-bound prediction diagnostics | Reports count predictions outside the 0–20 grade range; any clipping is explicitly labeled and evaluated separately. |
| 31 | 2026-10-27 | Planned | Missing-input behavior | Missing predictor values produce a clear validation error rather than an unexplained crash or silent guess. |
| 32 | 2026-10-28 | Planned | Out-of-range input errors | Negative, above-20, fractional and nonnumeric grade fixtures are rejected with field-specific messages. |
| 33 | 2026-10-29 | Planned | Feature-order invariance checks | Predictions are unchanged when incoming feature columns are reordered; missing or duplicated required columns fail clearly. |
| 34 | 2026-10-30 | Planned | Small-cohort reporting guard | Grouped summaries with fewer than 10 records are suppressed and explain the threshold; tests cover counts of 9 and 10. |
| 35 | 2026-10-31 | Planned | Model quality report export | A downloadable model-quality report combines validation scores, range checks, input rules and limitations. |

### Dashboard usability

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 36 | 2026-11-01 | Planned | Dataset overview navigation | The dashboard has clear Overview, Data quality and Model results sections with a predictable default view. |
| 37 | 2026-11-02 | Planned | Readable metrics glossary | MAE, RMSE, baseline, validation and holdout have short plain-language definitions next to the relevant results. |
| 38 | 2026-11-03 | Planned | Interactive residual views | Users can inspect validation residuals by model; chart counts agree with the out-of-fold prediction table. |
| 39 | 2026-11-04 | Planned | Model selector | A selector switches between evaluated models and updates metrics and explanations without using the holdout for model choice. |
| 40 | 2026-11-05 | Planned | Accessible chart palette | Charts use a color-vision-friendly palette plus labels or shapes; key series remain distinguishable without color alone. |
| 41 | 2026-11-06 | Planned | Keyboard-friendly controls | All interactive controls have readable labels and a logical keyboard order; a keyboard-only walkthrough reaches each action. |
| 42 | 2026-11-07 | Planned | Dashboard behavior tests | App tests cover navigation, model selection and expected empty/error states; no uncaught exceptions appear. |

### Reproducibility

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 43 | 2026-11-08 | Planned | Environment dependency lock | A tested Python dependency lock and supported Python version reproduce the app in a clean environment. |
| 44 | 2026-11-09 | Planned | Portable configuration file | One documented configuration controls data/report paths and split settings; invalid values fail before training. |
| 45 | 2026-11-10 | Planned | Dataset cache status | The dashboard distinguishes missing, valid and changed cached data using source hashes and a clear next action. |
| 46 | 2026-11-11 | Planned | Repeatable report filenames | Generated report names include a stable run identifier derived from data, configuration and model version; identical runs do not create ambiguous copies. |
| 47 | 2026-11-12 | Planned | CLI error-path coverage | CLI tests cover missing files, invalid data and unwritable output paths, with nonzero exit status and useful messages. |
| 48 | 2026-11-13 | Planned | Data-source failure recovery | Simulated network failure and malformed archives preserve the last valid local dataset and produce a clear recovery message. |
| 49 | 2026-11-14 | Planned | Reproduction smoke checks | A clean-environment command installs dependencies, obtains public data, runs tests and builds the report successfully. |

### Deployment preparation

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 50 | 2026-11-15 | Planned | Minimal container package | Create a minimal container build for the existing Python app, without Kubernetes; build it and keep data retrieval explicit. |
| 51 | 2026-11-16 | Planned | Clean-environment smoke run | The packaged app starts from a clean environment using documented commands and produces the expected baseline report. |
| 52 | 2026-11-17 | Planned | Deployment startup script | One startup command verifies required data, then starts the app; failed preparation exits with a useful message. |
| 53 | 2026-11-18 | Planned | Health-check behavior | The deployment exposes a lightweight health check; checks distinguish a running server from a successfully rendered dashboard. |
| 54 | 2026-11-19 | Planned | Static sample report fallback | A versioned aggregate sample report keeps the demo informative when fresh data is unavailable and clearly labels its source and age. |
| 55 | 2026-11-20 | Planned | Choose and configure free hosting | Select an available free hosting route, verify current limits, and commit its configuration; record any account/access dependency without purchasing a plan. |
| 56 | 2026-11-21 | Planned | Deployment readiness checks | A deployment checklist passes for reproducible startup, public-data attribution, absence of secrets and a working sample-report fallback. |

### Public delivery

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 57 | 2026-11-22 | Planned | Deploy free dashboard and verify URL | Publish the dashboard on the selected free host and verify its URL without sign-in; if hosting is blocked, deliver an accessible static report on free hosting instead. |
| 58 | 2026-11-23 | Planned | Public-page smoke test | An automated smoke check verifies the public page loads and contains the project title, data attribution and usable result content. |
| 59 | 2026-11-24 | Planned | Deployment failure diagnostics | Failed deployment or data-loading states show actionable diagnostics without exposing credentials or private paths. |
| 60 | 2026-11-25 | Planned | Mobile layout fixes | At phone and desktop widths, charts and controls remain readable without clipped content or overlapping labels. |
| 61 | 2026-11-26 | Planned | Accessible empty and error states | Missing data, empty selections and invalid configuration show readable status messages that remain usable with a keyboard. |
| 62 | 2026-11-27 | Planned | Source attribution in exports | All report downloads include dataset attribution, license link, evaluation method and relevant limitations. |
| 63 | 2026-11-28 | Planned | Public demo regression checks | The public demo passes its smoke check, core navigation and export checks; the weekly review records the verified URL. |

### Monitoring and robustness

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 64 | 2026-11-29 | Planned | Input distribution summary | An input summary records G1/G2 count, mean, spread and missing values against fixed grade bins. |
| 65 | 2026-11-30 | Planned | Reference distribution snapshot | A reference distribution is saved from the training partition with source hash, split identifier and schema version. |
| 66 | 2026-12-01 | Planned | Synthetic distribution-shift demo | Synthetic grade shifts exercise the monitor without altering the source data; the demo clearly labels fabricated examples. |
| 67 | 2026-12-02 | Planned | Shift visualization | A view compares reference and synthetic distributions with consistent bins, counts and plain-language interpretation. |
| 68 | 2026-12-03 | Planned | Model-quality threshold configuration | Configuration defines documented warning thresholds for missingness, distribution change and validation error; invalid thresholds are rejected. |
| 69 | 2026-12-04 | Planned | Quality-gate CLI status | A CLI quality check returns a documented nonzero status when a configured threshold fails and reports exactly which rule failed. |
| 70 | 2026-12-05 | Planned | Monitoring report tests | Tests cover unchanged distributions, known shifts, missing values and threshold boundaries; no real-population performance claim is made. |

### Portfolio explanation

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 71 | 2026-12-06 | Planned | Reproducible figures export | A command exports labeled aggregate figures with consistent titles, units, dataset attribution and reproducible filenames. |
| 72 | 2026-12-07 | Planned | Benchmark comparison export | The same comparison report exports to a readable table and JSON, using consistent model names, splits and metric values. |
| 73 | 2026-12-08 | Planned | Data-contract documentation generator | Generate a readable data-contract page from validation definitions; tests detect disagreement between documented and enforced grade rules. |
| 74 | 2026-12-09 | Planned | Model-card report generator | Generate a model card from run metadata covering intended use, inputs, validation, data limitations and excluded uses. |
| 75 | 2026-12-10 | Planned | Limitations panel refinements | The dashboard explains historical-data limits, late-year timing, uncertainty and lack of causal evidence beside results. |
| 76 | 2026-12-11 | Planned | Demo walkthrough fixtures | A small synthetic demo fixture demonstrates the main dashboard states and can be reset without touching source data. |
| 77 | 2026-12-12 | Planned | End-to-end walkthrough tests | An end-to-end check runs ingestion validation, analysis, reporting and the demo walkthrough in a clean test environment. |

### Polish and feedback

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 78 | 2026-12-13 | Planned | Resolve highest-value review feedback | Resolve the highest-impact outstanding defect or review request; if none exists, exercise malformed configuration and fix any reproducible failure rather than inventing a feature. |
| 79 | 2026-12-14 | Planned | Improve slowest measured path | Measure startup and report generation; optimize only a demonstrated bottleneck while preserving results, otherwise record the measured baseline. |
| 80 | 2026-12-15 | Planned | Cache invalidation tests | Tests prove changes to source data or configuration invalidate affected cached results and identical inputs reuse valid cache entries. |
| 81 | 2026-12-16 | Planned | Export content consistency checks | Tests compare dashboard, JSON and tabular exports for matching record counts, metrics and source identifiers. |
| 82 | 2026-12-17 | Planned | Version info in reports | Each report records project version, commit identifier when available, Python version and relevant dependency versions. |
| 83 | 2026-12-18 | Planned | Fresh-install regression checks | A fresh installation from the documented commands passes tests and reproduces the chosen benchmark within stated numeric tolerances. |
| 84 | 2026-12-19 | Planned | Deployment and docs link validation | Check README, dataset, license and public-demo links; repair broken links and record the date checked. |

### Handoff

| Day | Date | Status | Task | Done when |
| --- | --- | --- | --- | --- |
| 85 | 2026-12-20 | Planned | Resolve remaining material defects | Resolve remaining material defects; if none remain, run negative-path release checks and document that evidence without cosmetic code changes. |
| 86 | 2026-12-21 | Planned | Final public demo regression | Run the final public demo checks on desktop and mobile and verify exported reports and error states. |
| 87 | 2026-12-22 | Planned | Frozen-model final evaluation | Freeze model settings selected through training validation, then evaluate the selected model once on the reserved holdout and export results with limitations; do not retune based on this result. |
| 88 | 2026-12-23 | Planned | Generate final project summary | Generate a final plain-language summary with verified features, measured results, public URL and merged PR evidence; distinguish plans from completed work. |
| 89 | 2026-12-24 | Planned | Package reproducible handoff | Package reproducible run instructions, configuration, dependency lock, attribution and known limitations; another clean setup can follow them. |
| 90 | 2026-12-25 | Planned | Final verification, handoff and schedule stop | Verify the final release and public URL, account for unfinished work and open PRs, deliver the handoff, and disable the daily schedule; no filler changes or extension beyond December 25. |

## Completion checklist

- The public deliverable loads without sign-in; the repository alone does not meet this goal.
- A fresh setup reproduces the documented analysis, and the source/license are credited.
- Model comparisons use valid partitions, report limitations and make no unsupported production claims.
- Tests pass, daily PR outcomes are traceable, and open work is listed honestly.
- The final brief links the live deliverable, repository, model card and setup instructions.
- The automation ends on December 25, 2026; no follow-on period is assumed.
