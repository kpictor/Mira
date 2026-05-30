# External Reviewer Brief

- pack: `long-term-integrated-thesis`
- review_type: external_independent_reviewer_dry_run
- prepared_date: 2026-05-30
- status: ready_to_run_not_completed

## Purpose

This review tests whether an institutional analyst can use the workflow pack without the original research author explaining it live.

The reviewer should answer:

1. Can you reproduce the workflow's conclusion from the supplied files?
2. Can you identify the weakest lens and biggest source gap?
3. Does the workflow change actionability versus an ordinary memo?
4. Are the stop rules specific enough to challenge or refresh later?
5. Would you allow this workflow to be shared with other analysts?

## Reviewer Independence Rule

The reviewer should not read:

- internal chat history
- unpublished reasoning notes
- case files outside the assigned review set unless requested by the brief

The reviewer may use:

- public sources
- company filings
- the public workflow pack
- the assigned case artifacts
- `../g06-reviewer-selection-rubric.csv`

## Assigned Review Tasks

### Task A: Fresh Case Reproduction

Use only the public workflow pack and one assigned case.

Recommended case:

- `../../lly-2026-05-glp1-workflow-dry-run/`

Expected reviewer output:

- reproduce or challenge the action label
- identify whether payer/access and realized-price evidence are sufficient
- state whether the unavailable-data exception is acceptable

### Task B: Hot Theme Handoff Challenge

Use:

- `../../humanoid-robotics-2026-05-value-capture-screen/`

Expected reviewer output:

- decide whether `industry_map_first` is justified
- identify one public company that could be promoted to full single-equity research
- state what evidence would be required before actionability

### Task C: Recent Theme Selection Freshness Challenge

Use:

- `../trial-theme-matrix.csv`
- `../theme-selection-refresh-audit.csv`
- `../../../scripts/validate_recent_theme_selection.py`

Expected reviewer output:

- decide whether the seven selected hot directions are current enough for the stated market scope
- score `theme_selection_freshness`
- challenge whether hotness source IDs, stale_after dates, refresh triggers and drop/replace rules are specific enough for another analyst to maintain the theme list
- list exact replacements or monitoring fixes if the theme set is stale, too narrow or too narrative-driven

### Task D: Practice Falsification Challenge

Use:

- `../practice-falsification-audit.csv`
- `../methodology-iteration-trace-audit.csv`
- `../multi-lens-coverage-audit.csv`

Expected reviewer output:

- decide whether methodology claims are backed by validated cases rather than theory-only assertions
- score `practice_falsification`
- challenge whether each claim has a concrete rejection test, actionability delta and source-gap consequence
- challenge whether each methodology patch traces to a case failure mode, patch artifact, validator and decision effect rather than vague memory or overfit theory
- challenge whether consumer/product/economy/industry/company/valuation coverage is case-grounded
- list exact claims that should be downgraded, removed or kept internal-only

### Task E: Historical Failure Backtest Challenge

Use one of:

- `../../tdoc-2020-2022-failure-backtest/`
- `../../pton-2020-2022-failure-backtest/`

Expected reviewer output:

- decide whether the workflow would have downgraded before the visible collapse
- check whether valuation reconstruction is sufficient for external sharing
- identify missing consensus, source-archive evidence or transcript licensing issues
- set `historical_consensus_exception_decision` to `accept_exception`, `accept_with_caveats`, `require_export` or `reject_exception`

### Task F: G05 CRM Source-Sufficiency Challenge

Use:

- `../g05-fy2-fcf-source-upgrade-2026-05-30.md`
- `../g05-crm-unavailable-data-exception-review.md`
- `../g05-crm-source-attempts.csv`
- `../../crm-2026-05-product-workflow-trial/expectation-map.csv`
- `../../crm-2026-05-product-workflow-trial/evidence-log.csv`

Expected reviewer output:

- decide whether MarketScreener FY2028 FCF forecast is sufficient for G05
- choose `accept_source`, `accept_with_caveats` or `reject_source`
- state whether G05 should remain cleared for external-release purposes
- list exact fixes if the source is rejected

### Task F: G01 Method-Source Sufficiency Challenge

Use:

- `../g01-external-method-source-audit.csv`
- `../g01-external-method-source-upgrade-2026-05-30.md`
- `source-appendix.md`

Expected reviewer output:

- decide whether public institutional and Asian/Chinese practitioner sources are enough as a method-source basis
- choose `accept_basis`, `accept_with_caveats`, `require_private_material` or `reject_basis`
- record the result as `g01_method_source_decision`
- state whether private buyside execution-detail opacity is adequately caveated
- list exact fixes if more source work is required before external release

### Task G: G04 Follow-Through Readiness Challenge

Use:

- `../follow-through-trigger-tracker.csv`
- `../g04-follow-through-event-watch-calendar.csv`
- `../g04-later-event-candidate-screen.csv`
- `../g04-follow-through-execution-tracker.csv`
- `../g04-follow-through-handoff-2026-05-30.md`
- `../../../scripts/validate_g04_later_event_candidate_screen.py`

Expected reviewer output:

- decide whether the future follow-through trigger process is specific enough to execute
- score `g04_follow_through_readiness`
- score `g04_false_completion_control`
- confirm that event monitoring, scheduled future events, candidate-screen rows without `refresh_allowed: yes` and packet exports are not treated as completed G04 evidence
- confirm that the analyst must run `validate_g04_later_event_candidate_screen.py` before drafting a follow-through refresh
- list exact fixes if G04 readiness is not reviewable

## Scoring

Complete:

- `external-reviewer-scorecard.csv`

Minimum release standard:

- no P0 finding
- average score at least 4
- `methodology_iteration_traceability` at least 4 and reported as `pass` or `accepted_with_caveats`
- `reviewer_release_recommendation` is `release_internal_only`, `release_with_caveats`, or `release_external`
- if `release_internal_only`, reviewer must state exact blockers

## Required Reviewer Output

The reviewer should return:

1. completed scorecard
2. one-page reviewer memo
3. list of P0/P1 blockers
4. suggested edits to workflow or templates
5. release recommendation
6. completed intake checklist or equivalent confirmations

## Current Known Blockers

The reviewer should not treat these as surprises:

- no true post-memo follow-through refresh exists yet
- G04 event-watch and packet-export controls are prepared, but they do not clear G04 without a validated later-event refresh
- recent theme selection and refresh controls are prepared, but reviewer should challenge `theme_selection_freshness` before external release
- practice-falsification controls are prepared, but reviewer should challenge `practice_falsification` before external release
- CRM expectation map uses MarketScreener FY2 FCF forecast; reviewer should challenge source methodology
- G01 method-source coverage now includes public Asian/Chinese practitioner sources, but private buyside execution detail remains undercovered; reviewer should accept the basis with caveats or reject it explicitly
- historical backtests still lack reviewer-accepted consensus archives or exception approval
- this pack has only passed internal reviewer simulation so far

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: reviewer cannot reproduce a case conclusion, finds a P0 source-quality issue, rejects the unavailable-data exception, or disagrees with the action label in a way that changes methodology design.
