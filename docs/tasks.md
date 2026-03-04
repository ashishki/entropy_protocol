# Entropy Protocol — Task Registry

**Classification:** Confidential — Internal Development Document
**Filename:** `docs/tasks.md`
**Version:** 1.1
**Date:** 2026-03-04
**Owner:** Spec Owner / Staff-Level Systems Architect

---

## Purpose

This document is the authoritative task registry for the Entropy Protocol. It tracks all open development tasks, audit finding remediations, and architectural decisions requiring action. All P0/P1 audit findings must have a corresponding entry in the Audit Findings Backlog section.

---

## Task Status Definitions

| Status | Meaning |
|---|---|
| **Open** | Task identified; not started. |
| **In Progress** | Work underway. |
| **Blocked** | Waiting on a dependency (specify). |
| **Mitigated** | Remediation implemented; pending audit verification. |
| **Closed** | Verified closed by a pipeline step; citation required. |

---

## Audit Findings Backlog

Entries below are sourced from:
- `docs/AUDIT_v1.md` (baseline findings F-1..F-21)
- `docs/audit/REVIEW_REPORT.md` Cycle 1 (new findings F-22..F-32)

No findings are marked as resolved; all are treated as **Open** unless otherwise noted.

Finding IDs match the source audit exactly (F-1 through F-21). Task IDs are prefixed `TASK-AF-` (Audit Finding).

### Entry Format

```
| TASK-AF-<N> | F-<N> | P<severity> | <Status> | <Source file> | <Acceptance criterion> | <ADR/PR ref> |
```

---

### P0 Findings (CRITICAL — Block Phase Gating)

| Task ID | Finding ID | Severity | Status | Source Audit | Summary | Acceptance Criterion | ADR/PR |
|---|---|---|---|---|---|---|---|
| TASK-AF-001 | F-1 | P0 | Open | `docs/AUDIT_v1.md` | Harvey-Liu formula variant not specified. Mandated deflated Sharpe cannot be correctly computed, verified, or audited. | PROTOCOL_SPEC.md NN-5 and GLOSSARY.md contain: (a) the specific variant (Bonferroni / Holm-Bonferroni / BHY / DSR), (b) the complete formula with all required parameters, (c) aggregation rule for cross-phase trials, (d) whether AT trials count toward the same budget. A second reviewer can independently reproduce the computed haircut from the same inputs. | — |
| TASK-AF-002 | F-2 | P0 | Open | `docs/AUDIT_v1.md` | Sharpe CI claim is wrong by factor 4–6×. Stated CI ±0.15–0.20 at 15 months OOS requires ~34 years of data; actual CI ≈ ±0.91. K1 is effectively a coin flip as specified. | CHARTER.md and PROTOCOL_SPEC.md CI statement is corrected to ±0.89 (or an alternative framework is documented with derivation). All downstream decision thresholds that depended on the wrong CI are recascaded. A derivation is shown in the spec. | — |
| TASK-AF-003 | F-3 | P0 | Open | `docs/AUDIT_v1.md` | P3 correlation trigger population undefined. Trigger frequency varies by an order of magnitude depending on which of five plausible populations is chosen. | CHARTER.md and PROTOCOL_SPEC.md Section D state: (a) asset-price or skill P&L correlation, (b) universe (all 20 vs. active positions only), (c) return interval (daily / 4H), (d) treatment of short positions after Phase 3. Definition locked before Phase 0 P3 implementation. | — |
| TASK-AF-004 | F-4 | P0 | Open | `docs/AUDIT_v1.md` | P4 signal algorithm undefined. Phase 0 exit criterion, Phase 1 OOS spanning, and Phase 2 IC correlation requirement all depend on a P4 algorithm that is nowhere specified. | PROTOCOL_SPEC.md Section E contains a complete P4 specification: inputs, features, thresholds or model class, calibration method, and the assignment rule for "trending / mean-reverting / stress." A second developer can independently reproduce the historical label series from the same raw data. | — |
| TASK-AF-005 | F-5 | P0 | Open | `docs/AUDIT_v1.md` | IC_long assumption is load-bearing and unvalidated; no suspect threshold exists unlike IC_short. At ρ_avg=0.40, effective FLAM gross ≈ 0.25, below K1. | CHARTER.md and PROTOCOL_SPEC.md define: (a) a suspect threshold for IC_long analogous to IC_short's >0.04 rule, (b) a haircut rule if walk-forward IC_long exceeds the threshold, (c) a literature citation or prior justification for the 0.03–0.05 range, (d) FLAM BR_eff calculation that accounts for skill correlation (using N_eff correction). | — |

