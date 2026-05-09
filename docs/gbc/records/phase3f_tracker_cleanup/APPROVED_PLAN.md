# GBC Approved Plan - Phase 3F Tracker Cleanup

## Goal

Perform a documentation-only sequencing correction before Phase 4A is committed.

## In Scope

- Update `docs/BROKER_OPS_PROJECT_PLAN.md`.
- Update `docs/DATA_SCHEMA.md` with a short sequencing note.
- Update `docs/gbc/AUDIT_LEDGER.md`.
- Add Phase 3F GBC records.
- Regenerate `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`.

## Out Of Scope

- Source code edits.
- Test edits.
- Phase 4A implementation edits.
- Generated exception-log edits.
- Phase 4A GBC record edits.
- Commit.

## Affected Surfaces

- `docs/BROKER_OPS_PROJECT_PLAN.md`
- `docs/DATA_SCHEMA.md`
- `docs/gbc/AUDIT_LEDGER.md`
- `docs/gbc/records/phase3f_tracker_cleanup/`
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf`

## Verification Plan

```bash
git status --short --untracked-files=all
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report --help
rg -n 'Phase 3|Phase 3F|Normalize timestamps|duplicate ID|missing required|abnormal symbol|market-event overlap|Phase 4A|order_exception_log' docs/BROKER_OPS_PROJECT_PLAN.md docs/DATA_SCHEMA.md docs/gbc/AUDIT_LEDGER.md
git status --short --untracked-files=all
```

## Risks

- Do not mix Phase 3F docs cleanup with Phase 4A source/test/output changes.
- Do not make the tracker claim Phase 4A is locked before its commit.

## Human Approval

- Approved by: user prompt
- Date: 2026-05-09
