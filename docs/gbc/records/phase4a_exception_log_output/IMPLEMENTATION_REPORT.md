# GBC Implementation Report - Phase 4A Exception Log Output

## Summary

Added the first structured report output: deterministic `order_exception_log.csv` generation from validated static inputs and existing exception records.

## Files Changed

- `src/broker_ops_report/reporting.py`: added the Phase 4A CSV writer.
- `src/broker_ops_report/cli.py`: added `generate-reports --report exception-log`.
- `tests/test_reporting.py`: added output contract and validation-failure tests.
- `docs/BROKER_OPS_PROJECT_PLAN.md`: marked only the exception log output complete.
- `docs/DATA_SCHEMA.md`: documented the exception-log columns.
- `docs/gbc/AUDIT_LEDGER.md`: added the Phase 4A audit entry.
- `docs/gbc/records/phase4a_exception_log_output/`: added GBC records.
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`: regenerated from the updated plan.

## Behavior Added Or Updated

- `generate-reports --report exception-log` validates inputs, detects existing exceptions, and writes `outputs/order_exception_log.csv`.
- Validation failure returns non-zero and does not write the exception log.

## Scope Control

- No JSON summary, by-symbol statistics, Markdown report, Excel output, HTML output, market-event overlap logic, duplicate-ID exception reporting, or missing-field exception reporting was added.
- No pandas, external dependency, live API, MT4/MT5, FIX, bridge, Binance, Telegram, TradingView, account, credential, `.env`, or browser-session dependency was added.

## Notes

- The no-argument `generate-reports` placeholder remains available for non-Phase-4A report modes.
