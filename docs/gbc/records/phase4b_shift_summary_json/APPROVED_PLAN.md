# GBC Approved Plan - Phase 4B Shift Summary JSON

## Implementation Plan

1. Inspect the current Phase 4A reporting code, CLI, tests, and locked project tracker.
2. Add `SHIFT_SUMMARY_FILENAME` and `ShiftSummaryResult` in `src/broker_ops_report/reporting.py`.
3. Add `write_broker_ops_shift_summary()` that:
   - validates inputs first;
   - reads static order and market-event rows;
   - reuses `detect_exceptions()`;
   - builds deterministic order, validation, severity, exception, unresolved-item, output-file, and non-claim sections;
   - writes only `broker_ops_shift_summary.json`.
4. Update `src/broker_ops_report/cli.py` so `generate-reports --report shift-summary` calls the new writer.
5. Add tests in `tests/test_reporting.py` for the JSON output contract, deterministic regeneration, validation failure behavior, and absence of other report outputs.
6. Generate `outputs/broker_ops_shift_summary.json` from canonical fixtures.
7. Verify tests, CLI help, JSON parsing, count tie-outs, and SHA-256 reproducibility.
8. Stage and commit only Phase 4B files if all checks pass.

## Files In Scope

- `src/broker_ops_report/reporting.py`
- `src/broker_ops_report/cli.py`
- `tests/test_reporting.py`
- `outputs/broker_ops_shift_summary.json`
- `docs/gbc/records/phase4b_shift_summary_json/`

## Files Out Of Scope

- Static data fixtures.
- Existing validation and exception detection logic.
- `outputs/order_exception_log.csv` unless only checked for stability.
- README.
- Phase 4C/4D report outputs.
- Project tracker/PDF unless a separate tracker sync is requested.

## Verification Commands

```bash
git status --short --untracked-files=all
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report shift-summary --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
```

