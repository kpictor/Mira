# Methodology Card: Long-Term Integrated Thesis

- status: trial
- role: workflow + lens router + valuation expectation bridge
- last_updated: 2026-05-30
- source_bucket: mixed (`institutional`, `practitioner`, `first_principles`, `derived_internal`)
- source_quality: medium-high
- credibility_score: medium-high
- credibility_basis: The candidate combines durable public frameworks from CFA/HBS industry analysis, McKinsey consumer journey, HBR Jobs-to-Be-Done, SVPG product discovery, Mauboussin-style value creation and Expectations Investing. Later validation added live/historical Mira cases plus public Asian/Chinese practitioner priors from Hillhouse and Ping An Asset Management. Credibility remains limited by private buyside process opacity and the need for completed G04/G06 evidence.
- search_coverage: medium-high
- search_gaps: private buyside research processes, postmortems of failed long-term theses, sector-specific consumer/product evidence standards, external reviewer challenge, and true later-event follow-through evidence.
- comparison_baseline: ordinary `long_term_thesis` plus current Mira `framework-routing`, `macro-overlay`, `supply-chain`, `valuation-expectation`, and `long-term-multibagger-research`
- empirical_validation_mode: trial -> case backtest + live case trial
- follow_through_plan: Test on at least four cases: one mega-cap platform, one consumer/product mid-cap, one failed growth story, and one macro-sensitive cyclical or financial company.

## Core Idea

Long-term equity research should not ask only whether a company is good or whether an industry is growing. It should force six connected questions:

1. Is end demand real, durable and economically funded?
2. Is the product or service actually solving a customer job better than alternatives?
3. Is the macro environment helping, neutral or structurally constraining the thesis?
4. Is the industry structure allowing value capture, or is the profit pool migrating elsewhere?
5. Can this company execute, reinvest and defend returns over the thesis horizon?
6. What does the current market price already imply about all five questions?

The sixth question is mandatory. Without `valuation_expectations`, the method can identify a strong long-term business but fail to identify whether the stock offers attractive risk/reward.

## Reverse-Engineered From

- CFA-style industry and competitive analysis: industry boundary, size, growth, life cycle, profitability, concentration, competitive forces and macro/regulatory context.
- Porter Five Forces: supplier power, buyer power, threat of entrants, substitutes and rivalry.
- McKinsey Consumer Decision Journey: consideration, evaluation, purchase, experience and loyalty loops.
- HBR Jobs-to-Be-Done: customers hire products to make progress in specific circumstances, not because of abstract product categories.
- SVPG Product Discovery: product risk can be separated into value, usability, feasibility and business viability.
- Mauboussin / Morgan Stanley value-creation logic: ROIC, competitive advantage period, reinvestment and capital allocation discipline.
- Expectations Investing: reverse-engineer price-implied expectations rather than stopping at business analysis.
- Mira internal methods: `thesis-horizon-routing`, `framework-routing`, `macro-overlay`, `supply-chain`, `valuation-expectation`, `variant-perception`, and `long-term-multibagger-research`.

## Search Paths Used

- Method name search:
  `long term investment process`, `fundamental research process`, `industry competitive analysis`, `consumer decision journey`, `jobs to be done`, `product discovery`, `ROIC competitive advantage period`, `expectations investing`
- Artifact search:
  official framework pages, public institutional research pages, investor education pages, practitioner product research pages
- Contradiction search:
  `why long term investment theses fail`, `TAM fallacy`, `product market fit failure`, `valuation risk growth stocks`, `Porter five forces limitations`
- Translation / Asia practitioner search:
  Chinese and Asia practitioner coverage was improved with public Hillhouse and Ping An Asset Management sources. It is still not enough for final adoption without external reviewer acceptance because private buyside execution detail remains undercovered.

## Use When

- The user asks for long-term company, industry or theme research with horizon beyond one year.
- The thesis depends on multiple linked variables rather than a single earnings event.
- A company narrative mixes consumer demand, product adoption, industry growth, macro regime, execution quality and valuation.
- Mira needs to decide whether short-term evidence can be extrapolated into a long-term thesis.

## Avoid When

- The task is a pure earnings event, intraday move, short-term catalyst or FY1/FY2 revision.
- The research object is macro-only and does not need company/product/industry decomposition.
- Source quality is too weak to populate at least three of the six lenses.
- The user only needs a quick source check or narrow fact verification.

