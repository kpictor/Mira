# Iteration 08: LLY Public Pack Dry Run

- date: 2026-05-30
- case: `LLY_GLP1_2026`
- validation_type: fresh_case_dry_run + single_company_live_trial
- pack_used: `public-workflow-pack/`
- result: positive_partial

## Why LLY

LLY was selected because GLP-1 / metabolic health was already in the trial-theme matrix and stresses a different set of variables from AI infrastructure and enterprise AI software:

- direct healthcare product demand
- payer access and realized price
- clinical/regulatory product evidence
- manufacturing and launch execution
- high valuation expectation burden

## Workflow Result

The public pack did not produce a generic "GLP-1 winner" conclusion. It forced this state:

`watch_only_pending_payer_access_and_expectation_map_refresh`

## What Worked

- Theme-to-company handoff was clear because LLY has direct GLP-1 value capture.
- Product reality was strong because Mounjaro and Zepbound are commercial-scale products.
- Valuation expectations changed the actionability label because market cap and forward multiples already price sustained execution.
- Evidence classification separated company-reported growth from analyst estimates and Mira-derived calculations.

## What Failed / Missing

The public pack did not have a healthcare-specific payer overlay. LLY exposed the need to treat payer access, reimbursement, cash-pay price and gross-to-net trends as explicit thesis variables.

## Patch Added

Add `payer_access_and_net_price_check`.

Stop rule:

- If clinical demand is strong but payer access, net price or adherence/persistence is a source gap, do not issue an actionability conclusion.

## Public-Grade Impact

This iteration moves the workflow closer to institutional usability because:

- it adds a fourth full single-company live case
- it proves the candidate public pack can run on a fresh non-AI case
- it adds a healthcare/product-demand overlay

It does not satisfy the full goal because:

- the dry run was performed internally, not by an independent analyst
- no true follow-through refresh exists yet
- LLY still needs transcript support, all-PBM / plan-level payer/access evidence and fuller valuation history before external sharing

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 2026 LLY results, payer/access evidence, Foundayo launch/safety evidence or FY2027 consensus changes alter the actionability label.
