# GBC Approved Plan - Phase 4B.1 Tracker Sync

## Plan

1. Confirm the working tree is clean.
2. Update `docs/BROKER_OPS_PROJECT_PLAN.md` to mark the Phase 4B shift summary JSON output complete/locked.
3. Append a Phase 4B.1 tracker-sync entry to `docs/gbc/AUDIT_LEDGER.md`.
4. Create this `docs/gbc/records/phase4b_tracker_sync/` record set.
5. Regenerate `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf` using the existing project script.
6. Run the requested test and CLI help checks.
7. Stage and commit only the tracker-sync files.

## Allowed Files

- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase4b_tracker_sync/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`

## Protected Files

- `src/broker_ops_report/cli.py`
- `src/broker_ops_report/reporting.py`
- `tests/test_reporting.py`
- `outputs/order_exception_log.csv`
- `outputs/broker_ops_shift_summary.json`
- Phase 4C/4D outputs
- `README.md`

