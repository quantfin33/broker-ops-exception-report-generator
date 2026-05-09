# Broker Operations Exception Report Generator

A static Python portfolio demo for broker operations and trading-risk support.

The project reads synthetic broker-style order/event CSV files, validates the data,
detects operational exceptions, classifies severity, attaches recommended actions,
and generates review-ready CSV, JSON, and Markdown reports.

This is not a trading strategy tool. It is a broker-control-room reporting demo:
the focus is order lifecycle review, data quality, exception handling, and shift
handover.

## Why It Matters

Broker operations teams need to spot unresolved orders, missing rejection reasons,
failed bridge/connectivity states, latency issues, and report-quality problems
before they turn into client escalations or shift handover gaps.

This project simulates the reporting layer around a broker platform, order
management system, or bridge/execution workflow using static sample data only.

## What It Demonstrates

- CSV schema validation for broker-style order and market-event files.
- Lifecycle checks for timestamps, statuses, duplicate IDs, and required fields.
- Exception detection for received-not-transmitted, transmitted-without-final-status,
  rejected-without-reason, bridge failure/disconnection, high latency, and pending
  follow-up cases.
- Severity classification: `Critical`, `Warning`, and `Info`.
- Deterministic recommended actions for operational review.
- Report generation for exception logs, shift summaries, by-symbol stats, and
  shift handover notes.
- Test coverage for validation, exception detection, CLI behavior, and generated
  report contracts.

## Inputs

- `data/sample_order_events.csv` - synthetic broker-style order/platform events.
- `data/sample_market_events.csv` - synthetic market-event awareness data.

All sample rows are fake. Account IDs, order IDs, routes, and liquidity-provider
labels are synthetic.

## Outputs

- `outputs/order_exception_log.csv` - every detected operational exception with
  severity and recommended action.
- `outputs/broker_ops_shift_summary.json` - machine-readable shift summary,
  exception counts, severity breakdown, and unresolved items.
- `outputs/by_symbol_trading_stats.csv` - one row per symbol with order counts,
  volume, latency, P&L, and exception counts.
- `outputs/broker_ops_shift_report.md` - human-readable broker operations shift
  report and handover notes.
- `outputs/Broker_Ops_Exception_Report_Project_Plan.pdf` - project plan and build
  tracker.

Excel output is intentionally not included in this version.

## How To Run

Run commands from the project root.

```bash
PYTHONPATH=src python3 -m unittest discover
```

Validate the input CSV files:

```bash
PYTHONPATH=src python3 -m broker_ops_report validate-inputs \
  --orders data/sample_order_events.csv \
  --market-events data/sample_market_events.csv
```

Generate the exception log:

```bash
PYTHONPATH=src python3 -m broker_ops_report generate-reports \
  --report exception-log \
  --orders data/sample_order_events.csv \
  --market-events data/sample_market_events.csv \
  --output-dir outputs
```

Generate the shift summary JSON:

```bash
PYTHONPATH=src python3 -m broker_ops_report generate-reports \
  --report shift-summary \
  --orders data/sample_order_events.csv \
  --market-events data/sample_market_events.csv \
  --output-dir outputs
```

Generate by-symbol trading stats:

```bash
PYTHONPATH=src python3 -m broker_ops_report generate-reports \
  --report symbol-stats \
  --orders data/sample_order_events.csv \
  --market-events data/sample_market_events.csv \
  --output-dir outputs
```

Generate the Markdown shift report:

```bash
PYTHONPATH=src python3 -m broker_ops_report generate-reports \
  --report shift-report \
  --orders data/sample_order_events.csv \
  --market-events data/sample_market_events.csv \
  --output-dir outputs
```

## Verification Snapshot

Current expected audit results:

- Tests: `76` passing.
- Order rows: `20`.
- Market-event rows: `5`.
- Exception rows: `14`.
- Severity breakdown: `Critical 4`, `Warning 10`, `Info 0`.
- By-symbol rows: `6`.
- By-symbol total orders: `20`.
- No Excel or HTML output.

## Limitations And Non-Claims

- Static sample data only.
- No real client/account data.
- No live broker connection.
- No MT4/MT5 admin access.
- No FIX venue connection.
- No broker bridge integration.
- No trade execution.
- Not a trading bot.
- Not production risk infrastructure.
- Not investment or trading advice.

## Project Status

The v1 reporting workflow is complete for CSV, JSON, and Markdown outputs.
Remaining portfolio work is packaging, evidence, and publishing setup.