## Applies To

- `single_equity`
  Main use case. Can sit above `framework-routing` when `horizon_bucket = long_term_thesis` or `regime_transition`.
- `industry_concept`
  Use to decide which parts of a broad theme are demand, product, macro, industry structure or company execution.
- `macro_asset_or_regime`
  Use only when macro is being translated into company or sector opportunities.
- `portfolio_review`
  Use to compare which holdings have the weakest long-term assumption and which lenses are stale.

## Core Question

Does the long-term thesis survive a six-lens test, and does the current price leave enough room for the thesis to create investable upside after accounting for evidence quality, timing, competition, macro constraints and valuation expectations?

## Required Inputs

### Research Setup

- `research_object`
- `market_scope`
- `time_boundary`
- `horizon_bucket`
- `current_market_label`
- `available_sources`
- `source_gaps`
- `market_heat`: `low`, `medium`, `high`, `extreme`
- `thesis_maturity`: `unproven`, `early_evidence`, `scaling`, `financial_conversion`, `mature`
- `heat_maturity_gap`: `none`, `moderate`, `large`, `extreme`

### Theme-To-Company Handoff

Use this gate before writing a single-company long-term thesis from a hot theme:

- `theme_definition`
- `theme_maturity`: `early_narrative`, `early_revenue`, `scaling_revenue`, `margin_conversion`, `mature_cycle`
- `value_chain_nodes`
- `public_company_expressions`
- `investable_purity`: `low`, `medium`, `high`
- `value_capture_path`
- `why_this_company_not_just_the_theme`
- `read_through_type`: `direct`, `supplier`, `customer`, `substitute`, `victim`, `enabler`, `derivative`
- `theme_purity_score`: 1-5
- `expectation_burden_score`: 1-5
- `evidence_maturity_score`: 1-5
- `valuation_heat_score`: 1-5
- `handoff_decision`: `single_equity_research`, `industry_map_first`, `watch_only`, `reject_for_now`

Stop rule:

- If `value_capture_path` is unclear, do not write a single-company long-term thesis. Build an industry map or watchlist instead.
- If `theme_purity_score >= 4` and `expectation_burden_score >= 4`, do not issue an actionability conclusion without a complete expectation map.

### Consumer Demand

- end user and buyer identity
- adoption path and purchase trigger
- affordability and budget source
- frequency, retention, repeat purchase or churn
- substitution and trading-down risk
- channel and distribution evidence

### Payer Access / Net Price

Use this sub-lens when demand depends on reimbursement, insurance coverage, government access, employer benefits, cash-pay pricing or healthcare policy:

- `patient_demand`
- `prescriber_demand`
- `clinical_evidence`
- `regulatory_status`
- `payer_coverage`
- `employer_or_government_reimbursement`
- `cash_pay_price`
- `gross_to_net_or_realized_price_trend`
- `prior_authorization_or_access_friction`
- `adherence_or_persistence`
- `competitive_formulary_risk`
- `policy_or_regulatory_risk`

Stop rule:

- If clinical demand is strong but payer access, net price or persistence is a source gap, use `research_action: watch_only_pending_payer_access`.

### Pull-Forward Vs Structural Demand

Use this sub-lens when a thesis forms during an abnormal demand shock:

- pandemic
- stimulus
- regulatory deadline
- supply shortage
- one-time replacement cycle
- interest-rate or credit shock
- inventory restocking

Required fields:

- `shock_source`
- `duration_of_shock`
- `normalized_usage_baseline`
- `post_shock_retention`
- `payer_or_budget_persistence`
- `valuation_if_growth_normalizes`

Stop rule:

- If `shock_source` is material and `normalized_usage_baseline` or `post_shock_retention` is `source_gap`, the thesis cannot be upgraded to actionability.

### Product Reality

- customer job or use case
- product superiority versus alternatives
- value, usability, feasibility and business viability risks
- usage, retention, conversion or renewal evidence
- product roadmap dependencies
- feature-to-business-model translation
- product evidence ladder:
  `concept -> demo -> pilot -> paid_deployment -> repeat_usage -> expansion -> retention -> pricing_power -> margin_conversion`

Stop rule:

- Do not treat `demo`, `pilot` or management anecdotes as proof of durable product-market fit.
- Do not treat usage growth as monetization unless the metric is tied to pricing, revenue, retention or margin.

### Product Monetization Map

