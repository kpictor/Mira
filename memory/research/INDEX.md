# Research Thesis Index

- last_updated: 2026-05-29
- not_investment_advice: true
- purpose: PM-facing thesis registry for current research objects, not a portfolio or trading blotter.
- portfolio_review_loop: `loops/portfolio-review-loop.md`
- portfolio_template: `templates/portfolio-system/portfolio-register.csv`

## Active / Watch Thesis Board

| research_object | state | horizon | conviction | stale_after | next_catalyst | actionability | primary_refs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AAPL | stale | 12-24 months | medium business quality / low new actionability | needs_refresh; case stale on next earnings or 2026-07-13 | next quarterly results / guidance update | no_action | `memory/research/AAPL/thesis-ledger.md`; `cases/aapl-2026-04/actionability-bridge.md` |
| NVTS | upgrade_watch | near-term execution to FY1/FY2 revision | medium-low | next Q2 2026 earnings or material customer/ramp update | Q2 2026 earnings; NVIDIA 800V ecosystem update | small_if_confirmed | `cases/nvts-2026-05/earnings-analysis.md`; `cases/nvts-2026-05/actionability-bridge.md` |
| CRWV | upgrade_watch | 6-18 months | medium demand / low financing clarity | 2026-08-15 or next quarterly update | Q2 results; financing/capex update | watch_only | `cases/crwv-2026-05/event-delta.md` |
| WOLF | narrative_watch | micro-small event / catalyst | low-to-medium, evidence constrained | next quarterly results, customer/order validation update, financing event, or 2026-08-15 | customer/order validation; financing event | watch_only | `cases/wolf-2026-05/expectation-map.csv` |

## Rules

- This board is a research registry, not a portfolio.
- `actionability` values are research actions only and do not authorize trades.
- `state` and `actionability` values must use [../../data/controlled-vocabulary.md](../../data/controlled-vocabulary.md).
- Any row with stale or event-based `stale_after` must be refreshed before live use.
- Add new rows only when a thesis has evidence refs, refresh triggers and an actionability boundary.

## Next Maintenance

- Add explicit thesis-ledger objects for NVTS, CRWV and WOLF if they remain active after the next event update.
- Promote only validated, postmortem-reviewed methods to `adopted`.
- Replace legacy evidence schema cases or keep them marked as historical examples.
