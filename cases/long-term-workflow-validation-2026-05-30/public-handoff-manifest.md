# Public Handoff Manifest

- prepared_date: 2026-05-30
- package_status: internal_candidate_ready_for_external_review
- final_external_release: no

## Send To External Reviewer

Send these files first:

- `public-workflow-pack/README.md`
- `public-workflow-pack/workflow.md`
- `public-workflow-pack/fill-guide.md`
- `public-workflow-pack/template-inventory.md`
- `public-workflow-pack/source-appendix.md`
- `public-workflow-pack/analyst-checklist.csv`
- `public-workflow-pack/external-reviewer-brief.md`
- `public-workflow-pack/external-review-request.md`
- `public-workflow-pack/external-reviewer-scorecard.csv`
- `public-workflow-pack/blind-review-assignment.md`
- `public-workflow-pack/external-review-results-template.md`
- `public-workflow-pack/external-review-intake-checklist.csv`
- `g05-fy2-fcf-source-upgrade-2026-05-30.md`
- `g05-crm-source-attempts.csv`
- `external-reviewer-bundle-manifest.csv`

Send one assigned case folder:

- `../lly-2026-05-glp1-workflow-dry-run/`
- or `../humanoid-robotics-2026-05-value-capture-screen/`
- or `../pton-2020-2022-failure-backtest/`

## Keep Internal Unless Requested

- `public-readiness-audit.md`
- `public-release-gate-tracker.csv`
- `public-release-decision.md`
- `ordinary-vs-workflow-comparison.md`
- `expectation-map-data-availability-audit.md`
- `historical-source-cleanup-2026-05-30.md`
- internal methodology review logs

## Reviewer Return Package

Expected return:

- completed `external-reviewer-scorecard.csv`
- completed `external-review-results-YYYY-MM-DD.md`
- completed `external-review-intake-checklist.csv`
- P0/P1 blocker list
- release recommendation
- specific edit suggestions

Validate the return with:

- `../../scripts/validate_external_review_return.py`
- `g06-external-review-return-validation-standard.md`

## Future Institutional Colleague Release

After G04 and G06 clear, prepare the colleague release from:

- `institutional-release-bundle-manifest.csv`
- `public-workflow-pack/institutional-colleague-release-notes-template.md`
- `public-workflow-pack/institutional-colleague-acceptance-memo-template.md`
- `public-workflow-pack/institutional-use-boundaries.md`
- `public-workflow-pack/institutional-adoption-faq.md`
- `final-release-cutover-checklist.csv`
- dated external go/no-go memo

Do not send the institutional release bundle as final methodology while `public-release-decision.md` remains `release_status: not_ready_external_release`.

## Release Owner Checklist

Before external release:

- confirm no P0 findings
- resolve or explicitly accept P1 findings
- complete one true follow-through refresh
- validate the completed follow-through refresh with `../../scripts/validate_follow_through_refresh.py`
- confirm reviewer accepts or caveats `theme_selection_freshness`
- confirm reviewer accepts or caveats CRM G05 source package
- confirm reviewer accepts or caveats the TDOC/PTON historical consensus unavailable-data exception
- complete the institutional release bundle manifest and preserve use-boundary caveats
- update `public-readiness-audit.md`
- update `public-release-decision.md`
- run `../../scripts/run_long_term_release_checks.py`

## Current Blockers

- true follow-through refresh not completed
- external reviewer not completed

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: reviewer assignment changes, new case folder is selected, release gates change, or external reviewer returns findings.