Use this sub-lens when `product_reality` is a primary lens and the company discloses AI/software/product usage or ARR metrics:

- `product_metric`
- `metric_type`: `ARR`, `usage`, `bookings`, `active_users`, `tokens`, `records`, `API_calls`
- `economic_link`: `direct_revenue`, `expansion_signal`, `retention_signal`, `usage_proxy`, `cost_driver`
- `incrementality`: `new`, `cross_sell`, `bundle`, `acquired`, `source_gap`
- `customer_cohort`
- `retention_or_renewal_evidence`
- `pricing_evidence`
- `margin_evidence`
- `total_company_bridge`

Stop rule:

- If product usage/ARR metrics cannot be bridged to retention, pricing, margin or total-company growth, use `research_action: watch_only_pending_product_monetization_map`.

### Hardware / Subscription Mix

Use this sub-lens when a subscription thesis depends on physical product sales, devices, equipment, installation, supply chain or installed-base expansion:

- `hardware_revenue_growth`
- `hardware_gross_margin`
- `subscriber_growth_source`
- `retention_or_churn`
- `engagement_quality`
- `inventory_or_capacity_commitment`
- `replacement_cycle`
- `normalized_new_user_demand`
- `unit_economics_after_normalization`

Stop rule:

- If subscription growth depends on hardware placements and normalized hardware demand or hardware gross margin is a source gap, use `research_action: watch_only_pending_normalized_hardware_demand`.

### Macro Economy

- growth, inflation, employment, rates, credit, fiscal, currency and liquidity context
- macro-to-company transmission chain
- revenue, margin, financing, discount-rate and risk-premium exposure
- macro_weight: `context`, `secondary` or `primary`
- what macro path the market appears to price in

### Industry Structure

- industry boundary and profit-pool definition
- supply/demand balance
- industry life-cycle stage
- supplier/customer power
- threat of entrants, substitutes and rivalry
- regulation and technology route risk
- value-chain position and profit-pool migration

### Company Execution

- management credibility
- capital allocation record
- ROIC and reinvestment runway
- margin structure and operating leverage
- financial quality and balance-sheet survivability
- execution KPIs versus peers
- moat durability and competitive advantage period

### Valuation Expectations

- current valuation anchor and quality
- `valuation_anchor_type`
- `anchor_quality`: `high`, `medium`, `low`, `source_gap`
- market-implied growth, margin, ROIC, duration and risk-premium assumptions
- `implied_assumption_range`
- base / bull / bear scenario ranges
- what must go right for current price to be fair
- what is already priced
- false precision warning
- variant perception versus market
- downside path and kill criteria
- valuation refresh trigger

Stop rule:

- If `anchor_quality = source_gap`, the workflow may still produce a research thesis but not an actionability conclusion.
- If `market_heat = high` or `extreme` and this is a single-equity memo, missing FY1/FY2 expectation mapping forces `research_action: watch_only_pending_expectation_map`.

Minimum single-company expectation map:

- current price
- current market cap / enterprise value
- FY1/FY2 consensus revenue, EPS and FCF, or explicit `source_gap`
- company guidance midpoint
- historical company multiple range, with metric definitions separated
- current peer multiple range, with peer comparability caveats
- implied growth duration
- implied margin / ROIC path
- downside multiple and earnings path

Do not mix current peer multiples, historical trailing multiples and forward consensus multiples into one valuation judgment. If historical EV/FCF, historical forward P/E or FY2 FCF consensus are unavailable, keep them as explicit source gaps instead of substituting an easier metric.

### Backlog Quality

Use this sub-lens when backlog, RPO, order book or book-to-bill drives the thesis:

- `order_backlog_disclosure_quality`: `direct`, `partial`, `qualitative`, `source_gap`
- `firm_commitment_definition`
- `delivery_timing`
- `book_to_bill`
- `cancellation_or_deferral_risk`
- `margin_of_backlog`
- `customer_concentration`
- `capacity_constraint`
- `conversion_refresh_trigger`

Stop rule:

- Backlog growth alone cannot prove durable demand unless conversion timing, firmness and margin quality are addressed.

### Acquisition-Driven Value Capture

Use this sub-lens when the thesis depends on acquisitions or portfolio reshaping:

- `strategic_fit`
- `purchase_price`
- `funding_mix`
- `integration_cost`
- `incremental_margin`
- `ROIC_path`
- `what_would_show_value_creation`

Stop rule:

