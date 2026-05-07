# Audit Index — Signal Analytics Sandbox

_Append-only. One row per review cycle._

---

## Review Schedule

| Cycle | Phase | Date | Scope | Stop-Ship | P0 | P1 | P2 |
|-------|-------|------|-------|-----------|----|----|-----|
| 1 | Phase 1 | 2026-05-07 | T01-T03 | No | 0 | 0 | 0 |
| 2 | Phase 2 | 2026-05-07 | T04-T06 | No | 0 | 0 | 0 |
| 3 | Phase 3 | 2026-05-07 | T07-T08 | No | 0 | 0 | 0 |
| 4 | Phase 4 | 2026-05-07 | T09-T11 | No | 0 | 0 | 0 |
| 5 | Phase 5 | 2026-05-07 | T12-T14 | No | 0 | 0 | 0 |
| 6 | Phase 6 | 2026-05-07 | T15-T17 | No | 0 | 0 | 0 |
| 7 | Phase 7 | 2026-05-07 | T18-T19 | No | 0 | 0 | 0 |
| 8 | Phase 8 | 2026-05-07 | T20 | No | 0 | 0 | 0 |
| 9 | Phase 9 | 2026-05-07 | SAS-PILOT-001-SAS-PILOT-007 | No | 0 | 0 | 0 |

---

## Archive

| Cycle | File | Phase | Health |
|-------|------|-------|--------|
| 1 | `docs/archive/PHASE1_REVIEW.md` | Phase 1 | OK |
| 2 | `docs/archive/PHASE2_REVIEW.md` | Phase 2 | OK |
| 3 | `docs/archive/PHASE3_REVIEW.md` | Phase 3 | OK |
| 4 | `docs/archive/PHASE4_REVIEW.md` | Phase 4 | OK |
| 5 | `docs/archive/PHASE5_REVIEW.md` | Phase 5 | OK |
| 6 | `docs/archive/PHASE6_REVIEW.md` | Phase 6 | OK |
| 7 | `docs/archive/PHASE7_REVIEW.md` | Phase 7 | OK |
| 8 | `docs/archive/PHASE8_REVIEW.md` | Phase 8 | OK |
| 9 | `docs/archive/PHASE9_REVIEW.md` | Phase 9 | OK |

---

## Notes

- Index initialized at project bootstrap (2026-05-07).
- Phase 0 (SAS-001/SAS-002) is non-codex and does not produce a review cycle entry. Phase 1 close produces Cycle 1.
- Heavy tasks (T12, T14, T20) produce per-task evidence files at `docs/audit/HEAVY_T{NN}_EVIDENCE.md`. Those are referenced from the cycle review that closes the heavy task; they are not separate cycle entries.
- Optional simplification passes use a separate row prefix (`SIMP-N`) and live in `docs/audit/SIMPLIFICATION_REPORT.md`. They do not interleave with deep review cycles in this index.
