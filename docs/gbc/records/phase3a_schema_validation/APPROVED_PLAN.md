# GBC Approved Plan - Phase 3A CSV Schema Validation

## Goal

Implement standard-library-only structural validation for the static CSV fixtures.

## In Scope

- Add `schema.py` constants for headers, required fields, allowed values, timestamp fields, numeric fields, and secret scan patterns.
- Add `validation.py` with `ValidationIssue`, `ValidationResult`, and `validate_inputs`.
- Update `validate-inputs` CLI to print success/error summaries and return appropriate exit codes.
- Make the primary sample order CSV structurally valid by filling `evt_0013.symbol` with a synthetic value.
- Move missing-field coverage into temporary test fixtures.
- Update Phase 3A docs, GBC records, audit ledger, and regenerated project-plan PDF.

## Out Of Scope

- Exception detection.
- Lifecycle consistency.
- Duplicate ID checks.
- Report generation.
- New dependencies or live integrations.

## Affected Surfaces

- `src/broker_ops_report/`
- `tests/`
- `data/sample_order_events.csv`
- `docs/`
- project-plan PDF under `outputs/`

## Verification Plan

- `PYTHONPATH=src python3 -m unittest discover`
- `PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv`
- `PYTHONPATH=src python3 -m broker_ops_report --help`
- `PYTHONPATH=src python3 -m broker_ops_report validate-inputs --help`
- Inspect `git status --short`.
- Confirm no report files were generated.

## Risks

- The primary fixtures are now structurally valid. Intentionally invalid cases for missing required fields must be maintained in temporary test fixtures.

## Human Approval

- Approved by: User request in this thread.
- Date: 2026-05-09.
