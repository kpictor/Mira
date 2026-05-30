# G04 Follow-Through Refresh Validation Standard

- standard_date: 2026-05-30
- gate: `G04 true_follow_through_refresh`
- status: ready_to_validate_future_refresh
- validation_script: `../../scripts/validate_follow_through_refresh.py`
- stale_after: 2026-06-30
- must_refresh_if: follow-through template fields change, G04 intake fields change, preferred case changes, or a reviewer changes the G04 clearing rule

## Purpose

This standard defines how to validate a completed true follow-through refresh.

It does not clear G04 by itself. G04 clears only after a later material event occurs, a completed refresh file is written, the evidence log is updated and the validation script exits 0.

## Required Inputs

Minimum command:

```bash
python3 scripts/validate_follow_through_refresh.py \
  --refresh path/to/follow-through-refresh-YYYY-MM-DD.md \
  --original-cutoff YYYY-MM-DD
```

Preferred command:

```bash
python3 scripts/validate_follow_through_refresh.py \
  --refresh path/to/follow-through-refresh-YYYY-MM-DD.md \
  --original-cutoff YYYY-MM-DD \
  --evidence-log path/to/evidence-log.csv \
  --intake path/to/completed-g04-follow-through-intake-checklist.csv \
  --gate-tracker cases/long-term-workflow-validation-2026-05-30/public-release-gate-tracker.csv \
  --public-readiness-audit cases/long-term-workflow-validation-2026-05-30/public-readiness-audit.md \
  --review-log memory/methodologies/review-log.csv
```

## Pass Conditions

The script requires:

- `qualifies_as_true_follow_through: yes`;
- `follow_through_gate_status: pass`;
- validation summary reports `g04_clearable: true`;
- refresh date after the original memo cutoff;
- `original_memo_date` equals the supplied original cutoff;
- `stale_after` is later than `refresh_date`;
- completed qualification table with all required rows answered `yes` and supported by evidence;
- new event evidence table with source rows dated after the original cutoff;
- before/after thesis-variable table;
- exactly one approved refresh result label;
- `stale_after` and `must_refresh_if`;
- if supplied, updated evidence log has at least one source date after the original cutoff and contains the same later-event `source_id` values used in the refresh;
- if supplied, G04 intake checklist contains all required intake requirements and all rows are `pass` or `accepted`.
- if supplied, the release gate tracker has G04 in an external-clear status and points to the completed refresh file;
- if supplied, public-readiness audit references the completed refresh, the case ID, `follow_through_gate_status: pass` and the selected refresh result label;
- if supplied, methodology review log has a G04 follow-through row for the case and completed refresh.

## Failure Conditions

G04 remains blocked if:

- the refresh is a same-window source-gap cleanup;
- event date is not after original cutoff;
- `original_memo_date` does not match the supplied cutoff;
- `stale_after` is not later than `refresh_date`;
- event is not material to a named thesis variable;
- no new source evidence is added;
- new event evidence source IDs do not appear in the updated evidence log later-event rows;
- before/after action labels are missing;
- original refresh trigger quality is not evaluated;
- multiple refresh result labels are selected or no approved label is selected;
- `follow_through_gate_status` is not `pass`;
- intake checklist remains pending;
- intake checklist is missing required requirements;
- public readiness audit, gate tracker or review log are not updated before claiming release readiness.

## Release Rule

Do not mark `G04` as complete unless:

1. the completed refresh file exists;
2. `scripts/validate_follow_through_refresh.py` exits 0;
3. `public-release-gate-tracker.csv` points G04 to the completed refresh file;
4. `scripts/validate_long_term_release.py` exits 0 after the gate tracker is updated.
