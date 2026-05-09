# GBC Approved Plan - Phase 4A Exception Log Output

## Goal

Generate only `outputs/order_exception_log.csv` from validated static inputs.

## In Scope

- Add `src/broker_ops_report/reporting.py`.
- Update `generate-reports` with `--report exception-log`.
- Validate inputs before writing the CSV.
- Add focused tests for the exception-log command and output contract.
- Update `docs/BROKER_OPS_PROJECT_PLAN.md`, `docs/DATA_SCHEMA.md`, and `docs/gbc/AUDIT_LEDGER.md`.
- Add Phase 4A GBC records.
- Regenerate `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`.

## Out Of Scope

- `broker_ops_shift_summary.json`.
- `by_symbol_trading_stats.csv`.
- `broker_ops_shift_report.md`.
- Excel or HTML output.
- Market-event overlap.
- Duplicate-ID or missing-field exception reporting.
- External dependencies or live integrations.
- README edits.
- Commit.

## Affected Surfaces

- `src/broker_ops_report/reporting.py`
- `src/broker_ops_report/cli.py`
- `tests/test_reporting.py`
- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/DATA_SCHEMA.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase4a_exception_log_output/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`
- `outputs/order_exception_log.csv`

## Verification Plan

```bash
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report exception-log --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report generate-reports --help
```

Also inspect output file counts, severity counts, recommended-action coverage, `pyproject.toml`, and `git status --short --untracked-files=all`.

## Risks

- Do not let Phase 4A generate later report artifacts.
- Keep report rows tied to existing exception objects only.

## Human Approval

- Approved by: user prompt
- Date: 2026-05-09
