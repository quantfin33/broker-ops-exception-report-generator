# GBC Task Brief - Phase 4B Shift Summary JSON

## Goal

Generate `outputs/broker_ops_shift_summary.json` from the existing static CSV fixtures and the existing validation and exception pipeline.

## Background

Phase 4A locked `outputs/order_exception_log.csv`. Phase 4B adds only the machine-readable shift summary JSON so later report outputs remain isolated.

## In Scope

- Add a standard-library JSON report writer.
- Implement `generate-reports --report shift-summary`.
- Validate inputs before writing.
- Reuse existing exception objects, severity, and recommended actions.
- Write only `outputs/broker_ops_shift_summary.json`.
- Add focused tests for JSON structure, counts, non-claims, validation failure behavior, and deterministic regeneration.

## Out Of Scope

- By-symbol trading statistics CSV.
- Markdown shift report.
- Excel or HTML output.
- Market-event enrichment.
- Timestamp normalization.
- Duplicate-ID or missing-field exception rows.
- New exception types.
- Severity or recommended-action changes.
- External dependencies.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, `.env`, or browser-session dependencies.
- README edits.

## Acceptance Criteria

- [x] `generate-reports --report shift-summary` exits 0 for canonical fixtures.
- [x] `broker_ops_shift_summary.json` parses as JSON.
- [x] Total exceptions tie out to the existing 14 exception objects.
- [x] Severity counts remain `Critical: 4`, `Warning: 10`, `Info: 0`.
- [x] Exception type breakdown is deterministic.
- [x] Validation failures are not written as exception rows.
- [x] Static-demo non-claims are present.
- [x] No Phase 4C, Phase 4D, Excel, README, or live integration work is added.

