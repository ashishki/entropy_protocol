# Audit Index - Entropy Core

Append-only. One row per reset-era review cycle.

## Review Schedule

| Cycle | Phase | Date | Scope | Stop-Ship | P0 | P1 | P2 |
|-------|-------|------|-------|-----------|----|----|----|
| PHASE1-RESET | 1 | 2026-05-07 | T01-T03 Reset Foundation | 0 | 0 | 0 | 0 |
| PHASE2-GOVERNANCE | 2 | 2026-05-07 | T04-T07 Governance Integrity | 0 | 0 | 0 | 0 |
| PHASE3-EVALUATION | 3 | 2026-05-07 | T08-T11 Evaluation Safety | 0 | 0 | 0 | 0 |
| RESET-CLOSURE | 4 | 2026-05-07 | T01-T14 Reset Closure | 0 | 0 | 0 | 0 |
| FIRST-RESEARCH-PACKET | 5 | 2026-05-07 | T15-T19 First Research Evidence Packet | 0 | 0 | 0 | 0 |
| ARCHIVE-EVIDENCE-EXPANSION | 6 | 2026-05-07 | T20-T24 Archive Evidence Expansion | 0 | 0 | 0 | 0 |
| ARCHIVE-REPRODUCIBILITY-HARDENING | 7 | 2026-05-08 | T25-T29 Archive Reproducibility Hardening | 0 | 0 | 0 | 0 |
| PHASE-GATE-READINESS-REVIEW | 8 | 2026-05-09 | T30-T34 Phase-Gate Readiness Review | 0 | 0 | 0 | 0 |
| HOLDOUT-ACCESS-PROTOCOL | 9 | 2026-05-09 | T35-T39 Holdout Access Protocol | 0 | 0 | 0 | 0 |

## Archive

| Cycle | File | Phase | Health |
|-------|------|-------|--------|
| PHASE1-RESET | `docs/audit/PHASE1_REVIEW.md` | 1 | PASS |
| PHASE2-GOVERNANCE | `docs/audit/PHASE2_REVIEW.md` | 2 | PASS |
| PHASE3-EVALUATION | `docs/audit/PHASE3_REVIEW.md` | 3 | PASS |
| RESET-CLOSURE | `docs/audit/RESET_REVIEW.md` | 4 | PASS |
| FIRST-RESEARCH-PACKET | `docs/audit/FIRST_RESEARCH_PACKET_REVIEW.md` | 5 | PASS |
| ARCHIVE-EVIDENCE-EXPANSION | `docs/audit/ARCHIVE_EVIDENCE_EXPANSION_REVIEW.md` | 6 | PASS |
| ARCHIVE-REPRODUCIBILITY-HARDENING | `docs/audit/ARCHIVE_REPRODUCIBILITY_REVIEW.md` | 7 | PASS |
| PHASE-GATE-READINESS-REVIEW | `docs/audit/PHASE_GATE_READINESS_REVIEW.md` | 8 | PASS |
| HOLDOUT-ACCESS-PROTOCOL | `docs/audit/HOLDOUT_ACCESS_PROTOCOL_REVIEW.md` | 9 | PASS |

## Notes

- Pre-reset audit files live under `docs/legacy/old-workflow/2026-05-07/` or existing archive directories.
- Run Phase 1 validation before T01 and write `docs/audit/PHASE1_AUDIT.md`.
