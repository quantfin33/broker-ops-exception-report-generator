# GBC Task Brief - Phase 3E Recommended Actions

## Goal

Add deterministic recommended-action mapping to the six existing typed and severity-classified broker exceptions.

## Background

Phase 3C added internal exception-type detection. Phase 3D added severity. Phase 3E adds recommended actions only, still without report generation.

## In Scope

- Add `recommended_action` to internal `BrokerException` records.
- Map each of the six existing exception types to the approved action text.
- Add tests for all recommended-action mappings.
- Confirm canonical exception count and severity counts remain stable.
- Update Phase 3E docs, audit ledger, project tracker, and project-plan PDF.

## Out Of Scope

- Broker report generation.
- JSON, CSV, or Markdown output files.
- By-symbol statistics.
- Market-event overlap logic.
- Duplicate-ID exception reporting.
- Missing-field exception reporting.
- External dependencies.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, `.env`, or browser-session dependencies.
- README edits.
- Commit.

## Acceptance Criteria

- [x] Every existing exception type has the approved recommended action.
- [x] All canonical fixture exceptions include `recommended_action`.
- [x] Canonical exception count remains 14.
- [x] Severity counts remain `Critical: 4`, `Warning: 10`, `Info: 0`.
- [x] No report files are generated.
- [x] Full unit test suite passes.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, or private account data.
