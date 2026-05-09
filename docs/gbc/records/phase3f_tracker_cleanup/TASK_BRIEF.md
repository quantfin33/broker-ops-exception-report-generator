# GBC Task Brief - Phase 3F Tracker Cleanup

## Goal

Correct the project tracker and PDF so Phase 3 core exception pipeline completion is clear before Phase 4A is committed.

## Background

Phase 4A exception-log work exists locally and is valid because it depends on Phase 3C through Phase 3E exception objects. The tracker still showed unchecked Phase 3 items, which made it look like Phase 4 had advanced before Phase 3 was complete.

## In Scope

- Clarify that Phase 3 core exception pipeline is complete.
- Mark timestamp normalization as a deferred optional validation enhancement.
- Clarify duplicate IDs and missing required fields are validation failures, not exception-log rows.
- Clarify abnormal symbol activity belongs to later by-symbol statistics.
- Clarify market-event overlap belongs to later enrichment.
- Mark Phase 4A as local work-in-progress, not locked.
- Regenerate the project-plan PDF.

## Out Of Scope

- Source code changes.
- Test changes.
- Report logic changes.
- New validation logic.
- New exception rules.
- New report outputs.
- Phase 4A commit.
- Edits to Phase 4A implementation files, generated `order_exception_log.csv`, or Phase 4A GBC records.

## Acceptance Criteria

- [x] Tracker clearly states Phase 3 core exception pipeline is complete.
- [x] Phase 4A remains local/unlocked in the tracker.
- [x] Phase 4 report outputs remain unchecked until locked.
- [x] Phase 4A implementation files remain untouched.
- [x] Project-plan PDF is regenerated.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, or private account data.
