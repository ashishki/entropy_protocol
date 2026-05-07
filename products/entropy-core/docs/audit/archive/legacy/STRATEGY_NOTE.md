# STRATEGY_NOTE — Phase 7 Boundary Review
_Date: 2026-05-03 · Reviewing: Phase 7 completion before Phase 8/T21_

## Strategic Assessment

Phase 6 and Phase 7 now have scoped boundary reviews. Existing review coverage
before this session already included Phase 1 audit artifacts and Phase 2-5
boundary reviews. The missing implementation-phase reviews were Phase 6
(`products/entropy-core/docs/audit/PHASE6_REVIEW.md`) and Phase 7 (`products/entropy-core/docs/audit/PHASE7_REVIEW.md`).

Phase 7 materially improves the evaluation infrastructure: strict IS/OOS
splitting, detector-level leakage reports, and a runner that blocks OOS
evaluation before the T19 checklist passes. During review, a P1 weakness was
found and fixed: omitted leakage detectors can no longer produce an overall PASS.

## Recommendation

- Proceed past Phase 7 only as far as T21 governance disposition.
- Do not start T21 implementation until D-010 is closed for T21 or a
  T21-specific waiver/disposition is recorded.
- Treat D-012's first profiling gate as reached. Performance work may collect
  Python profiling evidence, but no language/runtime escalation is approved.

## Strategic Risks

| Risk | Status | Disposition |
|------|--------|-------------|
| Formula-bearing T21 starts without governance disposition | Active | Stop-ship before T21 implementation |
| Leakage gate becomes formal rather than detector-backed | Remediated | Missing T19 detectors now FAIL |
| Synthetic tests are misused as real evidence | Active | F-30/F-31 remain future real-evidence gates |
| High-load performance assumptions remain unmeasured | Active | D-012 profiling gate reached; evidence required before escalation or scale claims |

## Next Action

Record an explicit T21 formula-governance disposition before implementing the
P&L Attribution Engine.
