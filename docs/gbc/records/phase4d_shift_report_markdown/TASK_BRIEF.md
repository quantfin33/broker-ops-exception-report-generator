# GBC Task Brief - Phase 4D Broker Ops Shift Report Markdown

## Goal

Generate `outputs/broker_ops_shift_report.md` as the human-readable broker operations shift report.

## Background

Phase 4A, 4B, and 4C locked the exception log CSV, shift summary JSON, and by-symbol stats CSV. Phase 4D renders those same validated structures into a deterministic Markdown report.

## In Scope

- Add standard-library Markdown report generation.
- Implement `generate-reports --report shift-report`.
- Validate inputs before writing.
- Include input files, order activity summary, exception summary, severity breakdown, items requiring review, by-symbol summary, shift handover notes, and limitations/non-claims.
- Write only `outputs/broker_ops_shift_report.md`.
- Add tests for required sections, counts, non-claims, validation failure behavior, and absence of Excel/HTML output.
- Update Phase 4D docs, audit ledger, project tracker, and project-plan PDF.

## Out Of Scope

- Excel output.
- HTML output.
- Market-event overlap logic.
- New exception types.
- Pandas or external dependencies.
- README edits.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, account, credential, `.env`, browser-session, real client/account data, execution claims, or trading-bot claims.

## Acceptance Criteria

- [x] `generate-reports --report shift-report` exits 0 for canonical fixtures.
- [x] `outputs/broker_ops_shift_report.md` exists.
- [x] Required sections are present.
- [x] Counts tie to 20 order rows, 5 market-event rows, 14 exceptions, `Critical: 4`, `Warning: 10`, and `Info: 0`.
- [x] Required non-claims are present.
- [x] No Excel or HTML output is created.

