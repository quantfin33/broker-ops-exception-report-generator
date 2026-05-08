# Broker Operations Exception Report Generator - Codex Instructions

## Project Purpose

Build a static, recruiter-safe Python demo that reads broker-style order/platform event logs and produces broker operations exception reports, by-symbol statistics, and shift handover notes.

This is a broker-control-room reporting demo. It is not a trading strategy, trading bot, live broker integration, MT4/MT5 Manager API wrapper, FIX venue connection, or proof of broker administrator access.

## Operating Rule

Use the Guided Build Cycle for every meaningful change:

`task brief -> read-only inspection -> approved plan -> bounded implementation -> tests -> audit -> checkpoint`

Do not skip inspection. Do not expand the scope while implementing. If a task requires live credentials, real accounts, external broker APIs, or account-specific data, stop and ask for a safer static alternative.

## Scope Boundaries

Allowed:

- static CSV inputs;
- deterministic Python transformations;
- broker-style exception rules;
- generated JSON, CSV, Markdown, and optional Excel outputs;
- tests, sample fixtures, README, and local documentation.

Not allowed:

- live order monitoring;
- real broker, exchange, Binance, Telegram, TradingView, MT4/MT5, FIX, or bridge connections;
- credential, session, browser, app-support, `.env`, or account-file reuse;
- claims of production broker access or real execution control.

## Expected Outputs

The finished v1 should generate:

- `outputs/broker_ops_shift_summary.json`
- `outputs/by_symbol_trading_stats.csv`
- `outputs/order_exception_log.csv`
- `outputs/broker_ops_shift_report.md`
- optional `outputs/broker_ops_shift_report.xlsx`

## Build And Test Commands

Use these local Phase 1 commands from the repo root:

```bash
PYTHONPATH=src python3 -m broker_ops_report --help
PYTHONPATH=src python3 -m broker_ops_report validate-inputs --help
PYTHONPATH=src python3 -m broker_ops_report generate-reports --help
PYTHONPATH=src python3 -m broker_ops_report run-demo --help
PYTHONPATH=src python3 -m unittest discover
```

Installed-package equivalent in environments where `python` is available:

```bash
python -m broker_ops_report --help
python -m broker_ops_report validate-inputs
python -m broker_ops_report generate-reports
python -m unittest discover
```

Current documentation command:

```bash
/Users/chris/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_project_plan_pdf.py
```

If running outside Codex, install `reportlab` into the local Python environment or use an equivalent Python runtime that already has it.

## Verification Expectations

Before calling a task complete:

- inspect `git status --short`;
- review the relevant diff;
- run the narrowest meaningful tests or artifact checks;
- confirm generated output paths exist when the task touches outputs;
- confirm safety language still says this is static/demo-only;
- record any skipped test and why.

## Protected Claims

Keep these claims true:

- The project reads static sample data.
- The project simulates a reporting/review layer around broker operations.
- The project does not connect to MT4/MT5, broker APIs, FIX venues, exchanges, bridges, or live accounts.
- The project is a portfolio demo, not production risk infrastructure.
