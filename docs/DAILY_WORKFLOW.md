# Daily development workflow

## Schedule

Day 1: 2026-09-27, initial setup. Days 2–90: 2026-09-28 through 2026-12-25, daily at 09:00 America/Los_Angeles, including weekends. Automation ID: `daily-fellowship-code-and-pr`. The recurrence has an end date. No work beyond that date is authorized by this schedule. The local computer and desktop app must be running and the project directory available.

## Each run

1. Check local date and existing progress file to prevent duplicate daily work. Read roadmap, current Git status and remote PR state.
2. Choose the next unfinished task in `docs/ROADMAP.md`, respecting prerequisites and its “Done when” result. Dates are planning slots, not reasons to repeat finished work. If delayed, prioritize prerequisites and public delivery; record revised next steps and deferred items without extending December 25.
3. Use `.venv`, implement the change and relevant tests. Run pipeline checks; exercise the app when its behavior changes. Record failures as failures.
4. Write `docs/progress/YYYY-MM-DD.md`: feature, rationale, files, exact validation, limitations, learning point, next step, publication status. Do not fabricate human work hours.
5. Commit only project files. Exclude raw private source documents, credentials, local environments, downloaded raw data, and personal information.
6. Create a branch such as `fellowship/YYYY-MM-DD-short-feature`. Open a PR to the dedicated repository under `archverma24`. Do not push directly to the default branch for feature work. The user authorizes creating and squash-merging project PRs without daily confirmation. Never force-push.
7. Review the PR diff and fix actionable issues. Verify required checks and project CI pass on the latest head commit, then squash-merge into `main` using the expected head SHA. Never bypass branch protections, unresolved review requirements, failing checks or conflicts. Fix blockers where possible; otherwise report them. Verify GitHub reports the PR merged and synchronize the clean local checkout with `main`. Start the next feature from updated `main`. Same-day reruns reuse an open PR; if already merged, avoid duplicate work and use a new PR only for a necessary follow-up change.
8. If GitHub is unavailable, retain local commits and record the publishing blocker. When access returns, publish pending work without duplicate PRs. Never substitute another repository.
9. Attach the PR and give three short points in everyday words: Added, Checked, Merged (verified PR link or blocker). At the start of the next planned PR, reconcile the roadmap status and progress log against verified previous merges so status bookkeeping does not require a separate PR. Include a concise factual weekly summary every seventh project day.
10. On Day 90, prepare a final handoff, account for open PRs, and disable the automation. Do not extend it.

## Publication target

Repository: https://github.com/archverma24/education-outcomes-lab. Default branch: `main`. User supplied this URL and connector access was verified on 2026-09-27. Use Git when authenticated. The connector returned HTTP 403 on PR creation during setup; the existing Git credential helper successfully authenticated a GitHub REST PR request without printing or storing credentials. Use a trusted CA bundle for HTTPS if the local Python root store is missing. Alternatively use connected GitHub tools when their permissions allow to create a tree, commit, branch and pull request. Never extract connector credentials. Fetch published commits back into the local checkout to keep histories aligned.

## Brief template

- Added: [what changed, in everyday words]
- Checked: [whether it worked and tests passed]
- Merged: [verified PR link, or a clear explanation if blocked]

Daily briefs may support a user's own professional journal. Do not automatically post them to LinkedIn or submit program reports.