- Do not count acquired exposure as value creation until the integration and ROIC path is explicit.

### Capital Allocation Distortion

Use this sub-lens when buybacks, ASRs, acquisitions, divestitures or debt materially affect per-share metrics:

- `capital_action`
- `funding_source`
- `share_count_effect`
- `debt_or_cash_effect`
- `eps_effect`
- `operating_vs_financial_engineering`
- `capital_allocation_refresh_trigger`

Stop rule:

- Do not treat per-share acceleration as operating acceleration until share count, debt and acquisition effects are separated.

### Cash Flow Quality

Use this sub-lens when free cash flow or cash conversion is part of the long-term thesis:

- `fcf_quality`: `high`, `medium`, `low`, `source_gap`
- `working_capital_tailwind`
- `deferred_revenue_change`
- `capex_intensity`
- `repeatability_of_cash_conversion`

Stop rule:

- Do not treat one-quarter free-cash-flow strength as durable without working-capital decomposition and capex requirements.

## Primary Signal

The strongest long-term signal is not any single lens. It is cross-lens consistency:

- consumer demand is real and economically funded
- product evidence explains why adoption should persist
- industry structure allows value capture
- macro does not overwhelm the thesis or is explicitly priced
- company execution converts the opportunity into ROIC and cash flow
- valuation does not already require near-perfect execution

## Why It Works

Long-term failures often happen because research overweights one attractive dimension:

- big TAM without company right-to-win
- loved product without durable unit economics
- strong demand in a bad profit pool
- good company with no valuation margin
- industry tailwind overwhelmed by macro tightening
- short-term evidence incorrectly promoted to long-term proof

This method makes those hidden leaps explicit. It improves Mira by turning long-term analysis from a narrative memo into a dependency map with evidence quality, conflict checks and refresh triggers.

## Failure Mode

- It may become too heavy for simple cases.
- It may create fake precision in `valuation_expectations` if market expectation proxies are weak.
- It may underweight sector-specific variables if used mechanically.
- It may duplicate existing overlays unless the lens router is explicit.
- It may still miss non-public primary research signals.

## Evidence Cost

High for full workflow. Medium if used as a routing checklist. Evidence cost is highest for consumer demand and product reality when public data is thin.

## Speed Vs Depth

- quick scan: answer the six questions with `known`, `unknown`, `not_material`
- standard research: populate each lens with 3-5 evidence-backed variables
- deep research: build full dependency map, valuation expectation bridge and case-specific evidence ladder

## Comparison To Existing Methods

Compared with current `thesis-horizon-routing`, this adds content structure after the horizon is identified.

Compared with `framework-routing`, this is not a price-setter classification. It is a long-term thesis decomposition system.

Compared with `supply-chain` and `macro` overlays, this is broader and decides when those overlays matter.

Compared with `long-term-multibagger-research`, this is less return-path-specific and more general. The multibagger method can become a specialized mode inside this workflow when the target return path is 10x/100x.

Compared with `variant-perception`, this adds operating lens depth. `variant-perception` remains useful as the market-expectation discipline inside the valuation bridge.

## Follow-Through Criteria

For each completed case, record:

- which lens drove the thesis
- which lens was the weakest assumption
- which lens had the largest source gap
- whether valuation expectations changed the conclusion
- which refresh trigger fired first
- whether the method found a risk that ordinary memo writing would have missed
- whether `theme_to_company_handoff` prevented a false single-stock conclusion
- whether `market_heat_vs_thesis_maturity` forced a downgrade

## Trial Design

Run four case tests:

1. Mega-cap platform: test whether consumer/product/industry/company/valuation conflicts are clearer than ordinary `large-mega` memo.
2. Consumer or product-led mid-cap: test demand and product evidence discipline.
3. Failed growth story: backtest whether the workflow would have exposed the weak lens early.
4. Macro-sensitive company: test whether macro is correctly weighted without taking over company analysis.

Iteration 01 live theme tests:

- `ai_power_and_data_center_infrastructure`
- `enterprise_ai_agents_and_software_monetization`
- `glp1_metabolic_health_and_consumer_readthrough`
- `humanoid_robotics_and_physical_ai`

Iteration 01 exposed required patches:

- add `theme_to_company_handoff`
- add `market_heat_vs_thesis_maturity`
- add product evidence ladder
- split valuation expectations into anchor quality, implied assumption range, false precision warning and downside path
- classify direct versus read-through exposure before company selection

