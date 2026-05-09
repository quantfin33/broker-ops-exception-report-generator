# GBC Approved Plan - Phase 4D Broker Ops Shift Report Markdown

## Implementation Plan

1. Confirm Phase 4C is committed and the working tree is clean.
2. Inspect existing CLI, reporting, tests, schema docs, and tracker files.
3. Add `SHIFT_REPORT_FILENAME`, `ShiftReportResult`, and `write_broker_ops_shift_report()` to `src/broker_ops_report/reporting.py`.
4. Reuse existing validation, exception detection, severity/recommended-action data, and by-symbol aggregation.
5. Update `generate-reports --report shift-report` in `src/broker_ops_report/cli.py`.
6. Add focused tests in `tests/test_reporting.py`.
7. Generate `outputs/broker_ops_shift_report.md`.
8. Update Phase 4D docs, GBC records, audit ledger, project tracker, and project-plan PDF.
9. Run verification and commit with `Add broker ops shift report`.

## Required Markdown Sections

- `Broker Operations Shift Report`
- `Input files used`
- `Order activity summary`
- `Exception summary`
- `Severity breakdown`
- `Items requiring review`
- `By-symbol summary`
- `Shift handover notes`
- `Limitations / non-claims`

## Required Non-Claims

- Static sample data only.
- No real client/account data.
- No live broker connection.
- No MT4/MT5 admin access.
- No execution or trading bot.

