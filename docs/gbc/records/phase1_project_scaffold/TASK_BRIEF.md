# GBC Task Brief - Phase 1 Project Scaffold

## Goal

Create the minimal Python package scaffold and CLI shell for the Broker Operations Exception Report Generator.

## Background

The project already has a GBC operating system, project plan, PDF generator, and safety instructions. Phase 1 must only create the Python scaffold and CLI placeholders. Broker exception rules, sample order-event data, and report generation are out of scope.

## In Scope

- Create `pyproject.toml`.
- Create `src/broker_ops_report/` with importable package, `__main__.py`, CLI shell, and config constants.
- Create `tests/test_cli.py` for package import, help output, command help, placeholder command exit behavior, and no live dependency assumptions.
- Add `data/.gitkeep` and `outputs/.gitkeep`.
- Update the Phase 1 checklist only after verification passes.
- Add GBC implementation, test, checkpoint, and audit records.

## Out Of Scope

- Broker exception detection rules.
- Realistic sample order-event or market-event data.
- Final broker report outputs.
- Live APIs, MT4/MT5, FIX, broker bridge, Binance, Telegram, TradingView, or account dependencies.
- README/portfolio phase work.

## Acceptance Criteria

- [x] Package imports successfully.
- [x] CLI root help works.
- [x] `validate-inputs`, `generate-reports`, and `run-demo` help works.
- [x] Placeholder commands exit predictably without reading data or writing reports.
- [x] `python -m unittest discover` equivalent passes in this local environment.
- [x] Project plan marks only Phase 1 scaffold items done.

## Safety Check

- [x] Static/demo-only.
- [x] No live trading, broker API, MT4/MT5, exchange, Telegram, or account dependency.
- [x] No credentials, browser sessions, app-support files, or private account data.
