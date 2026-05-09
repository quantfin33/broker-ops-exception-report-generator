# GBC Implementation Report - Phase 3D Severity Classification

## Summary

Added deterministic severity classification to the six existing broker exception types. The implementation keeps exception records internal and does not generate reports.

## Files Changed

- `src/broker_ops_report/exceptions.py`: added severity mapping, fallback, and `severity` field.
- `tests/test_exceptions.py`: added severity mapping tests and canonical severity coverage.
- `docs/BROKER_OPS_PROJECT_PLAN.md`: marked severity classification complete.
- `docs/DATA_SCHEMA.md`: documented the severity mapping.
- `docs/gbc/AUDIT_LEDGER.md`: added the Phase 3D audit entry.
- `docs/gbc/records/phase3d_severity_classification/`: added GBC records.
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`: regenerated from the updated plan.

## Behavior Added Or Updated

- `received_not_transmitted` is `Critical`.
- `transmitted_no_final_status` is `Critical`.
- `bridge_failed_or_disconnected` is `Critical`.
- `rejected_without_reason` is `Warning`.
- `high_latency` is `Warning`.
- `pending_follow_up` is `Warning`.

## Scope Control

- No recommended actions were implemented.
- No broker reports were generated.
- No by-symbol statistics, market-event overlap logic, duplicate-ID exception reporting, or missing-field exception reporting was added.
- No pandas, external dependency, live API, MT4/MT5, FIX, bridge, Binance, Telegram, TradingView, account, or credential dependency was added.

## Notes

- Unknown exception types default to `Info` to keep the classifier total and deterministic.
