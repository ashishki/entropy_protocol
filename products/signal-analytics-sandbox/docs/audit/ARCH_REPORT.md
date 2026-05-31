# ARCH_REPORT — Cycle 32
_Date: 2026-05-31_

## Component Verdicts

| Component | Verdict | Note |
|-----------|---------|------|
| Auto-validation decision stack | PASS | Decision engine and policy gate preserve conservative acceptance. |
| Active-state documents | PASS | State records Phase 42 complete and keeps external delivery blocked. |
| Tests | PASS | Unit tests cover all Phase 42 acceptance criteria and compact-state updates. |

## Contract Compliance

| Rule | Verdict | Note |
|------|---------|------|
| PSR-1 public-source-only | PASS | Evidence bundles allow public/operator-public source class and reject private-source URL patterns. |
| PSR-2 reproducibility | PASS | Decisions, policy output, and eval artifacts cite deterministic refs. |
| PSR-3 LLM output is never truth | PASS | Decision engine requires validators/policy; model confidence cannot bypass. |
| PSR-4 cost cap | PASS | No paid adapter or model calls added. |
| PSR-5 snapshot immutability | PASS | No market snapshot writes added. |
| PSR-6 disclaimer integrity | PASS | Report renderer and canonical disclaimer untouched. |
| PSR-7 outcome rule citation | PASS | No outcome engine changes; accepted outcomes report 0 recomputed rows. |
| PSR-8 evidence preservation | PASS | Evidence refs are required for extracted fields and validator results. |
| PSR-9 append-only registries | PASS | Registries untouched. |
| PSR-10 Phase 0 gate | PASS | Gate acknowledgment remains in `docs/CODEX_PROMPT.md`. |
| PSR-11 no forward-looking claims | PASS | New client-ready artifacts avoid advice, unsupported ranking, and future-profit wording. |

## ADR Compliance

| ADR | Verdict | Note |
|-----|---------|------|
| ADR-001 snapshot serialization | PASS | No snapshot behavior changed. |
| ADR-002 Author Market Intelligence | PASS | Deterministic truth boundaries preserved; RAG/agentic capabilities not expanded. |
| ADR-003 channel-specific tools | PASS | Review/export posture preserved. |
| ADR-004 media evidence pipeline | PASS | Media/OCR/transcript refs remain evidence refs; no provider expansion added. |
| ADR-005 auto-validation evidence engine | PASS | Phase 42 implements decision/policy/evaluation on the proof surface. |

## Architecture Findings

No architecture findings.

## Right-Sizing / Runtime Checks

| Check | Verdict | Note |
|-------|---------|------|
| Solution shape still Hybrid | PASS | No new architecture shape introduced. |
| Deterministic-owned areas remain deterministic | PASS | Outcomes remain non-recomputed because prerequisites are absent. |
| Runtime tier still T0 | PASS | No daemons, shell mutation, services, or privileged behavior added. |
| LLM adapter still gated | PASS | No adapter activation or LLM call added. |
| Public-source-only boundary intact (PSR-1) | PASS | Only public source refs in static artifacts. |

## Reproducibility / Integrity Checks

| Check | Verdict | Note |
|-------|---------|------|
| No new non-determinism sources | PASS | Decision/policy functions are deterministic and artifact-only. |
| Decimal discipline preserved | PASS | Confidence and setup numeric fields use `Decimal`. |
| Snapshots immutable on disk | PASS | Snapshot code untouched. |
| Disclaimer canonical | PASS | Disclaimer code untouched. |
| Outcome rule registry append-only | PASS | Registry untouched. |
| Extraction rule templates append-only | PASS | Templates untouched. |
| Active capability profiles respected | PASS | RAG/Agentic remain declared but not expanded by Phase 38 artifacts. |

## Doc Patches Needed

None.
