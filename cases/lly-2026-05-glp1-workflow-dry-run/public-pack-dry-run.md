# Public Pack Dry Run

- case: LLY GLP-1 direct exposure
- date: 2026-05-30
- pack_used: `cases/long-term-workflow-validation-2026-05-30/public-workflow-pack/`
- result: usable with one healthcare-specific gap

## What Worked

The public pack was sufficient to run a fourth live case without opening the internal methodology card.

Useful sections:

- theme-to-company handoff
- six-lens workflow
- valuation expectations
- evidence classification
- workflow scorecard

The workflow produced a better conclusion than a simple theme memo:

`watch_only_pending_payer_access_and_expectation_map_refresh`

## What The Pack Caught

1. Direct theme exposure does not override valuation burden.
2. GLP-1 demand is real, but realized-price pressure is already visible.
3. Product evidence is strong, but payer access and net price determine how demand converts into durable revenue.
4. High ROIC and revenue growth do not remove the need for expectation mapping.

## What The Pack Missed

The pack does not yet have an explicit healthcare reimbursement overlay.

Suggested patch:

`payer_access_and_net_price_check`

Required fields:

- patient demand
- prescriber demand
- payer coverage
- employer / government reimbursement
- cash-pay price
- gross-to-net / realized-price trend
- prior authorization or access friction
- adherence / persistence
- competitive formulary risk
- policy or regulatory risk

Stop rule:

- If clinical demand is strong but payer access, net price or persistence is a source gap, do not issue an actionability conclusion for a healthcare product thesis.

## Dry-Run Verdict

The pack now has evidence of portability beyond AI infrastructure and enterprise software. It works on a healthcare/product-demand case, but the source appendix and overlay list need a reimbursement/access patch before external release.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: reviewer cannot reproduce the LLY conclusion from the pack, or payer/access evidence changes the actionability label.
