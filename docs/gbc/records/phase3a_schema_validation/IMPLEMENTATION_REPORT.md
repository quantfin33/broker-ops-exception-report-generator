# GBC Implementation Report - Phase 3A CSV Schema Validation

## Summary

Implemented structural CSV validation for static order-event and market-event fixtures using only the Python standard library. The `validate-inputs` command now validates current fixtures and exits non-zero on schema/field/type errors.

## Files Changed

- `src/broker_ops_report/schema.py`: schema constants.
- `src/broker_ops_report/validation.py`: validation result/issue types and validation checks.
- `src/broker_ops_report/cli.py`: functional `validate-inputs` command.
- `tests/test_validation.py`: validation unit and CLI tests.
- `tests/test_cli.py`: updated CLI expectations after `validate-inputs` became functional.
- `data/sample_order_events.csv` and `docs/DATA_SCHEMA.md`: adjusted `evt_0013` so primary fixtures are structurally valid.

## Behavior Added Or Updated

- `validate-inputs` checks files, headers, required fields, allowed values, UTC-style timestamps, numeric parsing, market-event `related_symbols`, and obvious secret/live credential patterns.
- `generate-reports` and `run-demo` remain placeholders.
- No output report files are generated.

## Scope Control

- No broker exception rules were implemented.
- No by-symbol statistics or market-event overlap logic was implemented.
- No pandas, external dependency, live API, MT4/MT5, FIX, bridge, Binance, Telegram, TradingView, account, or credential dependency was added.

## Notes

- Phase 3B should handle lifecycle consistency and duplicate ID validation as a separate bounded task.
