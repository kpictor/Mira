# G05 CRM Unavailable-Data Exception Review

- review_packet_date: 2026-05-30
- gate: `G05 valuation_expectation_map`
- case_id: `CRM_2026`
- decision_needed_from: external independent reviewer
- packet_status: superseded_by_public_fy2_fcf_source
- release_impact: fallback_reviewer_audit_trail

## Supersession Note

After this packet was prepared, MarketScreener's Salesforce financial forecasts page was found to provide FY2028 FCF forecast data.

Primary G05 path is now:

- `g05-fy2-fcf-source-upgrade-2026-05-30.md`

This packet remains useful as reviewer audit trail and fallback if the reviewer rejects MarketScreener as sufficient.

## Question For Reviewer

If the reviewer rejects MarketScreener as sufficient, can CRM's expectation map be treated as public-grade for workflow-release purposes even though FY2028 FCF consensus is unavailable from the remaining public sources used, provided the map:

- keeps FY2028 FCF consensus as `source_gap`;
- labels FY2027 FCF as `modeled`, not consensus;
- includes sourced FY2027/FY2028 revenue and EPS estimates;
- includes current EV, current multiples, peer multiples and historical forward P/E / EV/Sales / EV/FCF;
- blocks valuation-led actionability until product monetization and FCF evidence improve?

Reviewer must answer one of:

- `accept_exception`
- `accept_with_caveats`
- `reject_exception`

## Facts

- CRM current price, market cap, enterprise value and current multiples are sourced from StockAnalysis.
- CRM FY2027/FY2028 revenue and EPS estimates are sourced from StockAnalysis/Finnhub.
- Salesforce FY2026 FCF is sourced from the FY2026 10-K.
- CRM FY2027 FCF is modeled from Salesforce FY2026 FCF and Salesforce FY2027 FCF growth guidance.
- CRM FY2028 FCF forecast is now available from MarketScreener; this exception packet applies only if that source is rejected.
- Historical forward P/E, EV/Sales and EV/FCF are sourced from StockAnalysis ratio history.
- The current action label remains `watch_only_pending_product_monetization_map`.

## Source Attempts

See:

- `g05-crm-source-attempts.csv`

Summary:

- StockAnalysis forecast provides FY2027/FY2028 revenue and EPS, but not FCF consensus.
- StockAnalysis statistics provides current P/FCF and EV/FCF, but not FY2028 FCF consensus.
- StockAnalysis ratio history provides historical forward P/E, EV/Sales and EV/FCF.
- Salesforce filings provide reported FY2026 FCF and FY2027 FCF growth guidance, not FY2028 FCF consensus.
- CompaniesMarketCap provides historical P/S and trailing P/E cross-checks, not FY2028 FCF consensus.

## Why This Exception May Be Acceptable

The missing data field is clearly isolated. The workflow does not substitute a modeled number as consensus, and it does not use valuation to upgrade actionability.

The expectation map can still support a disciplined watch-only conclusion because it answers:

- what is priced today;
- how CRM trades versus its own history;
- how CRM trades versus current peers;
- what assumptions must go right;
- what data would be required to upgrade actionability.

## Why This Exception May Be Rejected

An external reviewer may reject the exception if they believe FY2028 FCF consensus is required because:

- CRM's long-term thesis is cash-flow-driven;
- FY2027 FCF is modeled from guidance and may not capture FY2028 reinvestment, acquisitions or margin changes;
- EPS consensus may not proxy FCF well after ASR, debt financing and Informatica integration;
- public users could overread the map as valuation-complete.

## Reviewer Decision Rubric

Accept only if all are true:

- source attempts are sufficient for the public workflow pack;
- missing FY2028 FCF consensus is clearly labeled `source_gap`;
- modeled FY2027 FCF is not described as consensus;
- false-precision warning is visible in the expectation map;
- actionability remains watch-only and does not rely on the missing FCF field;
- reviewer can reproduce the G05 conclusion from supplied files.

Reject if any are true:

- FY2028 FCF consensus is necessary for public-grade reproducibility;
- source attempts are too shallow;
- ratio-history definitions are too unclear for public use;
- the exception would invite analysts to treat modeled FCF as consensus;
- the map's conclusion depends on the missing field.

## Required Reviewer Output

Reviewer should add rows to:

- `public-workflow-pack/external-reviewer-scorecard.csv`

Required dimensions:

- `g05_source_attempts`
- `g05_false_precision_control`
- `g05_exception_decision`

Required memo fields:

- decision: `accept_exception`, `accept_with_caveats`, or `reject_exception`
- caveats, if accepted
- exact fixes, if rejected
- whether G05 can be cleared for external-release purposes

## Current Internal Judgment

Internal judgment before MarketScreener source discovery: `accept_with_caveats_candidate`.

This is not binding. After MarketScreener source discovery, G05 is tracked through `g05-fy2-fcf-source-upgrade-2026-05-30.md`; reviewer still needs to challenge source sufficiency under G06.

## Source Trail

- CRM expectation map: `../crm-2026-05-product-workflow-trial/expectation-map.csv`
- CRM evidence log: `../crm-2026-05-product-workflow-trial/evidence-log.csv`
- CRM expectation notes: `../crm-2026-05-product-workflow-trial/expectation-map-notes.md`
- CRM valuation source audit: `../crm-2026-05-product-workflow-trial/valuation-source-audit.md`
- G05 upgrade: `g05-expectation-map-upgrade-2026-05-30.md`
- FY2 FCF source upgrade: `g05-fy2-fcf-source-upgrade-2026-05-30.md`

## Refresh Conditions

- stale_after: 2026-06-30
- must_refresh_if: FY2028 FCF consensus becomes available, reviewer rejects the exception, StockAnalysis changes ratio history definitions, CRM issues material FY2028 guidance, or Q2 FY2027 changes FCF trajectory.
