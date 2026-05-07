# Audit Index — Signal Analytics Sandbox

_Append-only. One row per review cycle._

---

## Review Schedule

| Cycle | Phase | Date | Scope | Stop-Ship | P0 | P1 | P2 |
|-------|-------|------|-------|-----------|----|----|-----|

---

## Archive

| Cycle | File | Phase | Health |
|-------|------|-------|--------|

---

## Notes

- Index initialized at project bootstrap (2026-05-07).
- Phase 0 (SAS-001/SAS-002) is non-codex and does not produce a review cycle entry. Phase 1 close produces Cycle 1.
- Heavy tasks (T12, T14, T20) produce per-task evidence files at `docs/audit/HEAVY_T{NN}_EVIDENCE.md`. Those are referenced from the cycle review that closes the heavy task; they are not separate cycle entries.
- Optional simplification passes use a separate row prefix (`SIMP-N`) and live in `docs/audit/SIMPLIFICATION_REPORT.md`. They do not interleave with deep review cycles in this index.
