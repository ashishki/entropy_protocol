# HEAVY_T20_EVIDENCE

Date: 2026-05-07
Task: T20 LLMExtractionAdapter

## Gate Behavior

- `LLMExtractionAdapter(...)` raises `LLMNotApproved` unless both gates are
  present: `SIGNAL_SANDBOX_ENABLE_LLM=1` and `llm_approved=True`.
- Unit coverage: `tests/unit/test_llm_extraction.py::test_activation_requires_both_gates`.
- CI uses fixed mock clients only; no live Ollama or Claude calls are made by
  the test suite.

## Cost-Cap Behavior

- Paid provider calls are treated as `provider == "claude"`.
- `SIGNAL_SANDBOX_COST_CAP_USD=0` disables paid LLM calls before model
  invocation.
- Once cumulative `cost_usd` reaches or exceeds the configured cap, the next
  `extract()` raises `CostCapExceeded` before invoking the client.
- Unit coverage:
  `tests/unit/test_llm_extraction.py::test_cost_cap_enforced` and
  `tests/unit/test_llm_extraction.py::test_zero_cap_disables_paid_provider`.

## Draft-Only Ledger Boundary

- Every successful LLM extraction returns `status="draft_pending_review"`.
- LLM adapter IDs are constrained to `llm/(ollama|claude)/[A-Za-z0-9._-]+`.
- `write_ledger(...)` rejects records whose
  `extraction_metadata.adapter_id.startswith("llm/")` unless `reviewer_id` is
  non-None.
- Unit coverage: `tests/unit/test_llm_extraction.py::test_no_direct_write_to_ledger`.

## Acceptance-Rate Baseline

- Fixed eval set: 3 synthetic public Telegram pilot examples covering
  `bablos79`, `nemphiscrypts`, and `pifagortrade`.
- Fixture model: `ollama/eval-fixture-v1`, deterministic mock response.
- Baseline acceptance rate:
  `3 / 3 = 1.000000` drafts approved without modification.
- Eval coverage:
  `tests/eval/test_llm_extraction_quality.py::test_acceptance_rate_baseline`.

## Verification

- `.venv/bin/python -m pytest tests/ -q` -> 84 passed.
- `.venv/bin/ruff check src/ tests/` -> pass.
- `.venv/bin/ruff format --check src/ tests/` -> pass.
- `.venv/bin/pyright` -> pass.
