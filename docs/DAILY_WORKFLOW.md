# Daily development workflow

## Schedule

Day 1: 2026-09-27, initial setup. Days 2–90: 2026-09-28 through 2026-12-25, daily at 09:00 America/Los_Angeles, including weekends. Automation ID: `daily-fellowship-code-and-pr`. The recurrence has an end date. No work beyond that date is authorized by this schedule. Keep the local computer and desktop app running for the scheduled task.

## Each run

1. Check the date in America/Los_Angeles. Read the roadmap, recent progress logs, remote main state, and open PRs through the connected GitHub repository to prevent duplicate work.
2. Choose the next unfinished task in `docs/ROADMAP.md`, respecting prerequisites and its “Done when” result. Dates are planning slots, not reasons to repeat finished work. If delayed, prioritize prerequisites and public delivery; record revised next steps and deferred items without extending December 25.
3. Implement the change with GitHub repository branch and file tools. Add relevant tests and use GitHub Actions to run `python -m unittest discover -s tests -v`. Exercise the public UCI data path when the task requires it. Record failures as failures. Do not access the local checkout, project files, shell, or credentials.
4. Write `docs/progress/YYYY-MM-DD.md`: feature, rationale, files, exact validation, limitations, learning point, next step, and PR status. Do not fabricate human work hours.
5. Commit only project files. Exclude raw private source documents, credentials, local environments, downloaded raw data, and personal information.
6. Create a branch such as `fellowship/YYYY-MM-DD-short-feature`. Open a PR to the dedicated repository under `archverma24`. Do not push directly to the default branch for feature work. The user authorizes creating and squash-merging project PRs without daily confirmation. Never force-push.
7. Review the PR diff and fix actionable issues. Verify required checks and project CI pass on the latest head commit, then squash-merge into `main` using the expected head SHA. Never bypass branch protections, unresolved review requirements, failing checks, or conflicts. Fix blockers where possible; otherwise report them. Verify GitHub reports the PR merged and remote main points at the merge commit. Start the next feature from updated remote main. Same-day reruns reuse an open PR; if already merged, avoid duplicate work and use a new PR only for a necessary follow-up change.
8. If the GitHub connector cannot perform a needed write, report its exact error and the repository permissions needed. Do not use a local checkout, credentials, or another repository as a fallback.
9. Attach the PR and give three short points in everyday words: Added, Checked, Merged (verified PR link or blocker). At the start of the next planned PR, reconcile the roadmap status and progress log against verified previous merges so status bookkeeping does not require a separate PR. Include a concise factual weekly summary every seventh project day.
10. On Day 90, prepare a final handoff, account for open PRs, and disable the automation. Do not extend it.

## Publication target

Repository: https://github.com/archverma24/education-outcomes-lab. Default branch: `main`. The connected GitHub installation must have repository content and pull-request write permission for the scheduled workflow. Use the public UCI source for data; GitHub remains the sole source of truth for project files and PR state.

## Brief template

- Added: [what changed, in everyday words]
- Checked: [whether it worked and tests passed]
- Merged: [verified PR link, or a clear explanation if blocked]

Daily briefs may support a user's own professional journal. Do not automatically post them to LinkedIn or submit program reports.
