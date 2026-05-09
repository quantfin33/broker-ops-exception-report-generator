# GBC Task Brief - Phase 3A CSV Schema Validation

## Goal

Make the `validate-inputs` CLI command structurally validate the static CSV fixtures without applying broker exception rules or generating reports.

## Background

Phase 2 locked controlled static CSV fixtures. Phase 3A validates file existence, headers, required core fields, enum values, UTC-style timestamp fields, numeric fields, market-event fields, and obvious secret/live credential patterns using only the Python standard library.

## In Scope

- Add schema constants.
- Add structural CSV validation helpers.
- Make `validate-inputs` functional.
- Adjust the primary order fixture so it is structurally valid.
- Add temporary-fixture tests for invalid cases.
- Update Phase 3A GBC records, audit ledger, project checklist, and project-plan PDF.

## Out Of Scope

- Broker exception detection rules.
- Lifecycle consistency rules.
- Duplicate ID validation.
- By-symbol statistics.
- Market-event overlap logic.
- Broker report generation.
- Pandas or external dependencies.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, or credential dependencies.

## Acceptance Criteria

- [x] Current fixture files validate successfully.
- [x] Bad temporary fixtures fail with clear errors.
- [x] `validate-inputs` exits `0` for current fixtures.
- [x] `validate-inputs` exits non-zero for bad temporary fixtures.
- [x] Tests cover missing columns, invalid enums, missing core fields, invalid timestamps, invalid numeric fields, missing market-event columns, and no live dependency.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, private logs, or private account data.
