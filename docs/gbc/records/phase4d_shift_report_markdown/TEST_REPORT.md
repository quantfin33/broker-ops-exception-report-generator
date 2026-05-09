# GBC Test Report - Phase 4D Broker Ops Shift Report Markdown

## Commands Run

```bash
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --orders data/sample_order_events.csv --market-events data/sample_market_events.csv
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report exception-log --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report shift-summary --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report symbol-stats --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report generate-reports --report shift-report --orders data/sample_order_events.csv --market-events data/sample_market_events.csv --output-dir outputs
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report generate-reports --help
```

## Results

- Full test suite passed 76 tests.
- `validate-inputs` returned exit code 0.
- All four approved report commands returned exit code 0.
- Markdown report contained all required sections and non-claims.

## Artifact Checks

- `outputs/broker_ops_shift_report.md` exists.
- `outputs/order_exception_log.csv` exists.
- `outputs/broker_ops_shift_summary.json` exists.
- `outputs/by_symbol_trading_stats.csv` exists.
- No Excel or HTML output exists.

## Gaps

Final integration-check phase, README, and portfolio evidence remain deferred.

