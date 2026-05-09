# GBC Approved Plan - Phase 4C By-Symbol Trading Stats

## Implementation Plan

1. Run artifact-lock preflight for Phase 4A and Phase 4B outputs.
2. Inspect current CLI, reporting, exception, validation, tests, schema docs, and sample order data.
3. Add `SYMBOL_STATS_FILENAME`, `SYMBOL_STATS_HEADERS`, `SymbolStatsResult`, and `write_by_symbol_trading_stats()` to `src/broker_ops_report/reporting.py`.
4. Reuse `validate_inputs()` and `detect_exceptions()` instead of duplicating validation or exception logic.
5. Aggregate source rows by symbol with deterministic alphabetical row order.
6. Update `generate-reports --report symbol-stats` in `src/broker_ops_report/cli.py`.
7. Add focused tests in `tests/test_reporting.py`.
8. Generate `outputs/by_symbol_trading_stats.csv`.
9. Update Phase 4C docs, audit ledger, project tracker, and project-plan PDF.
10. Run full verification and stop without committing.

## Approved Output Columns

`symbol`, `asset_class`, `total_orders`, `filled_orders`, `rejected_orders`, `failed_orders`, `pending_or_open_orders`, `total_volume`, `average_latency_ms`, `max_latency_ms`, `total_pnl_usd`, `exception_count`, `critical_exception_count`, `warning_exception_count`

## Files In Scope

- `src/broker_ops_report/reporting.py`
- `src/broker_ops_report/cli.py`
- `tests/test_reporting.py`
- `outputs/by_symbol_trading_stats.csv`
- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/DATA_SCHEMA.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase4c_by_symbol_stats/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`

## Files Out Of Scope

- Static CSV fixture changes.
- Existing validation and exception detection logic.
- Markdown shift report.
- Excel or HTML output.
- README.
- Market-event overlap logic.
- Live integration code or credentials.