---

### P1 Findings (HIGH — Required Before Next Phase)

| Task ID | Finding ID | Severity | Status | Source Audit | Summary | Acceptance Criterion | ADR/PR |
|---|---|---|---|---|---|---|---|
| TASK-AF-006 | F-6 | P1 | Open | `docs/AUDIT_v1.md` | K4 missed-kill probability unspecified. Dead short book (IC=0) survives K4 with 31% probability. K4 is miscalibrated in both directions simultaneously. | CHARTER.md documents both false-kill rate (acknowledged: ~60%) and missed-kill rate (~31%). A decision is recorded on whether the threshold is accepted as-is or adjusted, with rationale. | — |
| TASK-AF-007 | F-7 | P1 | Open | `docs/AUDIT_v1.md` | Regime label vintage contamination. P4 calibrated in Phase 0 on ≥3 years historical data; if parameter-fitted, Phase 1 IS windows overlap with calibration window → OOS spanning count invalid. | PROTOCOL_SPEC.md specifies: (a) whether P4 involves parameter fitting on historical data, (b) if yes, which windows are flagged as in-sample for spanning purposes, (c) mechanism for excluding in-sample labeled windows from OOS spanning counts. | — |
| TASK-AF-008 | F-8 | P1 | Open | `docs/AUDIT_v1.md` | FLAM Phase 3 justification rests on independence assumption contradicted by spec (shorts derived from mirrored long skills). At ρ_IC=0.8, net delta approaches zero or negative. | PROTOCOL_SPEC.md Section E documents: (a) assumed ρ_IC between long and short signals, (b) BR_eff formula adjusted for correlation, (c) revised expected net Sharpe delta range under the adjusted formula. Or Phase 3 is explicitly re-classified as exploratory with no positive-EV justification claim. | — |
| TASK-AF-009 | F-9 | P1 | Open | `docs/AUDIT_v1.md` | No SimBroker drift kill criterion in Phase 1. Phase 1 has a flag (>15% deviation) but no kill action. A false-positive Phase 1 exit certification is possible if costs are systematically understated. | A Phase 1 kill criterion (K6-Phase1 or equivalent) is defined: if SimBroker cost deviation exceeds X% for Y consecutive months during Phase 1, Phase 1 exit is blocked until recalibrated. CHARTER.md and PROTOCOL_SPEC.md updated accordingly. | — |
| TASK-AF-010 | F-10 | P1 | Open | `docs/AUDIT_v1.md` | P1+P3 concurrent activation and sequential recovery undefined. Four unresolved nested states (A–D) identified. Acknowledged as known gap in ARCHITECT_BRIEF.md but unresolved in all five documents. | CHARTER.md Section D defines gross exposure target and ramp behavior for all four states (A–D) from AUDIT_v1.md F-10. Definition sufficient for deterministic harness implementation without developer judgment. | — |
| TASK-AF-011 | F-11 | P1 | Open | `docs/AUDIT_v1.md` | N_eff equicorrelation formula inaccurate for heterogeneous portfolios. Eigenvalue-based formula gives N_eff=3.0 where equicorrelation gives 2.07 — difference straddles K3 threshold. | GLOSSARY.md and PROTOCOL_SPEC.md specify which formula is used for K3 purposes. If equicorrelation retained: cite evidence of adequacy at the K3 boundary. If eigenvalue-based adopted: update all N_eff example computations in docs. | — |

---

### P2 Findings (MEDIUM/LOW — Time-Bounded, No Phase Gate Block)

