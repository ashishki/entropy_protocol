# Evidence Index — Entropy Protocol

_Proof lookup across reviews, evals, and heavy tasks. Retrieval convenience only — points to canonical artifacts._
_Required because this project has heavy tasks (T16, T17, T18, T19, T20, T21, T22) and cross-phase evidence expectations._

---

## Heavy Task Evidence

| Task | Evidence Type | Artifact | Status | Date |
|------|--------------|---------|--------|------|
| T16 (SimBroker Fill Engine) | Determinism + no-lookahead + bar-range constraint | tests/unit/test_simbroker.py::test_fill_engine_determinism | Not started | — |
| T17 (Calibration Interface) | Abstract interface enforcement + no-op mock | tests/unit/test_simbroker.py::test_bid_ask_provider_abstract | Not started | — |
| T18 (IS/OOS Splitter) | Leakage boundary test | tests/integration/test_walk_forward.py::test_no_future_leakage | Not started | — |
| T19 (Leakage Detection) | Leakage checklist PASS evidence | tests/integration/test_leakage.py::test_full_leakage_checklist | Not started | — |
| T20 (Walk-Forward Runner) | RunRecord hashes + leakage gate | tests/integration/test_walk_forward.py::test_runner_produces_run_record_with_all_hashes | Not started | — |
| T21 (P&L Attribution) | Worked example verification | tests/unit/test_attribution.py::test_four_stream_worked_example | Not started | — |
| T22 (P1/P3 State Machine) | Synthetic circuit-breaker test suite | tests/unit/test_governance.py::test_p1_circuit_breaker_suite | Not started | — |

## Phase Gate Evidence

| Phase | Gate | Artifact | Status | Date |
|-------|------|---------|--------|------|
| Phase 0 (v1) | All T01-T24 pass; no OOS claims before T19 passes | docs/audit/CYCLE{N}_REVIEW.md | Not started | — |

## Statistical Formula Stubs (blockers from PROJECT_BRIEF.md)

| Formula | Status | Blocking task | Resolution path |
|---------|--------|--------------|-----------------|
| Harvey-Liu deflation | Incomplete — needs worked example | T23 | Implement stub; document formula assumption; resolve in Phase 0+ |
| Sharpe CI derivation | Incomplete — needs validation examples | T23 | Implement analytical method with configurable bootstrap fallback |
| K3/N_eff estimator | Must be locked across docs and implementation | T23 | Implement with documented formula; test against known N_eff |
| Purge/embargo formula | Incomplete | T18 | Document assumption used; implement; note in ADR when resolved |
| P4 weekly regime algorithm | Not independently reproducible | Out of scope v1 | Defer to Phase 1+ |
