# GBC Task Brief - Phase 3D Severity Classification

## Goal

Add deterministic severity classification to the six existing broker exception types.

## Background

Phase 3C added internal exception-type detection. Phase 3D adds a severity field only. Recommended actions, report generation, by-symbol statistics, and market-event overlap remain out of scope.

## In Scope

- Add `severity` to internal `BrokerException` records.
- Map `received_not_transmitted`, `transmitted_no_final_status`, and `bridge_failed_or_disconnected` to `Critical`.
- Map `rejected_without_reason`, `high_latency`, and `pending_follow_up` to `Warning`.
- Keep an `Info` fallback for unknown exception types.
- Add tests for all severity mappings.
- Update Phase 3D docs, audit ledger, project tracker, and project-plan PDF.

## Out Of Scope

- Recommended actions.
- Broker report generation.
- By-symbol statistics.
- Market-event overlap logic.
- Duplicate-ID exception reporting.
- Missing-field exception reporting.
- External dependencies.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, or `.env` dependencies.
- README edits.
- Commit.

## Acceptance Criteria

- [x] All six existing exception types receive the approved severity.
- [x] All canonical fixture exceptions include severity.
- [x] No exception includes `recommended_action`.
- [x] Exception detection does not write output files.
- [x] Full unit test suite passes.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, or private account data.
