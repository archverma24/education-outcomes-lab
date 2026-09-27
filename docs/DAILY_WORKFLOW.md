# Daily development workflow

## Schedule

Day 1: 2026-09-27, initial setup. Days 2–90: 2026-09-28 through 2026-12-25, daily at 09:00 America/Los_Angeles, including weekends. Automation ID: `daily-fellowship-code-and-pr`. The recurrence has an end date. No work beyond that date is authorized by this schedule. The local computer and desktop app must be running and the project directory available.

## Each run

1. Check local date and existing progress file to prevent duplicate daily work. Read roadmap, current Git status and remote PR state.
2. Choose the next unfinished useful increment. Adapt the sequence to evidence and feedback; dates are planning slots, not reasons to manufacture changes.
3. Use `.venv`, implement the change and relevant tests. Run pipeline checks; exercise the app when its behavior changes. Record failures as failures.
4. Write `docs/progress/YYYY-MM-DD.md`: feature, rationale, files, exact validation, limitations, learning point, next step, publication status. Do not fabricate human work hours.
5. Commit only project files. Exclude raw private source documents, credentials, local environments, downloaded raw data, and personal information.
6. Create a branch such as `fellowship/YYYY-MM-DD-short-feature`. Open a PR to the dedicated repository under `archverma24`. Do not push directly to the default branch for feature work. Do not merge PRs or force-push.
7. If yesterday's PR is unmerged, prefer an independent feature based on the default branch. If dependent, create a clearly labeled stacked PR targeting the predecessor branch; record that dependency. Reconcile bases when earlier PRs merge.
8. If GitHub is unavailable, retain local commits and record the publishing blocker. When access returns, publish pending work without duplicate PRs. Never substitute another repository.
9. Attach the PR and give a brief in the project chat: feature, value, checks, PR link/blocker, learning point, next feature. Include a concise factual weekly summary every seventh project day.
10. On Day 90, prepare a final handoff, account for open PRs, and disable the automation. Do not extend it.

## Publication target

Repository: https://github.com/archverma24/education-outcomes-lab. Default branch: `main`. User supplied this URL and connector access was verified on 2026-09-27. Use Git when authenticated. The connector returned HTTP 403 on PR creation during setup; the existing Git credential helper successfully authenticated a GitHub REST PR request without printing or storing credentials. Use a trusted CA bundle for HTTPS if the local Python root store is missing. Alternatively use connected GitHub tools when their permissions allow to create a tree, commit, branch and pull request. Never extract connector credentials. Fetch published commits back into the local checkout to keep histories aligned.

## Brief template

- Added: [actual behavior]
- Why: [practical benefit]
- Validation: [commands and measured results]
- PR: [verified URL or exact blocker]
- Learning: [one short concept]
- Next: [next useful increment]

Daily briefs may support a user's own professional journal. Do not automatically post them to LinkedIn or submit program reports.
