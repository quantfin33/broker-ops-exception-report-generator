# GBC Task Brief - Phase 3C Exception Detection Types

## Goal

Implement deterministic broker exception detection types from the already schema-valid static order fixture.

## Background

Phase 3A validates CSV schema and core fields. Phase 3B validates duplicate order IDs and lifecycle consistency. Phase 3C adds internal exception-type detection only, without report generation or ranking.

## In Scope

- Add an internal `BrokerException` data structure.
- Detect `received_not_transmitted`.
- Detect `transmitted_no_final_status`.
- Detect `rejected_without_reason`.
- Detect `bridge_failed_or_disconnected`.
- Detect `high_latency`.
- Detect `pending_follow_up`.
- Add focused tests for each exception type.
- Update Phase 3C docs, audit ledger, project plan, and project-plan PDF.

## Out Of Scope

- Severity classification.
- Recommended actions.
- Broker report generation.
- By-symbol statistics.
- Market-event overlap logic.
- Abnormal symbol activity.
- Duplicate ID, missing-field, or lifecycle exception report rows.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, or `.env` dependencies.
- README edits.
- Commit.

## Acceptance Criteria

- [x] Canonical fixtures still validate successfully.
- [x] Each Phase 3C exception type is detected by tests.
- [x] Returned exceptions include event id, symbol, status, bridge status, and detail.
- [x] No severity or recommended-action fields exist yet.
- [x] Exception detection does not write output files.
- [x] Full unit test suite passes.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, or private account data.
