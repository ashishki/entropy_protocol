# Agentic Capability Evaluation

## SAS-MI-015 — Internal Analyst Memo Export

- Date: 2026-05-09
- Eval Source: `.venv/bin/python -m pytest tests/unit/test_analyst_memo_export.py -q`, run 2026-05-09
- Task tag: `agent:loop`
- Primary metric: memo guard test pass rate = `1.000000` (`3/3`)
- Baseline comparison: first recorded agentic memo-export baseline; no prior
  agentic memo baseline exists, so no regression is computed.
- Result: PASS

### Checks Covered

- Required memo sections are present: scope, corpus coverage, retrieved
  evidence, deterministic metrics, interpretation, limitations, and review
  queue.
- Interpretive claims reject unknown citations and require at least one cited
  source document ID or deterministic metric ID.
- Memo rendering marks the artifact as internal-only and not customer-facing;
  model validation rejects `internal_only=false`.

### Regression Notes

- Regression: none.
- Root cause classification: n/a.
