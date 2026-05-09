# GBC Approved Plan - Phase 3B Lifecycle And Duplicate Validation

## Goal

Implement duplicate ID and lifecycle consistency validation only.

## In Scope

- Update canonical fixture duplicate examples into unique synthetic IDs.
- Add lifecycle status groups to `schema.py`.
- Add duplicate ID validation and lifecycle consistency validation to `validation.py`.
- Add tests for duplicate IDs, blank optional server IDs, lifecycle timestamp ordering, missing executed prices, and missing transmitted/final timestamps.
- Update `docs/DATA_SCHEMA.md`, project checklist, audit ledger, GBC records, and regenerated project-plan PDF.

## Out Of Scope

- Exception rules.
- Severity/actions.
- Report generation.
- By-symbol statistics.
- Market-event overlap logic.
- New dependencies or live integrations.

## Affected Surfaces

- `data/sample_order_events.csv`
- `src/broker_ops_report/`
- `tests/test_validation.py`
- `docs/`
- project-plan PDF under `outputs/`

## Verification Plan

- `PYTHONPATH=src python3 -m unittest discover`
- `PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv`
- `PYTHONPATH=src python3 -m broker_ops_report --help`
- `PYTHONPATH=src python3 -m broker_ops_report validate-inputs --help`
- Inspect `git status --short`.
- Confirm `outputs/` contains only `.gitkeep` and the project-plan PDF.

## Risks

- Canonical fixtures must remain valid. Duplicate and lifecycle-failure examples belong only in temporary test fixtures.

## Human Approval

- Approved by: User request in this thread.
- Date: 2026-05-09.
