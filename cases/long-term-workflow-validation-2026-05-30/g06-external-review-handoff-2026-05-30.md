# G06 External Review Handoff

- handoff_date: 2026-05-30
- gate: `G06 external_independent_reviewer`
- status: ready_to_assign_not_completed
- release_impact: not_cleared

## Purpose

G06 requires an independent reviewer to test whether the workflow can be reproduced and challenged without the original research author explaining it live.

This handoff defines what is ready, what the reviewer must return and what counts as a valid G06 clearing event.

## Ready To Send

Public workflow pack:

- `public-workflow-pack/README.md`
- `public-workflow-pack/workflow.md`
- `public-workflow-pack/fill-guide.md`
- `public-workflow-pack/template-inventory.md`
- `public-workflow-pack/source-appendix.md`
- `public-workflow-pack/analyst-checklist.csv`
- `public-workflow-pack/external-reviewer-brief.md`
- `public-workflow-pack/external-reviewer-scorecard.csv`
- `public-workflow-pack/blind-review-assignment.md`
- `public-workflow-pack/external-review-results-template.md`
- `public-workflow-pack/external-review-intake-checklist.csv`

Assigned evidence packets:

- `../lly-2026-05-glp1-workflow-dry-run/`
- `../humanoid-robotics-2026-05-value-capture-screen/`
- `../pton-2020-2022-failure-backtest/`
- `../crm-2026-05-product-workflow-trial/`
- `trial-theme-matrix.csv`
- `theme-selection-refresh-audit.csv`
- `g06-reviewer-selection-rubric.csv`
- `practice-falsification-audit.csv`
- `methodology-iteration-trace-audit.csv`
- `multi-lens-coverage-audit.csv`
- `../scripts/validate_recent_theme_selection.py`
- `g01-external-method-source-audit.csv`
- `g01-external-method-source-upgrade-2026-05-30.md`
- `follow-through-trigger-tracker.csv`
- `g04-follow-through-event-watch-calendar.csv`
- `g04-later-event-candidate-screen.csv`
- `g04-follow-through-execution-tracker.csv`
- `g04-follow-through-handoff-2026-05-30.md`
- `../../scripts/validate_g04_later_event_candidate_screen.py`
- `g05-fy2-fcf-source-upgrade-2026-05-30.md`
- `g05-crm-source-attempts.csv`
- `historical-consensus-source-attempts.csv`
- `historical-consensus-unavailable-data-exception-2026-05-30.md`

## Required Reviewer Return

Reviewer must return:

1. completed scorecard based on `public-workflow-pack/external-reviewer-scorecard.csv`;
2. external review memo based on `public-workflow-pack/external-review-results-template.md`;
3. P0/P1 blocker list;
4. `g01_method_source_decision` for public method-source sufficiency;
5. `theme_selection_freshness` result for recent-theme selection and refresh discipline;
6. `practice_falsification` result for case-grounded methodology claims;
7. `methodology_iteration_traceability` result for whether `methodology-iteration-trace-audit.csv` proves patches came from case failures rather than vague theory;
8. `g04_follow_through_readiness` and `g04_false_completion_control` scores;
9. G05 source decision for MarketScreener FY2028 FCF forecast;
10. `historical_consensus_exception_decision` for TDOC/PTON;
11. release recommendation.

## Return Validation

After the reviewer returns completed files, run:

```bash
python3 ../../scripts/validate_external_review_return.py \
  --scorecard path/to/completed-external-reviewer-scorecard.csv \
  --results path/to/external-review-results-YYYY-MM-DD.md \
  --intake path/to/completed-external-review-intake-checklist.csv \
  --assignment-tracker g06-reviewer-assignment-tracker.csv \
  --independence-screen g06-reviewer-independence-screen.csv
```

See:

- `g06-external-review-return-validation-standard.md`

This command must exit 0 before G06 can be marked complete.

## G06 Clearing Rule

G06 can clear only if:

- reviewer independence is confirmed;
- assigned reviewer in `g06-reviewer-assignment-tracker.csv` matches the completed scorecard reviewer;
- reviewer assignment is in a returned or validated state;
- `g06-reviewer-independence-screen.csv` rows `screen_05` and `screen_06` are `pass` or `accepted`;
- scorecard has no placeholder rows;
- results memo reviewer and review date match the completed scorecard;
- no P0 finding is returned;
- average score is at least 4;
- every P1 has a named owner and fix, recorded with `owner:` and `fix:` markers in `required_fix`;
- results memo scorecard summary values match the completed scorecard;
- G01 method-source decision is `accept_basis` or `accept_with_caveats`;
- `theme_selection_freshness` meets release minimum score and is reported as `pass` or `accepted_with_caveats`;
- `practice_falsification` meets release minimum score and is reported as `pass` or `accepted_with_caveats`;
- `methodology_iteration_traceability` meets release minimum score and is reported as `pass` or `accepted_with_caveats`;
- external review memo challenges `methodology-iteration-trace-audit.csv` and does not identify ungrounded or overfit method patches;
- `g04_follow_through_readiness` and `g04_false_completion_control` meet release minimum score;
- external review memo reports `g04_follow_through_readiness` and `g04_false_completion_control` as `pass` or `accepted_with_caveats`;
- external review memo confirms the later-event candidate screen and `validate_g04_later_event_candidate_screen.py` prevent a refresh before `refresh_allowed: yes`;
- completed intake checklist contains all required intake requirements;
- G05 source decision is `accept_source` or `accept_with_caveats`;
- historical consensus exception decision is `accept_exception` or `accept_with_caveats`;
- release recommendation is `release_external` or `release_with_caveats`.

If the reviewer returns `release_internal_only`, `reject`, any P0, `require_private_material` / `reject_basis` for G01, `reject_source` for G05, or `require_export` / `reject_exception` for the historical consensus exception, G06 remains blocked.

## Current Status

The handoff is ready to assign.

G06 is not cleared because no independent reviewer has returned a scorecard or memo.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: reviewer returns findings, G04 follow-through refresh completes, G01 method-source basis is challenged, practice-falsification evidence changes, G05 source is challenged, historical consensus exception changes, or assigned case files change.
