# GBC Test Report - Phase 4C By-Symbol Trading Stats

## Commands Run

```bash
git status --short --untracked-files=all
git log --oneline -10
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report exception-log --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report shift-summary --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report symbol-stats --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report generate-reports --help
```

## Results

- `PYTHONPATH=src python3 -m unittest discover` passed 74 tests.
- `validate-inputs` returned exit code 0 for canonical fixtures.
- `generate-reports --report symbol-stats` returned exit code 0 and wrote `outputs/by_symbol_trading_stats.csv`.
- `generate-reports --report exception-log` and `generate-reports --report shift-summary` still returned exit code 0.
- Root CLI help and `generate-reports --help` returned exit code 0.

## Artifact Checks

- `outputs/by_symbol_trading_stats.csv` exists.
- Output has 6 symbol rows.
- Total orders tie to 20 source rows.
- Exception count ties to 14 existing exception records.
- Critical and Warning counts tie to 4 and 10.
- `outputs/order_exception_log.csv` still exists and remains valid.
- `outputs/broker_ops_shift_summary.json` still exists and remains valid.
- No Markdown, Excel, or HTML output exists.

## Gaps

Phase 4D Markdown shift report remains deferred.

