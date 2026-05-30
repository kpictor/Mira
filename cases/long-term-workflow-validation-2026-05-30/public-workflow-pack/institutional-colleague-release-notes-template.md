# Institutional Colleague Release Notes Template

- release_date: YYYY-MM-DD
- methodology: `long-term-integrated-thesis`
- release_status: draft_not_released
- objective_complete: false
- approved_use: controlled institutional research use
- release_owner: TBD
- stale_after: YYYY-MM-DD
- must_refresh_if: new G04 follow-through evidence, external reviewer findings, material case event, or valuation source challenge changes the release decision

## Release Decision

Decision: `draft_not_released`

Do not distribute this as final external methodology until:

- `G04` true follow-through refresh is complete and accepted.
- `G06` external independent reviewer results are complete and accepted.
- `public-release-decision.md` changes to `release_status: ready_external_release`.
- `scripts/validate_objective_readiness.py` reports `objective_complete: true`.
- `final-release-cutover-checklist.csv` is pass or accepted for every row.
- `institutional-colleague-acceptance-checklist.csv` is pass or accepted, a dated memo based on `institutional-colleague-acceptance-memo-template.md` passes `scripts/validate_institutional_colleague_acceptance_return.py`, and `scripts/validate_institutional_colleague_acceptance.py` reports `acceptance_ready: true`.

## What Is Being Released

This package releases the `long-term-integrated-thesis` workflow for 3-5 year thesis work where the conclusion depends on multiple linked variables:

- consumer or end-demand durability
- product reality and monetization
- macro or capital-cycle transmission
- industry structure and value migration
- company execution and capital allocation
- valuation expectations and what is already priced

The method is designed to block attractive narratives when evidence is insufficient. It is not a stock-picking shortcut and should not be used to bypass source work.

## Validation Base

Current validation evidence:

- ETN and VRT infrastructure trials
- CRM enterprise AI product monetization trial
- LLY GLP-1 healthcare/product dry run
- humanoid robotics value-capture screen
- TDOC and PTON historical failure backtests
- ordinary-vs-workflow comparison
- public workflow pack reviewer simulation
- release QA validator

## Known Limits

Keep these caveats in the release notes unless later evidence closes them:

- No true post-memo follow-through refresh has been completed yet.
- No independent external reviewer has returned a completed scorecard and results memo yet.
- Historical TDOC/PTON examples still require reviewer acceptance of the consensus exception or licensed consensus export before public-grade use.
- CRM G05 uses a MarketScreener FY2028 FCF forecast that must remain visible to the reviewer and final user.
- Private buyside and Chinese-language practitioner source coverage is incomplete.

## Allowed Use

Allowed:

- internal analyst training
- controlled case work with explicit source logs
- PM discussion when action labels and stop rules are preserved
- external review after the blind review packet is assigned

Not allowed before final release:

- final external methodology publication
- portfolio policy adoption
- actionability claims without an expectation map
- use of product, theme or TAM evidence as a substitute for monetization and valuation work
- deletion of source gaps to make the memo look complete

## User Instructions

Before running a case:

1. Confirm the research object, market scope, time boundary and thesis horizon.
2. Run routing through `loops/analysis-routing.md`.
3. If the case is a long-term thesis, use `loops/long-term-thesis-loop.md`.
4. Complete the public workflow pack files and any triggered overlay.
5. Keep evidence, inference and judgment separate.
6. Record `stale_after` and `must_refresh_if`.

## Release Evidence

Attach or cite:

- `public-release-decision.md`
- `public-release-gate-tracker.csv`
- `objective-readiness-audit.csv`
- `release-qa-report-YYYY-MM-DD.md`
- completed G04 follow-through refresh
- completed G06 external reviewer results memo
- completed final cutover checklist
- external go/no-go memo with `decision: go`
