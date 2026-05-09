# GBC Approved Plan - Phase 3D Severity Classification

## Goal

Add severity classification to the six existing exception types only.

## In Scope

- Update `src/broker_ops_report/exceptions.py` with a severity mapping and `severity` field.
- Update `tests/test_exceptions.py` with severity mapping tests.
- Update `docs/BROKER_OPS_PROJECT_PLAN.md`, `docs/DATA_SCHEMA.md`, and `docs/gbc/AUDIT_LEDGER.md`.
- Add Phase 3D GBC records.
- Regenerate `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`.

## Out Of Scope

- `recommended_action`.
- Report output files.
- By-symbol statistics.
- Market-event overlap.
- Duplicate-ID or missing-field exception reporting.
- External dependencies or live integrations.
- README edits.

## Affected Surfaces

- `src/broker_ops_report/exceptions.py`
- `tests/test_exceptions.py`
- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/DATA_SCHEMA.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase3d_severity_classification/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`

## Verification Plan

```bash
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --help
```

Also inspect `outputs/`, `pyproject.toml`, `git status --short`, and canonical severity counts.

## Risks

- Keep severity as classification only; do not imply final reporting is complete.
- Keep recommended actions absent until a separately approved phase.

## Human Approval

- Approved by: user prompt
- Date: 2026-05-09
