# GBC Approved Plan - Phase 3E Recommended Actions

## Goal

Add recommended-action mapping to the six existing exception types only.

## In Scope

- Update `src/broker_ops_report/exceptions.py` with a recommended-action mapping and `recommended_action` field.
- Update `tests/test_exceptions.py` with recommended-action tests and stability checks.
- Update `docs/BROKER_OPS_PROJECT_PLAN.md`, `docs/DATA_SCHEMA.md`, and `docs/gbc/AUDIT_LEDGER.md`.
- Add Phase 3E GBC records.
- Regenerate `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`.

## Out Of Scope

- Report output files.
- By-symbol statistics.
- Market-event overlap.
- Duplicate-ID or missing-field exception reporting.
- External dependencies or live integrations.
- README edits.
- Commit.

## Affected Surfaces

- `src/broker_ops_report/exceptions.py`
- `tests/test_exceptions.py`
- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/DATA_SCHEMA.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase3e_recommended_actions/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`

## Verification Plan

```bash
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --help
```

Also inspect `outputs/`, `pyproject.toml`, `git status --short --untracked-files=all`, and canonical exception/action coverage.

## Risks

- Keep recommended actions as internal triage metadata only; do not generate report artifacts yet.
- Keep severity mapping unchanged from Phase 3D.

## Human Approval

- Approved by: user prompt
- Date: 2026-05-09
