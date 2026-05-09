# GBC Implementation Report - Phase 3E Recommended Actions

## Summary

Added deterministic recommended-action mapping to the six existing broker exception types. The implementation keeps exception records internal and does not generate reports.

## Files Changed

- `src/broker_ops_report/exceptions.py`: added recommended-action mapping, `recommended_action` field, and lookup helper.
- `tests/test_exceptions.py`: added recommended-action tests and canonical stability checks.
- `docs/BROKER_OPS_PROJECT_PLAN.md`: marked recommended actions complete.
- `docs/DATA_SCHEMA.md`: documented the recommended-action mapping.
- `docs/gbc/AUDIT_LEDGER.md`: added the Phase 3E audit entry.
- `docs/gbc/records/phase3e_recommended_actions/`: added GBC records.
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`: regenerated from the updated plan.

## Behavior Added Or Updated

- `received_not_transmitted` now includes the approved queue/routing review action.
- `transmitted_no_final_status` now includes the approved downstream execution follow-up action.
- `rejected_without_reason` now includes the approved missing-reason investigation action.
- `bridge_failed_or_disconnected` now includes the approved platform/risk/technical escalation action.
- `high_latency` now includes the approved latency review action.
- `pending_follow_up` now includes the approved shift-handover action.

## Scope Control

- No broker reports were generated.
- No by-symbol statistics, market-event overlap logic, duplicate-ID exception reporting, or missing-field exception reporting was added.
- No pandas, external dependency, live API, MT4/MT5, FIX, bridge, Binance, Telegram, TradingView, account, credential, `.env`, or browser-session dependency was added.

## Notes

- Unknown exception types fail clearly for recommended-action lookup.
