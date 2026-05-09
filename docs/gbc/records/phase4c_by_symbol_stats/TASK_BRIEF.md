# GBC Task Brief - Phase 4C By-Symbol Trading Stats

## Goal

Generate `outputs/by_symbol_trading_stats.csv` from the existing validated static order fixture and existing exception records.

## Background

Phase 4A locked the exception log CSV and Phase 4B locked the shift summary JSON. Phase 4C adds only the by-symbol trading statistics CSV.

## In Scope

- Add standard-library by-symbol CSV generation.
- Implement `generate-reports --report symbol-stats`.
- Validate inputs before writing.
- Aggregate order counts, volume, latency, P&L, and existing exception counts by symbol.
- Write only `outputs/by_symbol_trading_stats.csv`.
- Add focused tests for headers, row counts, total tie-outs, severity tie-outs, numeric fields, sorted symbols, and absence of Markdown/Excel/HTML output.
- Update Phase 4C tracker/docs/GBC records and regenerate the project-plan PDF.

## Out Of Scope

- Markdown shift report.
- Excel or HTML output.
- Market-event overlap logic.
- Abnormal-symbol activity flags.
- New exception types.
- Pandas or external dependencies.
- README edits.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, `.env`, browser-session, or real client/account data.
- Commit.

## Acceptance Criteria

- [x] `generate-reports --report symbol-stats` exits 0 for canonical fixtures.
- [x] `by_symbol_trading_stats.csv` has the approved headers.
- [x] One output row exists per unique symbol.
- [x] Symbols are sorted alphabetically.
- [x] Total orders tie to 20 source rows.
- [x] Exception counts tie to 14 existing exception records.
- [x] Severity counts tie to `Critical: 4` and `Warning: 10`.
- [x] No Markdown, Excel, HTML, market-event overlap, or live integration work is added.

