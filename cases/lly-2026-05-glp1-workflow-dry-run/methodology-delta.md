# Methodology Delta: LLY GLP-1 Dry Run

- case: LLY 2026 GLP-1 direct exposure
- review_date: 2026-05-30
- affected_method: `long-term-integrated-thesis`
- decision: keep under trial; add payer access / net price overlay

## What The Case Proves

The workflow is portable to a non-AI sector.

LLY tested:

- direct theme-to-company handoff
- consumer/medical demand
- product reality and regulatory/commercial evidence
- pricing and reimbursement risk
- high valuation burden

The workflow improved the conclusion by separating:

- direct GLP-1 winner status
- commercial product proof
- payer/access and realized-price durability
- stock expectation burden

## Patch Needed

Add `payer_access_and_net_price_check` for healthcare, reimbursement-dependent consumer demand and pharma/biotech product theses.

Required fields:

- `patient_demand`
- `prescriber_demand`
- `payer_coverage`
- `employer_or_government_reimbursement`
- `cash_pay_price`
- `gross_to_net_or_realized_price_trend`
- `prior_authorization_or_access_friction`
- `adherence_or_persistence`
- `competitive_formulary_risk`
- `policy_or_regulatory_risk`

Stop rule:

- If payer access, net price or persistence is a source gap, do not upgrade a healthcare product thesis to actionability even when clinical demand is strong.

## Public Pack Impact

The candidate public workflow pack is usable, but needs this overlay added to avoid under-specifying healthcare cases.

## Remaining Gaps

- earnings-call transcript
- all-PBM independent confirmation and plan-level payer/access evidence
- historical valuation range
- FCF consensus

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 2026 results show realized-price deterioration, payer/access evidence changes, Foundayo launch/safety evidence changes product assumptions, or valuation/consensus refresh changes the actionability label.
