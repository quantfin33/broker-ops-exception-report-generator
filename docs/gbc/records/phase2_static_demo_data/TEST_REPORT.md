# GBC Test Report - Phase 2 Static Demo Data

## Commands Run

```bash
PYTHONPATH=src python3 -m unittest discover
PYTHONPATH=src python3 -m broker_ops_report --help
head -5 data/sample_order_events.csv
head -5 data/sample_market_events.csv
/Users/chris/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 scripts/build_project_plan_pdf.py
```

## Results

- Passed: `PYTHONPATH=src python3 -m unittest discover` ran 11 tests and passed.
- Passed: `PYTHONPATH=src python3 -m broker_ops_report --help` returned exit code 0.
- Passed: `head -5 data/sample_order_events.csv` showed the required order-event header and synthetic fixture rows.
- Passed: `head -5 data/sample_market_events.csv` showed the required market-event header and synthetic fixture rows.
- Passed: project-plan PDF regenerated after the Phase 2 checklist update.

## Artifact Checks

- Files generated: static CSV fixtures, schema doc, GBC records, regenerated project-plan PDF.
- Counts tied out: not applicable because Phase 2 does not implement report generation.
- Report sections verified: not applicable to broker reports.

## Gaps Or Risks

- CSV validation behavior is intentionally deferred to Phase 3.
- Exception-rule tests are intentionally deferred to a later phase.