Iteration 03 ETN single-company trial exposed required patches:

- add minimum single-company expectation map
- add backlog quality sub-lens
- add acquisition-driven value capture sub-lens
- allow `consumer_demand` to translate into ultimate demand units for infrastructure cases

Iteration 04 VRT single-company contrast trial exposed required patches:

- add `purity_vs_expectation_burden` scoring
- add `order_backlog_disclosure_quality`
- add cash-flow quality / working-capital decomposition

Iteration 05 CRM product-reality trial exposed required patches:

- add `product_monetization_map`
- classify usage metrics by economic link
- separate organic product growth, acquired contribution, bundling and cross-sell
- add capital allocation distortion checks for ASR/debt effects

Iteration 06 TDOC historical failure backtest exposed required patches:

- add `pull_forward_vs_structural_demand`
- require normalized usage and post-shock retention before upgrading demand-shock growth
- treat acquisition-driven thesis expansion as unproven until ROIC / cross-sell / retention evidence is visible

Iteration 07 PTON historical failure backtest exposed required patches:

- add `hardware_subscription_mix_check`
- separate installed-base retention from normalized new hardware demand
- treat inventory and capacity commitments during abnormal demand as thesis-risk variables
- require hardware gross margin and unit economics after demand normalization before actionability

Iteration 08 LLY fresh-case dry run exposed required patches:

- add `payer_access_and_net_price_check`
- separate clinical/patient demand from reimbursed economic demand
- treat lower realized price as a thesis variable, not a footnote
- require payer access, net price and persistence evidence before actionability in healthcare product theses

Iteration 09 LLY source-gap refresh exposed required patches:

- add `source_gap_refresh`
- require source-gap refreshes to state whether they qualify as true post-memo follow-through
- allow source-gap closure to improve publication quality without automatically upgrading actionability
- require favorable new evidence to change the weakest lens, stop rule or valuation burden before it changes the research action

Iteration 10 public-pack reviewer simulation exposed required patches:

- every overlay in workflow must have README, fill-guide, checklist and template-inventory support
- decision labels used in cases must be defined or mapped to a standard stop rule
- internal reviewer simulation can improve reproducibility but cannot substitute for external independent analyst review

Iteration 11 historical source cleanup exposed required patches:

- historical failure backtests need separate valuation reconstruction tables
- approximate peak valuation must include price source, share-count source and source-variance warning
- exact peak EV and contemporaneous consensus should remain source gaps if not available, not be replaced by easier market-cap proxies

Iteration 12 humanoid robotics value-capture screen exposed required patches:

- add `theme_value_capture_screen`
- require public-company value capture before single-equity work on high-heat themes
- route themes with mostly private/pre-revenue/enabler exposure to `industry_map_first`
- do not treat enabling-layer exposure as pure-play theme exposure without a revenue bridge

Iteration 13 ordinary-vs-workflow comparison exposed required patches:

- add `ordinary_vs_workflow_delta`
- require each validation case to show whether the workflow changed actionability, source gaps, kill criteria, sizing or refresh triggers
- treat no decision change as a possible methodology failure or cost-efficiency failure

Iteration 14 expectation-map data availability audit exposed required patches:

- add `expectation_map_unavailable_data_exception`
- keep unavailable FY2 FCF or historical EV/FCF / forward P/E as `source_gap`
- label modeled values as modeled, not consensus
- require reviewer acceptance before an unavailable-data exception can support external sharing

Iteration 15 external reviewer packet exposed required patches:

- public-grade release requires a reviewer brief, blind assignment and scorecard
- internal simulation can prepare the workflow but cannot create independent review evidence
- reviewer output must include P0/P1 blockers and a release recommendation

Iteration 16 follow-through refresh playbook exposed required patches:

- true follow-through requires a later event after original memo cutoff
- refresh must compare before/after thesis variables and action label
- refresh must evaluate whether the original `must_refresh_if` was specific enough
- source-gap refresh and follow-through refresh must remain separate gates

Iteration 17 release gate tracker exposed required patches:

- separate `candidate_internal_release` from `external_release`
- external release requires named gates, evidence paths, blockers and next actions
- release decision should remain negative until true follow-through and external reviewer gates are resolved; G05 expectation-map gate is now internally cleared but remains subject to G06 source challenge

Iteration 18 operational loop creation exposed required patches:

