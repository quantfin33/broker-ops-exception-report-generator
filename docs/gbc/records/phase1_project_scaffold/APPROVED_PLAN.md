# GBC Approved Plan - Phase 1 Project Scaffold

## Goal

Create a minimal importable Python package and argparse CLI shell for Phase 1 only.

## In Scope

- Add standard-library-only package scaffold under `src/broker_ops_report/`.
- Add placeholder CLI subcommands: `validate-inputs`, `generate-reports`, and `run-demo`.
- Add tests that exercise import, help, command help, placeholder command behavior, and no live dependency requirements.
- Add `data/.gitkeep` and `outputs/.gitkeep`.
- Update `AGENTS.md` with local Phase 1 commands because this Mac has `python3` but no bare `python`.
- Update the project plan Phase 1 checklist and regenerate the project-plan PDF.
- Append GBC audit/checkpoint artifacts after verification.

## Out Of Scope

- Data schemas beyond placeholder path constants.
- CSV reading, validation logic, exception rules, report generation, Excel output, dashboard work, README work, CI, or live integrations.

## Affected Surfaces

- Packaging: `pyproject.toml`.
- Python source: `src/broker_ops_report/`.
- Tests: `tests/test_cli.py`.
- Project tracking: `docs/BROKER_OPS_PROJECT_PLAN.md`, GBC records, and project-plan PDF.
- Folders: `data/` and `outputs/`.

## Verification Plan

- Run `PYTHONPATH=src python3 -m unittest discover`.
- Run `PYTHONPATH=src python3 -m broker_ops_report --help`.
- Run command help for `validate-inputs`, `generate-reports`, and `run-demo`.
- Run each placeholder command and confirm exit code 0 with a clear Phase 1 not-implemented message.
- Inspect `git status --short --untracked-files=all`.
- Confirm no live integration strings, credentials, or account dependencies were added.

## Risks

- The user-requested bare `python` command is unavailable on this Mac. Use `python3` with `PYTHONPATH=src` locally; the package still supports `python -m broker_ops_report` where `python` is available or after installation.

## Human Approval

- Approved by: User request in this thread.
- Date: 2026-05-08.
