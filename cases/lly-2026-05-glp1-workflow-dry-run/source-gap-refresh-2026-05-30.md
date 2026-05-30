# LLY Source-Gap Refresh: Payer Access and FDA Verification

- case: `LLY_GLP1_2026`
- refresh_date: 2026-05-30
- refresh_type: payer_access_source_gap_refresh
- trigger: initial dry run flagged Foundayo FDA approval and payer/access as source gaps
- status: process_refresh_completed_not_full_follow_through

## Scope Discipline

This refresh does not satisfy the full public-grade follow-through gate.

Reason:

- It uses source work performed inside the same research cutoff window.
- It does not test a later quarterly earnings event after the initial thesis.
- It is still useful because it tests whether the workflow handles a source gap without forcing the analyst to restart the case.

## New Evidence Added

### FDA Verification

The FDA source gap is closed.

- FDA announced approval of Foundayo on 2026-04-01.
- The FDA label confirms Foundayo is indicated with reduced-calorie diet and increased physical activity for adults with obesity, or adults with overweight and at least one weight-related comorbid condition.
- The label also adds safety and usage constraints that should remain part of product-reality monitoring.

Interpretation:

- Regulatory status moves from `company_claim` to `regulator_verified`.
- Product evidence improves.
- It does not remove valuation or access risk.

### Commercial Payer Access

Lilly announced on 2026-05-28 that the three largest PBMs would cover its full obesity medicine portfolio, with CVS Caremark beginning Foundayo coverage on 2026-06-01 and broadening Zepbound access across template plans by 2026-10-01.

CVS independently stated that CVS Caremark would remove the new-to-market block on Foundayo effective 2026-06-01 where approved by plans, and add Zepbound back to commercial formularies as an additional preferred option on 2026-10-01.

Interpretation:

- `payer_coverage` moves from `source_gap` to `partial_verified`.
- The evidence is positive for access, but it is not enough to prove persistence, rebate levels, gross-to-net durability or employer adoption.
- Because the strongest broad PBM claim still comes from Lilly, the workflow should require payer-side confirmation when a payer claim drives actionability.

### Government Access

CMS says the Medicare GLP-1 Bridge will start on 2026-07-01 and provide eligible Medicare Part D beneficiaries access to certain GLP-1 drugs through 2027. CMS lists Foundayo and Zepbound KwikPen as eligible products and states prior authorization criteria apply.

Interpretation:

- Government access improves, but prior authorization remains a friction point.
- This supports volume conversion while increasing the need to monitor price/rebate and utilization management.

## Thesis Impact

No upgrade to actionability.

Prior state:

`watch_only_pending_payer_access_and_expectation_map_refresh`

Refreshed state:

`watch_only_pending_expectation_map_and_realized_price_refresh`

Why the label changed:

- FDA verification no longer blocks publication.
- Payer/access evidence is materially better than the initial source-gap state.
- The remaining bottleneck is whether access expansion converts into durable net revenue after rebates, prior authorization, cash-pay pricing and Medicare program economics.
- Valuation still requires sustained execution at a near-$1T enterprise value.

## Workflow Patch

Add a `source_gap_refresh` rule:

- If an initial memo blocks actionability because a high-impact evidence field is `source_gap`, the next iteration should first try to close that source gap.
- The refresh may change the research action only if the new evidence changes the weakest lens, stop rule or valuation burden.
- A source-gap refresh cannot satisfy the full follow-through gate unless the triggering evidence occurred after the original memo was completed.

## Remaining Gaps

- exact rebate / gross-to-net evidence
- employer opt-in and plan-level coverage evidence
- adherence and persistence
- Q2 2026 realized-price trend
- FY2027/FY2028 FCF consensus
- historical valuation range

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: Q2 2026 results show realized-price deterioration, CMS Bridge implementation details change access, CVS/PBM implementation differs from announced timing, or FY2027 consensus changes by more than 5%.
