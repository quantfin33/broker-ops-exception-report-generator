# GBC Approved Plan - Phase 3C Exception Detection Types

## Goal

Add internal broker exception type detection without severity, actions, aggregation, or report generation.

## In Scope

- Create `src/broker_ops_report/exceptions.py`.
- Add `BrokerException` with `exception_type`, order identifiers, symbol, status, bridge status, and detail.
- Add detector functions for the six approved Phase 3C exception types.
- Add `tests/test_exceptions.py`.
- Update the Phase 3 checklist, data schema notes, audit ledger, and GBC records.
- Regenerate `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`.

## Out Of Scope

- CLI report generation or a `detect-exceptions` CLI.
- Severity or recommended-action fields.
- By-symbol statistics.
- Market-event overlap.
- Abnormal symbol activity.
- Output report files.
- External dependencies or live integrations.

## Affected Surfaces

- `src/broker_ops_report/exceptions.py`
- `tests/test_exceptions.py`
- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/DATA_SCHEMA.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase3c_exception_detection_types/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`

## Verification Plan

```bash
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --help
```

Also inspect `outputs/`, `pyproject.toml`, and `git status --short`.

## Risks

- Exception detection must remain distinct from validation and report generation.
- The tracker must not imply severity, actions, by-symbol stats, or market-event overlap are complete.

## Human Approval

- Approved by: user prompt
- Date: 2026-05-09
