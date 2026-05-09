# GBC Implementation Report - Phase 4C By-Symbol Trading Stats

## Files Changed

- `src/broker_ops_report/reporting.py`: added the Phase 4C by-symbol stats CSV writer.
- `src/broker_ops_report/cli.py`: added `generate-reports --report symbol-stats`.
- `tests/test_reporting.py`: added output contract and validation-failure tests for symbol stats.
- `outputs/by_symbol_trading_stats.csv`: generated the canonical Phase 4C output.
- `docs/BROKER_OPS_PROJECT_PLAN.md`: marked Phase 4C by-symbol stats complete.
- `docs/DATA_SCHEMA.md`: documented the Phase 4C output columns.
- `docs/gbc/AUDIT_LEDGER.md`: added the Phase 4C entry.
- `docs/gbc/records/phase4c_by_symbol_stats/`: recorded the GBC cycle.
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`: regenerated from the updated tracker.

## Behavior Added

- The CLI can generate `outputs/by_symbol_trading_stats.csv` from validated static inputs.
- The writer aggregates one row per symbol.
- Counts tie to 20 source order rows, 14 existing exception records, 4 Critical exceptions, and 10 Warning exceptions.

## Scope Controls

- No Markdown report was generated.
- No Excel or HTML output was generated.
- No market-event overlap logic or abnormal-symbol flag was added.
- No new exception type was added.
- No pandas, external dependency, live API, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, `.env`, browser-session, or real client/account data was added.

