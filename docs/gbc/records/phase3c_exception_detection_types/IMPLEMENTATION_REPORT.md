# GBC Implementation Report - Phase 3C Exception Detection Types

## Summary

Added internal deterministic exception-type detection for the six approved Phase 3C broker operations cases. The implementation reads schema-valid static order rows and returns typed exception records only.

## Files Changed

- `src/broker_ops_report/exceptions.py`: added `BrokerException`, `detect_exceptions`, and row-level rule checks.
- `tests/test_exceptions.py`: added tests for all Phase 3C exception types and scope boundaries.
- `docs/BROKER_OPS_PROJECT_PLAN.md`: marked Phase 3C exception types complete and left later exception/reporting work unchecked.
- `docs/DATA_SCHEMA.md`: documented the Phase 3C exception type definitions.
- `docs/gbc/AUDIT_LEDGER.md`: added the Phase 3C audit entry.
- `docs/gbc/records/phase3c_exception_detection_types/`: added GBC records.
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`: regenerated from the updated plan.

## Behavior Added Or Updated

- Detects `received_not_transmitted`.
- Detects `transmitted_no_final_status`.
- Detects `rejected_without_reason`.
- Detects `bridge_failed_or_disconnected`.
- Detects `high_latency`.
- Detects `pending_follow_up`.

## Scope Control

- No CLI command was added.
- No output report files are generated.
- No severity classification or recommended actions were implemented.
- No by-symbol statistics, market-event overlap logic, abnormal symbol activity, pandas, external dependency, or live integration was added.

## Notes

- A single order row may produce more than one exception type.
- Duplicate ID and lifecycle problems remain validation concerns from Phase 3B, not Phase 3C broker exception report rows.
