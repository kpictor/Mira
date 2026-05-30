# Iteration 01 Assessment

- iteration_date: 2026-05-30
- validation_stage: direction-level live trial
- method_under_test: `long-term-integrated-thesis`
- status: not_public_grade

## First-Pass Finding

The six-lens structure is useful, but it is still not practical enough for institutional sharing. The first live theme selection exposes five required workflow patches:

1. Add a `theme_to_company_handoff` gate.
2. Add an `evidence_availability_tier`.
3. Add a `market_heat_vs_thesis_maturity` check.
4. Split `valuation_expectations` into `anchor_quality`, `implied_assumption_range` and `false_precision_warning`.
5. Require `read_through_map` for themes with indirect winners or losers.

## Theme Stress Results

### 1. AI Power And Data-Center Infrastructure

- workflow_result: useful but incomplete
- strongest_lens: `industry_structure`
- weakest_lens: `valuation_expectations`
- why: The theme has visible demand and capex narratives, but the investable question is whether public equities already price in multi-year power/cooling/electrical infrastructure scarcity.
- defect_exposed: The current workflow says to reverse-engineer expectations, but does not specify how to handle different valuation anchors across utilities, equipment suppliers, data-center operators and semiconductor companies.
- workflow_patch: `valuation_expectations` must require a sector-specific valuation anchor before any cross-theme conclusion.
- next_test: Compare one equipment beneficiary and one power-generation beneficiary.

### 2. Enterprise AI Agents And Software Monetization

- workflow_result: useful
- strongest_lens: `product_reality`
- weakest_lens: `product_reality`
- why: The same lens is both central and weak. AI-agent narratives require proof of workflow adoption, retention, willingness to pay and revenue conversion.
- defect_exposed: The current product lens lists adoption evidence, but does not distinguish demo capability, pilot usage, paid deployment, margin impact and durable workflow lock-in.
- workflow_patch: Add product evidence ladder: `demo -> pilot -> paid deployment -> expansion -> retention -> pricing power -> margin conversion`.
- next_test: Select one enterprise AI software name with disclosed adoption metrics and compare to one narrative-heavy name.

### 3. GLP-1 Metabolic Health And Consumer Read-Through

- workflow_result: useful but needs segmentation
- strongest_lens: `product_reality`
- weakest_lens: `industry_structure`
- why: Product efficacy and consumer demand can be strong while public-equity value capture depends on access, payer coverage, supply, competition, adherence and read-through magnitude.
- defect_exposed: The workflow does not yet force separation between direct beneficiaries and second-order consumer/retail losers or winners.
- workflow_patch: Require `direct_vs_readthrough` classification before company selection.
- next_test: Compare direct drug exposure with a consumer read-through case.

### 4. Humanoid Robotics And Physical AI

- workflow_result: high value as a rejection/triage tool
- strongest_lens: `valuation_expectations`
- weakest_lens: `public_company_value_capture`
- why: The theme is hot but public equity expressions are often indirect, diversified or driven by other businesses.
- defect_exposed: The workflow needs a precondition that the public company must have a traceable value-capture path before single-equity thesis work begins.
- workflow_patch: Add `investable_purity` and `value_capture_path` fields to `theme_to_company_handoff`.
- next_test: Build a robotics value-chain map before choosing any single stock.

## Workflow Defects Ranked

### P0: Missing Theme-To-Company Handoff

The workflow can analyze a theme, but it does not yet force the transition from broad theme to public-company value capture. This is dangerous in hot themes.

Required fields:

- `theme_definition`
- `value_chain_nodes`
- `public_company_expressions`
- `investable_purity`
- `value_capture_path`
- `why_this_company_not_just_the_theme`
- `read_through_type`: `direct`, `supplier`, `customer`, `substitute`, `victim`, `enabler`, `derivative`

### P0: Valuation Expectations Still Too Abstract

The method says valuation must be reverse-engineered, but hot themes need more guardrails.

Required fields:

- `valuation_anchor_type`
- `anchor_quality`
- `implied_assumption_range`
- `what_must_go_right`
- `what_is_already_priced`
- `false_precision_warning`
- `downside_path`

### P1: Product Reality Needs Evidence Ladder

For AI agents, humanoids and consumer health, the workflow must distinguish different levels of product proof.

Required ladder:

- `concept`
- `demo`
- `pilot`
- `paid_deployment`
- `repeat_usage`
- `expansion`
- `retention`
- `pricing_power`
- `margin_conversion`

### P1: Consumer Lens Needs Behavior And Budget Constraint

Consumer demand must not only ask whether people want something. It must ask who pays, what behavior changes, and what gets displaced.

Required fields:

- `payer`
- `budget_source`
- `substitution`
- `frequency_change`
- `adherence_or_retention`
- `second_order_behavior`

### P2: Macro Weight Needs More Discipline

Macro should not become generic background. It should be scored as:

- `context`
- `secondary`
- `primary`

and tied to a channel:

- revenue
- margin
- financing
- discount rate
- risk premium
- positioning

## Iteration 01 Verdict

The candidate workflow is directionally correct but not yet public-grade. It improved theme triage by exposing weak links, especially in humanoid robotics and AI software monetization. But it needs the patches above before single-company trials can be fairly judged.

## Next Iteration

1. Patch the methodology card with `theme_to_company_handoff`, product evidence ladder and valuation expectation fields.
2. Run two single-company trials:
   - one AI infrastructure / power beneficiary
   - one AI software monetization beneficiary
3. Run one historical failure backtest from a past hot theme.
4. Re-score the workflow against `workflow-scorecard.csv`.

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: any selected theme loses market relevance, public-company expression changes materially, or new company filings provide better evidence for product adoption, capex exposure, payer access or valuation expectations.
