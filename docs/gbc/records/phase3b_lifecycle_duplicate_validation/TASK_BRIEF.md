# GBC Task Brief - Phase 3B Lifecycle And Duplicate Validation

## Goal

Extend CSV validation to catch duplicate nonblank order IDs and lifecycle consistency contradictions in the static fixture data.

## Background

Phase 3A validates structural schema, required fields, enum values, timestamps, numeric fields, and secret patterns. Phase 3B adds data consistency validation only. It does not produce broker exception reports or business exception classifications.

## In Scope

- Make canonical fixture order IDs unique.
- Validate duplicate nonblank `client_order_id`.
- Validate duplicate nonblank `server_order_id`.
- Ignore blank `server_order_id` values for duplicate checks.
- Validate lifecycle-required timestamps and executed prices.
- Validate timestamp ordering.
- Add temporary bad-fixture tests for duplicate and lifecycle failures.
- Update schema docs, project checklist, audit ledger, GBC records, and project-plan PDF.

## Out Of Scope

- Broker exception detection rules.
- Severity classification.
- Recommended actions.
- By-symbol statistics.
- Market-event overlap logic.
- Broker report generation.
- Pandas or external dependencies.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, or credential dependencies.

## Acceptance Criteria

- [x] Canonical fixtures validate successfully.
- [x] Duplicate client-order and server-order IDs fail in temporary bad fixtures.
- [x] Blank server-order IDs do not fail duplicate validation.
- [x] Lifecycle timestamp and executed-price contradictions fail.
- [x] Rejected, cancelled, and expired rows without executed prices can pass lifecycle validation.
- [x] No exception rules, reports, severity, or recommended actions are added.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, private logs, or private account data.