| Task ID | Finding ID | Severity | Status | Source Audit | Summary | Acceptance Criterion | ADR/PR |
|---|---|---|---|---|---|---|---|
| TASK-AF-012 | F-12 | P2 | Open | `docs/AUDIT_v1.md` | Purge/embargo duration not specified. "Proportional to maximum holding period" is not a formula or value. | GLOSSARY.md defines purge/embargo length as a formula or value for 4H and 1D signals separately. Phase 0 leakage audit checklist requires this as a pass criterion. | — |
| TASK-AF-013 | F-13 | P2 | Open | `docs/AUDIT_v1.md` | P3 reduction range (35–50%) has no selection protocol. Indeterminate gross exposure after P3 fires; evaluation-vs-execution mismatch possible. | CHARTER.md and PROTOCOL_SPEC.md Section D specify a deterministic rule for selecting the reduction magnitude within 35–50% (e.g., a formula tied to current ρ, or a fixed value). | — |
| TASK-AF-014 | F-14 | P2 | Open | `docs/AUDIT_v1.md` | Temporal shuffling detects only one class of leakage (future price features). Classes (a)–(d) remain undetected: normalization leakage, regime label look-ahead, universe selection bias, within-window optimization. | Phase 0 leakage audit checklist is extended with explicit verification steps for each of the four additional leakage classes. Checklist is published in PROTOCOL_SPEC.md or a referenced annex. | — |
| TASK-AF-015 | F-15 | P2 | Open | `docs/AUDIT_v1.md` | K4 t-statistic formula not specified. Three candidate formulas give materially different values. Formula (a) implied by "expected t ≈ 0.24" but never stated. | PROTOCOL_SPEC.md Phase 3 and CHARTER.md Kill Criteria Appendix state the K4 t-statistic formula explicitly: numerator, denominator, degrees of freedom, and autocorrelation handling. | — |
| TASK-AF-016 | F-16 | P2 | Open | `docs/AUDIT_v1.md` | Phase 2 matched pair criteria undefined. "Same entry signal, different overlay state" leaves matching on instance vs. type, time proximity, continuous overlay state, and regime confounding all unspecified. | PROTOCOL_SPEC.md Phase 2 defines: (a) matching rule (instance or type), (b) time-proximity bound, (c) binary classification rule for overlay state, (d) treatment of regime-confounded pairs. Pre-registered before Phase 2 paper trading begins. | — |
| TASK-AF-017 | F-17 | P2 | Open | `docs/AUDIT_v1.md` | Timestamp convention leakage not in Phase 0 exit criteria. Recognized in ARCHITECT_BRIEF.md as advisory ("should be a checklist item") but not codified as a required verification step. | Phase 0 exit criteria in CHARTER.md and PROTOCOL_SPEC.md include explicit timestamp convention verification: data source UTC offset, bar-open vs. bar-close alignment, and evaluation-vs-paper consistency check. | — |
| TASK-AF-018 | F-18 | P2 | Open | `docs/AUDIT_v1.md` | GE-2/GE-3 boundary not bright-line for zero-weight, near-zero-weight, and cluster-cap edge cases. Behavioral integrity gap: developer can use GE-2 framing to avoid preregistration. | PROTOCOL_SPEC.md Section J1 defines bright-line rules for edge cases: (a) zero-weight skill allocation = GE-3 (preregistration required), (b) cluster-cap change forcing near-zero = GE-3, (c) differential timeframe weighting rule. | — |
| TASK-AF-019 | F-19 | P2 | Open | `docs/AUDIT_v1.md` | HWM, purge/embargo, and walk-forward window parameters absent from GLOSSARY.md despite stated coverage claim. HWM reset timing (phase-boundary / annual / inception) unspecified. | GLOSSARY.md adds: HWM (with reset timing rule), purge/embargo (with formula or value cross-reference to TASK-AF-012), walk-forward window parameters (4yr IS / 1yr OOS / annual roll). | — |
| TASK-AF-020 | F-20 | P2 | Open | `docs/AUDIT_v1.md` | K5 measurement period ambiguous: "any 12-month period" — rolling vs. calendar year vs. fixed windows from treasury activation date unspecified. | CHARTER.md and PROTOCOL_SPEC.md Section J specify K5 measurement as rolling (evaluated monthly) or calendar-year with explicit cutoff rule. | — |
| TASK-AF-021 | F-21 | P2 | Open | `docs/AUDIT_v1.md` | Phase 0 P1 circuit breaker verification criterion is untestable as stated. "Tested with synthetic data and verified" has no minimum test suite. Developer self-certifies against undefined protocol. | Phase 0 exit criteria list minimum required test scenarios for P1 circuit breaker: at least simultaneous P1+P3 firing, P1 recovery with P3 still active, restart mid-suspension, partial position reduction. Test cases enumerated, not implied. | — |

### Cycle 1 Additions (F-22..F-32)

