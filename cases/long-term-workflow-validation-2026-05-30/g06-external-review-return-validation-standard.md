# G06 External Review Return Validation Standard

- standard_date: 2026-05-30
- gate: `G06 external_independent_reviewer`
- status: ready_to_validate_future_return
- validation_script: `../../scripts/validate_external_review_return.py`
- stale_after: 2026-06-30
- must_refresh_if: reviewer package fields change, scorecard dimensions change, G06 reviewer selection rubric changes, G01 method-source package changes, practice-falsification audit changes, methodology iteration trace audit changes, G05 source package changes, historical consensus exception changes, or G04 follow-through changes the assigned reviewer evidence

## Purpose

This standard defines how to validate a completed external reviewer return.

It does not clear G06 by itself. G06 clears only after an independent reviewer returns completed materials and the validation script exits 0.

## Required Inputs

The reviewer must return:

- completed `external-reviewer-scorecard.csv`
- completed `external-review-results-YYYY-MM-DD.md`
- completed `external-review-intake-checklist.csv`

The reviewer should use `g06-reviewer-selection-rubric.csv` to confirm that each required release decision is covered by an appropriate reviewer profile, scorecard dimension and evidence path before returning a release recommendation.

The reviewer should have reviewed `theme-selection-refresh-audit.csv` and may run `validate_recent_theme_selection.py` to challenge recent-theme freshness before scoring `theme_selection_freshness`.

The reviewer should also review `practice-falsification-audit.csv` and challenge whether methodology claims are backed by validated cases, explicit rejection tests, actionability deltas and source-gap consequences before scoring `practice_falsification`.

The reviewer should use `methodology-iteration-trace-audit.csv` to challenge whether workflow patches trace to case failure modes, concrete patch artifacts, validation commands and decision effects rather than document-only theory or vague memory.

The reviewer should use `multi-lens-coverage-audit.csv` to challenge whether consumer, product, economy, industry, company and valuation lenses are supported by case evidence rather than only described in the workflow.

## Validation Command

```bash
python3 scripts/validate_external_review_return.py \
  --scorecard path/to/completed-external-reviewer-scorecard.csv \
  --results path/to/external-review-results-YYYY-MM-DD.md \
  --intake path/to/completed-external-review-intake-checklist.csv \
  --assignment-tracker cases/long-term-workflow-validation-2026-05-30/g06-reviewer-assignment-tracker.csv \
  --independence-screen cases/long-term-workflow-validation-2026-05-30/g06-reviewer-independence-screen.csv
```

## Pass Conditions

The script requires:

- reviewer fields are not placeholders;
- review dates are concrete dates;
- results memo reviewer and review date match the completed scorecard;
- assignment tracker has the same assigned reviewer as the completed scorecard and is in a returned or validated state;
- independence screen `screen_05` and `screen_06` are `pass` or `accepted`;
- all required dimensions are scored;
- completed scorecard covers every decision in `g06-reviewer-selection-rubric.csv`;
- every rubric-linked scorecard dimension is scored at or above its `minimum_release_score`;
- every rubric-linked evidence path exists in the release workspace;
- scorecard `finding_severity` values are limited to `P0`, `P1`, `P2`, `P3` or `none`;
- P0 findings use `release_impact: blocker`;
- P1 findings use `release_impact: blocker` or `release_impact: caveat`;
- average score is at least 4;
- minimum score is at least 4;
- no P0 findings;
- every P1 has a required fix with explicit `owner:` and `fix:` markers;
- results memo Findings table P0/P1 rows match the scorecard summary counts;
- every P1 in the results memo Findings table has explicit `owner:` and `fix:` markers;
- reviewer independence is confirmed;
- results memo scorecard summary values match the completed scorecard;
- G01 method-source decision is `accept_basis` or `accept_with_caveats`;
- `theme_selection_freshness` is scored at or above release minimum;
- reviewer results memo reports `theme_selection_freshness` as `pass` or `accepted_with_caveats`;
- `practice_falsification` is scored at or above release minimum;
- reviewer results memo reports `practice_falsification` as `pass` or `accepted_with_caveats`;
- reviewer results memo addresses `methodology-iteration-trace-audit.csv` when judging whether method changes are case-grounded and not overfit;
- `g04_follow_through_readiness` and `g04_false_completion_control` are scored at or above release minimum;
- reviewer results memo reports `g04_follow_through_readiness` and `g04_false_completion_control` as `pass` or `accepted_with_caveats`;
- reviewer results memo addresses `g04-later-event-candidate-screen.csv`, `validate_g04_later_event_candidate_screen.py` and the `refresh_allowed: yes` pre-refresh boundary;
- G05 source decision is `accept_source` or `accept_with_caveats`;
- historical consensus exception decision is `accept_exception` or `accept_with_caveats`;
- release recommendation is `release_external` or `release_with_caveats`;
- intake checklist rows are `pass` or `accepted`.
- `methodology_iteration_traceability` is scored at or above release minimum;
- reviewer results memo reports `methodology_iteration_traceability` as `pass` or `accepted_with_caveats`;
- completed intake checklist contains all required intake requirements.

## Failure Conditions

G06 remains blocked if the return has:

- placeholder scorecard rows;
- results memo reviewer or review date does not match the completed scorecard;
- assignment tracker reviewer does not match the completed scorecard reviewer;
- assignment tracker is not in a returned or validated state;
- independence screen `screen_05` or `screen_06` is not `pass` or `accepted`;
- missing required scorecard dimensions;
- missing a rubric-linked scorecard dimension;
- any rubric-linked score below its `minimum_release_score`;
- missing a rubric-linked evidence path;
- invalid `finding_severity` value;
- P0 finding without blocker release impact;
- P1 finding without blocker or caveat release impact;
- average score below 4;
- any score below the release minimum;
- any P0 finding;
- P1 finding without explicit `owner:` and `fix:` markers in `required_fix`;
- results memo Findings table P0/P1 counts do not match the scorecard summary;
- results memo Findings table P1 row lacks explicit `owner:` and `fix:` markers;
- results memo scorecard summary values do not match the completed scorecard;
- `g04_follow_through_readiness` below release minimum;
- `g04_false_completion_control` below release minimum;
- missing or failed `g04_follow_through_readiness` result in the reviewer memo;
- missing or failed `g04_false_completion_control` result in the reviewer memo;
- `g01_method_source_decision: require_private_material`;
- `g01_method_source_decision: reject_basis`;
- missing or failed `theme_selection_freshness` result in the reviewer memo;
- missing or failed `practice_falsification` result in the reviewer memo;
- reviewer memo ignores `methodology-iteration-trace-audit.csv` while accepting methodology changes as case-grounded;
- missing or failed `methodology_iteration_traceability` result in the reviewer memo;
- `g05_source_decision: reject_source`;
- `historical_consensus_exception_decision: require_export`;
- `historical_consensus_exception_decision: reject_exception`;
- `release_recommendation: release_internal_only`;
- `release_recommendation: reject`;
- failed action-label reproducibility;
- incomplete intake checklist.
- missing required intake checklist requirements.

## Release Rule

Do not mark `G06` as complete unless:

1. the completed return files exist;
2. `scripts/validate_external_review_return.py` exits 0;
3. `scripts/validate_long_term_release.py` exits 0 after the gate tracker is updated.
