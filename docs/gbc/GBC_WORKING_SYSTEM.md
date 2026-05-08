# Guided Build Cycle Working System

Last updated: 2026-05-08

## Purpose

The Guided Build Cycle is the operating system for building the Broker Operations Exception Report Generator with Codex. It keeps work sequential, inspectable, and safe while still moving quickly.

The cycle is:

`task brief -> read-only inspection -> approved plan -> bounded implementation -> tests -> audit -> checkpoint`

## Gates

### Gate 0 - Scope Safety

Confirm the task stays within the static broker-ops reporting demo. Stop if the task implies live trading, broker API use, MT4/MT5 integration, credentials, account-specific data, or production execution claims.

### Gate 1 - Inspection

Read the relevant files before planning. For code tasks, inspect schemas, entrypoints, tests, outputs, and any existing documentation. Do not guess field names, command names, or output paths.

### Gate 2 - Approved Plan

Write a small implementation plan before editing. The plan must name the goal, in-scope changes, out-of-scope changes, affected surfaces, verification plan, risks, and approval status.

### Gate 3 - Implementation

Implement only the approved slice. Keep changes local to the task. Do not perform unrelated cleanup, dependency churn, architecture changes, or output-contract changes without a new plan.

### Gate 4 - Verification

Run the narrowest meaningful tests and artifact checks. For report generation, verify files exist, row counts tie out, summary counts match source events, and report sections are present.

### Gate 5 - Audit

Review the diff and compare it against the approved plan. Check domain accuracy, schema contracts, exception-rule behavior, output consistency, safety language, and git hygiene.

### Gate 6 - Checkpoint

Record what changed, what passed, what failed, what risks remain, and the next recommended task. The checkpoint should make the next Codex session productive without rereading the entire history.

## Halt Conditions

Stop before editing if:

- required input files or schemas are missing;
- required columns are ambiguous;
- exception semantics are not clear enough to test;
- a requested change requires live broker, exchange, or account access;
- credentials or private account artifacts appear in scope;
- generated totals do not tie out;
- unrelated user changes appear in the same files and need a coordination decision.

## Artifact Rules

Use the lean templates in `docs/gbc/templates/`.

- One task brief per meaningful task.
- One approved plan before edits.
- One implementation report after edits.
- One test report after verification.
- One checkpoint note at the end of the cycle.

For small documentation-only tasks, these can be short. The point is traceability, not bureaucracy.