- promote the trial checklist into `loops/long-term-thesis-loop.md` for internal candidate use
- route 3-5 year, multi-lens, hot-theme-to-company or valuation-expectation-heavy questions into the dedicated loop instead of treating them as a small research-loop add-on
- keep the operational loop explicitly below final external-release status until true follow-through and external reviewer gates are resolved

Iteration 19 release QA validation exposed required patches:

- add `scripts/validate_long_term_release.py` so release status can be checked by command rather than asserted in prose
- separate all non-clear external gates from hard blocking gates
- require release decision, public audit, operational loop and public workflow pack to remain internally consistent before any external release claim

Iteration 20 G05 expectation-map upgrade exposed required patches:

- treat historical EV/FCF and forward P/E as solvable public-data gaps when a ratio-history source exists
- keep FY2 FCF consensus as a separate gate instead of hiding it inside a broad valuation-quality label
- allow a case to become `near_public_grade_pending_fy2_fcf_exception_review` without upgrading actionability

Iteration 21 G05 exception-review packet exposed required patches:

- turn unavailable-data exception from a methodology rule into a reviewer-decision packet
- require source-attempt evidence before asking a reviewer to accept an exception
- add scorecard dimensions for source-attempt sufficiency, false-precision control and exception decision

Iteration 22 G05 FY2 FCF source upgrade exposed required patches:

- continue searching for public data before relying on an unavailable-data exception
- allow a gate to move from exception-review path to sourced-data path when a public forecast source is found
- keep reviewer challenge under G06 even when G05 is internally cleared by data

Iteration 23 G06 reviewer handoff exposed required patches:

- external reviewer review is not complete until a scorecard, results memo and intake checklist are returned
- G06 clearing requires independence confirmation, no P0s, average score at least 4, G05 source acceptance and release recommendation
- release validator should check reviewer handoff completeness now and completed reviewer-result evidence later

Iteration 24 G04 follow-through handoff exposed required patches:

- true follow-through cannot be replaced by source-gap cleanup or same-window evidence
- first CRM refresh needs an assignment packet with original cutoff, target thesis variables and non-qualification examples
- release validator should reject a completed G04 claim unless the refresh file proves later event, before/after labels and `qualifies_as_true_follow_through: yes`

Iteration 25 external reviewer bundle integrity exposed required patches:

- reviewer handoff needs a send/no-send manifest, not only prose instructions
- blind review should explicitly exclude internal development logs unless requested
- release validator should check reviewer bundle paths before reviewer assignment

Iteration 26 external reviewer request memo exposed required patches:

- reviewer assignment should include a standardized request memo, not only templates
- independence boundary and known blockers should be visible before the reviewer starts
- release validator should check the request memo for independence and G04 blocker disclosure

Iteration 27 final release cutover exposed required patches:

- final external release needs a cutover checklist and go/no-go memo, not only gate-status edits
- validator should reject `ready_external_release` while any required gate remains non-clear
- validator should require all cutover rows to pass and a `decision: go` memo before final release

Success criteria:

- Identifies the weakest assumption before the conclusion.
- Produces clearer `must_refresh_if` conditions.
- Prevents at least one overconfident long-term extrapolation.
- Improves the valuation / expectations bridge versus ordinary thesis memo.

## Falsification Conditions

- The workflow does not produce a better source-gap map than existing research-loop outputs.
- Trial cases show repeated overlap with existing overlays without incremental insight.
- The valuation bridge creates false precision and does not change conclusions.
- Analysts skip the workflow because it is too heavy for normal research.
- It fails to catch obvious demand/product/industry/company conflicts in historical failed cases.

## Adoption Decision

Do not adopt as final external methodology yet. Keep `long-term-integrated-thesis` as `trial` for final release and `candidate_internal_release` for controlled internal use.

Recommended next step:

- Use `loops/long-term-thesis-loop.md` as the operating loop for any `horizon_bucket = long_term_thesis` research request that depends on multiple operating variables, theme-to-company handoff or valuation expectations.
- Run `scripts/validate_long_term_release.py` after any release-gate or public-pack change.
- Send the machine-checked reviewer bundle plus CRM G05 source package to an independent reviewer and collect the completed scorecard/results memo/intake checklist. Run the first true follow-through refresh after a later material event using `g04-follow-through-handoff-2026-05-30.md`. Only then complete `final-release-cutover-checklist.csv` and a go/no-go memo before changing release status.
