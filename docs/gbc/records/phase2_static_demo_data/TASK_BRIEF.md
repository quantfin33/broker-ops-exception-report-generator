# GBC Task Brief - Phase 2 Static Demo Data

## Goal

Create controlled static CSV fixtures and schema documentation for the Broker Operations Exception Report Generator.

## Background

Phase 0 and Phase 1 are locked in the initial scaffold commit. The project currently has a placeholder CLI and no business logic. Phase 2 adds only fixture data and fixture tests for later validation, exception-rule, and reporting work.

## In Scope

- Create `data/sample_order_events.csv`.
- Create `data/sample_market_events.csv`.
- Create `docs/DATA_SCHEMA.md`.
- Add fixture-only tests for files, headers, scenario rows, obvious secret/private account patterns, and no live dependency.
- Update the Phase 2 checklist only.
- Regenerate the project-plan PDF.

## Out Of Scope

- Validation logic.
- Exception detection rules.
- Final broker report outputs.
- Pandas or external dependencies.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, or account dependencies.
- Phase 3 work.

## Acceptance Criteria

- [x] Required CSV files exist.
- [x] Required headers are present in the requested order.
- [x] Fixture rows cover the requested future test scenarios.
- [x] Documentation explains columns, allowed values, UTC convention, imperfect rows, and non-claims.
- [x] Fixture-only tests pass.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, private logs, or private account data.
