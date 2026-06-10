# Daily Market Brief: {{ market_scope }}

- briefing_type: daily_market_brief
- as_of: {{ as_of_datetime_with_timezone }}
- market_scope: {{ market_scope }}
- time_boundary: {{ time_boundary }}
- source_boundary: {{ source_boundary }}
- live_data_gate: {{ live_data_gate }}
- quote_time: {{ quote_time_or_source_gap }}
- publish_time: {{ publish_time_or_source_gap }}
- stale_after: {{ stale_after }}
- must_refresh_if: {{ must_refresh_if }}

## Market Snapshot

{{ index_rates_fx_commodities_credit_snapshot }}

## Flows And Positioning

{{ public_flows_positioning_snapshot_eg_volume_breadth_vol_margin_balance_limit_up_down_or_cot_etf_flows_with_disclosure_caveats }}

## Key Moves

| asset_or_theme | move | source_time | likely_driver | vs_expectation | attribution_quality | notes |
| --- | ---: | --- | --- | --- | --- | --- |
| {{ asset_or_theme }} | {{ move }} | {{ source_time }} | {{ likely_driver }} | {{ above_below_inline_or_na }} | {{ confirmed_driver_or_plausible_driver_or_contested_driver_or_unexplained_move }} | {{ notes }} |

## Announcements And Rating Changes

| name | item_type | summary | expectation_delta | suggested_route |
| --- | --- | --- | --- | --- |
| {{ name }} | {{ announcement_or_rating_change_or_estimate_change }} | {{ summary }} | {{ expectation_delta }} | {{ route_or_watch_only }} |

## Driver Map

### Facts

{{ dated_facts }}

### Inferences

{{ market_inferences }}

### Judgments

{{ judgments_with_confidence_and_reversal_condition }}

## Today Calendar

| time | event | expected_variable | consensus_or_prior | market_relevance | source |
| --- | --- | --- | --- | --- | --- |
| {{ time }} | {{ event }} | {{ expected_variable }} | {{ consensus_or_prior_or_na }} | {{ market_relevance }} | {{ source }} |

## Watchlist Changes

{{ watchlist_changes }}

## Research Escalation Queue

| object | trigger | suggested_route | urgency | source_note | refresh_condition |
| --- | --- | --- | --- | --- | --- |
| {{ object }} | {{ trigger }} | {{ quick_map_or_monitoring_update_or_earnings_event_or_first_pass_research }} | {{ urgency }} | {{ source_note }} | {{ refresh_condition }} |

## Source Notes

{{ source_notes_with_urls_and_as_of_times }}