| Task ID | Finding ID | Severity | Status | Source Audit | Summary | Acceptance Criterion | ADR/PR |
|---|---|---|---|---|---|---|---|
| TASK-AF-022 | F-22 | P1 | Open | `docs/audit/REVIEW_REPORT.md` | Net Sharpe stream wording drifts (`a+b+c` vs `a+c`) across docs/tables. | All references to net Sharpe stream composition use identical definition `(a+b+c)`. | — |
| TASK-AF-023 | F-23 | P0 | Open | `docs/audit/REVIEW_REPORT.md` | RDL operational boundary conflict: "Phase 2+" vs "after Phase 2 exit criteria". | PROTOCOL_SPEC/workflow/GLOSSARY express one canonical boundary rule with no contradiction. | — |
| TASK-AF-024 | F-24 | P0 | Open | `docs/audit/REVIEW_REPORT.md` | RDL submission-time trial-count rule exists only in PROTOCOL_SPEC. | Rule appears in all canonical governance references (at minimum PROTOCOL_SPEC + GLOSSARY + workflow policy). | — |
| TASK-AF-025 | F-25 | P0 | Open | `docs/audit/REVIEW_REPORT.md` | RDL->RBE non-interaction control is not propagated outside module text. | Governance checklist includes explicit non-interaction verifier and evidence pointer. | — |
| TASK-AF-026 | F-26 | P1 | Open | `docs/audit/REVIEW_REPORT.md` | "Charter-level review" for RBE has no operational definition/authority schema. | Every RBE activation has a compliant review artifact (role, format, storage, approval fields). | — |
| TASK-AF-027 | F-27 | P2 | Open | `docs/audit/REVIEW_REPORT.md` | Explicit 4->5 gate topology missing; Phase 5 prerequisites skip direct dependency expression. | Phase transition map is unambiguous for optional Phase 4 bypass and treasury activation path. | — |
| TASK-AF-028 | F-28 | P2 | Open | `docs/audit/REVIEW_REPORT.md` | No machine-checkable RDL dormancy attestation artifact pre-Phase-2. | Pre-Phase-2 RDL mode attestation is machine-checkable and auditable by third party. | — |
| TASK-AF-029 | F-29 | P1 | Open | `docs/audit/REVIEW_REPORT.md` | K3 verdict can flip by N_eff estimator choice for heterogeneous clusters. | K3 estimator and boundary behavior are locked so same inputs produce same verdict across tools. | — |
| TASK-AF-030 | F-30 | P0 | Open | `docs/audit/REVIEW_REPORT.md` | Phase-2 activation behavior for scaffolded RDL hypotheses is unspecified. | Promotion queue and batch-limit policy make Phase-2 trial-count transition deterministic. | — |
| TASK-AF-031 | F-31 | P0 | Open | `docs/audit/REVIEW_REPORT.md` | RBE/kill-criteria interaction windows undefined during risk-budget changes. | K1-K6 evaluation windows remain auditable and continuous through RBE transitions. | — |
| TASK-AF-032 | F-32 | P1 | Open | `docs/audit/REVIEW_REPORT.md` | GE-2/GE-3 can be exploited to suppress trial counting via zero-weight framing. | Zero-weight persistence is explicitly GE-3 and trial-counted deterministically. | — |

---

## Development Backlog

*(Use this section for non-audit tasks: Phase 0 infrastructure, data pipeline, evaluation engine, etc.)*

| Task ID | Phase | Status | Summary | Acceptance Criterion |
|---|---|---|---|---|
| TASK-DEV-001 | Phase 0 | Open | Build walk-forward harness | Phase 0 exit criteria met per PROTOCOL_SPEC.md Section F |
| TASK-DEV-002 | Phase 0 | Open | Build SimBroker with cost model | Phase 0 exit criteria met; cost within 15% of paper fills |
| TASK-DEV-003 | Phase 0 | Open | Implement P1–P4 regime signal hierarchy | P1 circuit breaker passes test suite (resolves TASK-AF-021 as prerequisite) |
| TASK-DEV-004 | Phase 0 | Open | Implement evaluation engine | Phase 0 exit criteria met; leakage audit passes |

---

## Dependency Notes

- **TASK-AF-001** (Harvey-Liu formula) must be resolved before TASK-AF-002 (CI correction) is finalized, as the formula choice affects how trials are counted in the CI computation.
- **TASK-AF-003** (P3 population) and **TASK-AF-004** (P4 algorithm) must be resolved before TASK-DEV-003 (regime signal implementation) begins.
- **TASK-AF-005** (IC_long suspect threshold) is a prerequisite for any Phase 1 performance evaluation being considered valid.
- **TASK-AF-007** (vintage contamination) must be resolved before Phase 0 P4 calibration begins, as the answer determines the calibration procedure.
- **TASK-AF-012** (embargo length) is a prerequisite for TASK-DEV-004 (evaluation engine) passing the Phase 0 leakage audit.

---

*Version: 1.1 | Date: 2026-03-04*
*Audit sources: `docs/AUDIT_v1.md` v1.0; `docs/audit/REVIEW_REPORT.md` Cycle 1*
*See also: `docs/audit/REVIEW_REPORT.md` (consolidated findings), `docs/audit/AUDIT_INDEX.md` (artifact registry)*
