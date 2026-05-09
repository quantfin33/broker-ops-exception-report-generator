# GBC Approved Plan - Phase 2 Static Demo Data

## Goal

Add static synthetic CSV fixtures and schema documentation without implementing validation or exception rules.

## In Scope

- Add one order-events CSV with the required 24 columns and synthetic rows.
- Add one market-events CSV with the required 6 columns and synthetic rows.
- Document both CSVs in `docs/DATA_SCHEMA.md`.
- Add fixture-only `unittest` coverage.
- Update Phase 2 project-plan checklist, audit ledger, GBC records, and regenerated project-plan PDF.

## Out Of Scope

- CSV parsing in application code.
- Data validation behavior.
- Exception classification behavior.
- Report output generation.
- New dependencies or live integrations.

## Affected Surfaces

- `data/`
- `docs/`
- `tests/`
- project-plan PDF under `outputs/`

## Verification Plan

- Run `PYTHONPATH=src python3 -m unittest discover`.
- Run `PYTHONPATH=src python3 -m broker_ops_report --help`.
- Inspect `head -5 data/sample_order_events.csv`.
- Inspect `head -5 data/sample_market_events.csv`.
- Confirm `data/` contains only `.gitkeep` and the two sample CSV fixtures.
- Confirm `outputs/` contains only `.gitkeep` and the project-plan PDF.

## Risks

- The fixture rows are intentionally imperfect. Later validation code must treat those imperfections as expected test cases, not accidental data quality failures.

## Human Approval

- Approved by: User request in this thread.
- Date: 2026-05-08.
