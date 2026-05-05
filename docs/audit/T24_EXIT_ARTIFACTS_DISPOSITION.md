# T24_EXIT_ARTIFACTS_DISPOSITION
_Date: 2026-05-05 · Decision ID: D-020_

## Verdict

T24 may proceed under a narrow, task-specific evidence-governance disposition.
This is not a global D-010 closure and does not mark Phase 0 as passed.

## Rationale

T24 emits Phase 0 exit artifacts, which are governance-sensitive because reports
can be mistaken for phase-gate approval or OOS performance evidence. The project
goal at this point is to complete the Phase 0 foundation so the full result can
be analyzed after T24. The implementation may therefore generate deterministic
implementation evidence, but it must not claim scientific validation, RDL/K-report
coverage, or human phase-gate approval.

## Allowed T24 Scope

T24 may implement only:

- reproducible Markdown evaluation reports from registered trial and run records;
- leakage evidence collection from explicitly supplied T19 `LeakageReport`
  objects for registered runs;
- append-only evidence-index row writing to a caller-supplied or default
  `EVIDENCE_INDEX.md` path;
- deterministic Phase 0 task-status report rendering for T01-T24;
- explicit `NOT_APPROVED` phase-gate status unless a caller supplies separate
  human-approval evidence.

## Prohibited T24 Scope

T24 must not implement:

- automatic phase-gate approval;
- OOS performance claims;
- K-report generation or epoch coverage closure;
- RDL promotion telemetry or closure claims for F-30/F-31;
- statistical validation beyond reporting already available fields;
- live data access, external network egress, or runtime service escalation.

## D-010 Finding Disposition for T24

| Finding | T24 disposition |
|---------|-----------------|
| F-1 Harvey-Liu | T24 may report existing/stub fields only; no new formula validation. |
| F-2 Sharpe CI | T24 may report existing/stub fields only; no phase-gate proof. |
| F-4 P4 reproducibility | Out of T24 scope; no P4 labeler. |
| F-5 IC_long / FLAM | Out of T24 scope; no IC/BR/FLAM code. |
| F-30 RDL telemetry | Future real-evidence gate; T24 must not emit RDL telemetry or claim closure. |
| F-31 K-report epoch coverage | Future real-evidence gate; T24 must not emit K-report artifacts or claim closure. |

## Required T24 Review Focus

The T24 implementation review must verify:

1. Evaluation reports are byte-identical for identical DB state.
2. Reports include hashes, IS/OOS windows, leakage status, and explicit
   `not_computed` metric placeholders when no metric exists.
3. Leakage evidence appends rows only when every registered run has a supplied
   PASS `LeakageReport`.
4. Missing leakage reports raise `EvidenceCollectionError`.
5. Phase 0 gate reports list T01-T24 and do not mark the phase gate as approved
   without explicit caller-supplied approval.
6. T24 does not emit RDL, K-report, OOS-claim, P4, IC/BR, FLAM, or automatic
   phase-gate approval artifacts.

## Decision

Record as D-020. T24 implementation may begin under these constraints.
