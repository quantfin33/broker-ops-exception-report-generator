# GBC Checkup Matrix

Last updated: 2026-05-08

## Purpose

This matrix defines the recurring checks for the Broker Operations Exception Report Generator. Use it during planning, verification, audit, and pre-commit review.

## Checkups

| Checkup | When | Evidence |
| --- | --- | --- |
| Scope safety | Every task | Task stays static/demo-only and has no live trading, broker API, credential, or account dependency. |
| Schema audit | Data and validation tasks | Required columns, null rules, timestamp assumptions, and numeric fields are documented and tested. |
| Domain audit | Exception-rule and report tasks | Status lifecycle, bridge status, latency, rejection, pending, and handover behavior match broker-ops framing. |
| Rule audit | Exception-rule tasks | Each exception rule has at least one positive fixture and one non-trigger case where practical. |
| Output audit | Report-generation tasks | JSON, CSV, Markdown, and optional Excel outputs exist and counts tie out. |
| Safety audit | README/docs/report tasks | Non-claims are visible: no MT4/MT5 connection, no live monitor, no trading bot, no broker-admin proof. |
| Source/provenance audit | Reuse tasks | No code or data is copied from live trading, credential, browser, app-support, cache, or session files. |
| Git audit | Before commit | `git status --short` and diff are reviewed; unrelated user changes are not included. |

## Minimum Verification By Phase

| Phase | Required Checks |
| --- | --- |
| Documentation/GBC | Markdown sections exist, PDF regenerates, PDF text contains GBC and audit language. |
| Scaffold | Package imports, CLI help works, tests discover. |
| Static data | CSV headers match the plan, intentionally imperfect rows are present, no real account data exists. |
| Validation | Missing columns, missing core fields, duplicate IDs, timestamp parsing, and numeric parsing are tested. |
| Exception rules | Each rule has deterministic fixtures and expected severity/action output. |
| Reports | Output files generate, row counts tie out, handover section lists unresolved items. |
| README | Usage works from a clean checkout, limitations are explicit, no production claims are implied. |

## Pre-Commit Checklist

- [ ] Run relevant tests or explain why they were not run.
- [ ] Regenerate changed outputs.
- [ ] Inspect generated report content.
- [ ] Scan for secrets and live integration references.
- [ ] Review `git status --short`.
- [ ] Review diff for unrelated changes.
- [ ] Update the project plan checklist.
- [ ] Add an audit ledger entry.
