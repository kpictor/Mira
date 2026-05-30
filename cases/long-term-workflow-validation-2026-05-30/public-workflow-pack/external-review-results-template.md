# External Review Results Template

- review_date: YYYY-MM-DD
- reviewer_id: replace
- reviewer_independence_confirmed: false
- reviewed_pack_version_date: 2026-05-30
- review_status: draft
- release_recommendation: replace

Allowed `release_recommendation` values:

- `release_external`
- `release_with_caveats`
- `release_internal_only`
- `reject`

## Independence Confirmation

`review_date` and `reviewer_id` must match the completed scorecard exactly.

Reviewer confirms they did not use:

- internal chat history
- unpublished reasoning notes
- review-log history
- live explanations from the original analyst

Reviewer used:

- public workflow pack
- assigned case files
- public sources and filings
- completed `external-reviewer-scorecard.csv`

## Scorecard Summary

Copy these values from the completed scorecard. Do not manually adjust them to improve release optics.

- average_score:
- minimum_score:
- p0_findings_count:
- p1_findings_count:
- g01_method_source_decision: `accept_basis` | `accept_with_caveats` | `require_private_material` | `reject_basis`
- g04_follow_through_readiness: `pass` | `accepted_with_caveats` | `fail`
- g04_false_completion_control: `pass` | `accepted_with_caveats` | `fail`
- theme_selection_freshness: `pass` | `accepted_with_caveats` | `fail`
- practice_falsification: `pass` | `accepted_with_caveats` | `fail`
- methodology_iteration_traceability: `pass` | `accepted_with_caveats` | `fail`
- g05_source_decision: `accept_source` | `accept_with_caveats` | `reject_source`
- historical_consensus_exception_decision: `accept_exception` | `accept_with_caveats` | `require_export` | `reject_exception`
- action_label_reproducibility: pass | partial | fail
- release_blockers_remaining:

## Findings

| severity | case_or_task | finding | evidence | required_fix | release_impact |
| --- | --- | --- | --- | --- | --- |
| P0/P1/P2/P3/none | replace | replace | replace | replace | blocker/caveat/none |

For P1 findings, `required_fix` must use `owner: ...; fix: ...`. P0/P1 rows in this table must match `p0_findings_count` and `p1_findings_count`.

## G01 Method-Source Decision

Reviewer decision:

- `accept_basis`
- `accept_with_caveats`
- `require_private_material`
- `reject_basis`

Reviewer notes:

- public institutional source sufficiency:
- Asian/Chinese practitioner source sufficiency:
- private buyside execution-detail gap:
- required caveats or fixes:

## G04 Follow-Through Readiness Decision

Reviewer decision:

- `pass`
- `accepted_with_caveats`
- `fail`

Reviewer notes:

- trigger tracker specificity:
- event-watch calendar sufficiency:
- later-event candidate screen sufficiency:
- `validate_g04_later_event_candidate_screen.py` pre-refresh control:
- `refresh_allowed: yes` boundary:
- execution tracker sufficiency:
- false-completion controls:
- required caveats or fixes:

## Recent Theme Selection Decision

Reviewer decision:

- `pass`
- `accepted_with_caveats`
- `fail`

Reviewer notes:

- seven-theme coverage:
- hotness source-id sufficiency:
- stale_after boundaries:
- refresh trigger specificity:
- drop/replace rule specificity:
- required caveats or fixes:

## Practice Falsification Decision

Reviewer decision:

- `pass`
- `accepted_with_caveats`
- `fail`

Reviewer notes:

- case evidence sufficiency:
- falsification test specificity:
- actionability delta sufficiency:
- source-gap consequence handling:
- theory-only or stale-theory claims found:
- required caveats or fixes:

## Methodology Iteration Traceability Decision

Reviewer decision:

- `pass`
- `accepted_with_caveats`
- `fail`

Reviewer notes:

- case failure to patch traceability:
- patch artifact sufficiency:
- validator and decision-effect sufficiency:
- overfit or memory-based patches found:
- required caveats or fixes:

## G05 Source Decision

Reviewer decision:

- `accept_source`
- `accept_with_caveats`
- `reject_source`

Reviewer notes:

- MarketScreener FY2028 FCF forecast sufficiency:
- StockAnalysis ratio-history sufficiency:
- false-precision controls:
- required caveats or fixes:

## Historical Consensus Exception Decision

Reviewer decision:

- `accept_exception`
- `accept_with_caveats`
- `require_export`
- `reject_exception`

Reviewer notes:

- TDOC consensus source attempts:
- PTON consensus source attempts:
- false-precision controls:
- whether historical examples can be shared as caveated examples:
- required licensed export or fixes:

## Release Recommendation Rationale

State whether the workflow can be shared with institutional colleagues and under what caveats.

If not ready, list exact blockers and the evidence needed to clear them.

## Required Attachments

- completed `external-reviewer-scorecard.csv`
- reviewer memo
- P0/P1 blocker list, if any

## Refresh Conditions

- stale_after: YYYY-MM-DD
- must_refresh_if: reviewer recommendation changes, P0/P1 blockers are fixed, G04 follow-through refresh completes, historical consensus export becomes available, or source definitions change materially.
