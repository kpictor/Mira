# Research Report Readout: {{ research_object }}

- task_mode: `research_report_interpretation`
- report_title: {{ report_title }}
- provider_or_submitter: {{ provider_or_submitter }}
- author_or_team: {{ author_or_team }}
- report_date: {{ YYYY-MM-DD_or_source_gap }}
- report_type: {{ report_type }}
- market_scope: {{ market_scope }}
- time_boundary: {{ time_boundary }}
- analysis_cutoff_date: {{ YYYY-MM-DD }}
- ingestion_route: {{ ingestion_route }}
- ingestion_artifacts: {{ ingestion_artifacts }}
- license_scope: {{ license_scope }}
- storage_scope: {{ storage_scope }}
- redistribution_allowed: {{ redistribution_allowed }}
- readiness_level: {{ readiness_level }}
- stale_after: {{ YYYY-MM-DD_or_not_applicable }}
- must_refresh_if: {{ refresh_condition }}

## Setup

{{ what_the_user_asked_and_how_the_report_enters_mira }}

## Source And Permission Boundary

{{ report_identity_completeness_permission_and_publication_boundary }}

## Report Thesis

{{ concise_statement_of_the_report_view_rating_target_price_catalyst_and_time_horizon }}

## Claim Map Summary

| claim_area | claim_type | variable | report_claim_summary | independent_status | treatment |
| --- | --- | --- | --- | --- | --- |
| {{ claim_area }} | {{ claim_type }} | {{ variable }} | {{ summary_without_long_quote }} | {{ confirmed_or_source_gap }} | {{ treatment }} |

## Expectation / Variant-Perception Bridge

{{ whether_the_report_repeats_consensus_challenges_consensus_or_changes_the_expected_variable }}

## Valuation And Model Decomposition

{{ target_price_rating_model_or_multiple_decomposition_with_calculation_gap_if_needed }}

## Independent Cross-Check

{{ higher_weight_sources_checked_and_conflicts_or_gaps }}

## Bias And Framing Check

{{ incentives_selection_bias_model_precision_or_narrative_risks }}

## Mira Thesis Impact

{{ no_new_evidence_new_variable_evidence_upgrade_evidence_downgrade_expectation_delta_method_delta_or_actionability_gap }}

## Facts / Inferences / Judgments

### Facts

{{ verified_or_disclosed_facts }}

### Inferences

{{ attributed_interpretations_and_mira_reasoning }}

### Judgments

| judgment | confidence | confidence_basis | reversal_condition |
| --- | --- | --- | --- |
| {{ judgment }} | {{ low_medium_high }} | {{ basis }} | {{ reversal_condition }} |

## Refresh Triggers

- stale_after: {{ YYYY-MM-DD_or_not_applicable }}
- must_refresh_if: {{ refresh_condition }}

## Follow-Up Prompts

1. {{ route_bound_followup_question }}
