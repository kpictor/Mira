# Blind Review Assignment

- assignment_type: external_reviewer_dry_run
- prepared_date: 2026-05-30
- status: ready_to_assign

## Instructions To Sender

Send the reviewer only:

- `README.md`
- `workflow.md`
- `fill-guide.md`
- `template-inventory.md`
- `source-appendix.md`
- `analyst-checklist.csv`
- `external-reviewer-brief.md`
- `external-reviewer-scorecard.csv`
- `external-review-results-template.md`
- `external-review-intake-checklist.csv`
- assigned case folder
- `../g05-fy2-fcf-source-upgrade-2026-05-30.md` if reviewer is assigned G05
- `../g05-crm-unavailable-data-exception-review.md` if reviewer is assigned G05 fallback
- `../g05-crm-source-attempts.csv` if reviewer is assigned G05
- `../g01-external-method-source-audit.csv` if reviewer is assigned G01
- `../g01-external-method-source-upgrade-2026-05-30.md` if reviewer is assigned G01
- `../follow-through-trigger-tracker.csv` if reviewer is assigned G04
- `../g04-follow-through-event-watch-calendar.csv` if reviewer is assigned G04
- `../g04-later-event-candidate-screen.csv` if reviewer is assigned G04
- `../g04-follow-through-execution-tracker.csv` if reviewer is assigned G04
- `../g04-follow-through-handoff-2026-05-30.md` if reviewer is assigned G04
- `../../../scripts/validate_g04_later_event_candidate_screen.py` if reviewer is assigned G04

Do not send:

- chat transcript
- methodology development notes
- review-log history
- answers from the original analyst

## Recommended Assignments

### Reviewer 1: Fresh Healthcare Product Case

Folder:

- `../../lly-2026-05-glp1-workflow-dry-run/`

Question:

- Can the reviewer reproduce `watch_only_pending_expectation_map_and_realized_price_refresh`?

Pass condition:

- Reviewer identifies payer/access, realized price and valuation as the correct blockers.

### Reviewer 2: Hot Theme Handoff

Folder:

- `../../humanoid-robotics-2026-05-value-capture-screen/`

Question:

- Can the reviewer reproduce `industry_map_first`?

Pass condition:

- Reviewer agrees that public-company value capture is not yet direct, material and measurable.

### Reviewer 3: Historical Failure Backtest

Folder:

- `../../pton-2020-2022-failure-backtest/`

Question:

- Would the workflow have downgraded before FY2022 collapse?

Pass condition:

- Reviewer identifies normalized hardware demand, hardware gross margin and inventory commitment as pre-collapse blockers.

### Reviewer 4: G05 CRM Source Challenge

Files:

- `../g05-fy2-fcf-source-upgrade-2026-05-30.md`
- `../g05-crm-unavailable-data-exception-review.md`
- `../g05-crm-source-attempts.csv`
- `../../crm-2026-05-product-workflow-trial/expectation-map.csv`
- `../../crm-2026-05-product-workflow-trial/evidence-log.csv`

Question:

- Is MarketScreener FY2028 FCF forecast sufficient to keep G05 cleared, given current false-precision controls?

Pass condition:

- Reviewer returns `accept_source` or `accept_with_caveats` and states exact caveats for external release.

### G01 Method-Source Basis

Use:

- `../g01-external-method-source-audit.csv`
- `../g01-external-method-source-upgrade-2026-05-30.md`

Question:

- Is the public institutional plus Asian/Chinese practitioner method-source basis sufficient for external release, given the private buyside execution-detail caveat?

Pass condition:

- Reviewer returns `accept_basis` or `accept_with_caveats` and states exact caveats for external release.

### Reviewer 5: G04 Follow-Through Readiness

Files:

- `../follow-through-trigger-tracker.csv`
- `../g04-follow-through-event-watch-calendar.csv`
- `../g04-later-event-candidate-screen.csv`
- `../g04-follow-through-execution-tracker.csv`
- `../g04-follow-through-handoff-2026-05-30.md`
- `../../../scripts/validate_g04_later_event_candidate_screen.py`

Question:

- Are the future-event trigger, event-watch calendar, later-event candidate screen, execution tracker and clearing rule specific enough to execute later without treating readiness as completed G04 evidence?

Pass condition:

- Reviewer returns `pass` or `accepted_with_caveats` for both `g04_follow_through_readiness` and `g04_false_completion_control`, and confirms that G04 remains blocked until a real later-event refresh validates after `validate_g04_later_event_candidate_screen.py` passes with `refresh_allowed: yes`.

## Release Decision Rule

The workflow cannot be externally shared as final public-grade unless:

- at least one external reviewer returns no P0 findings
- no reviewer rejects the core action label because of unsupported evidence
- any P1 finding has a named owner and fix
- reviewer accepts the G01 public method-source basis or accepts it with caveats
- reviewer accepts G04 follow-through readiness and false-completion controls without treating readiness as completed evidence
- reviewer accepts either a complete expectation map or the unavailable-data exception protocol

## Result Logging

After review, create:

- `external-review-results-YYYY-MM-DD.md`
- completed `external-reviewer-scorecard.csv`
- completed `external-review-intake-checklist.csv`

Do not overwrite the blank scorecard template.
