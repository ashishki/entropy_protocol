# Archive — Historical Design Documents

**Purpose:** Preserved reasoning documents from the iterative design process (v1–v4). These are NOT active specifications.

These documents explain why current constraints exist. They are not superseded in the sense of being wrong — they are superseded in the sense that their conclusions have been incorporated into `CHARTER.md` and `PROTOCOL_SPEC.md`.

**Do not use archived documents as context for implementation or specification work.** Use `docs/EVOLUTION.md` instead, which summarizes the key decisions and their rationale in a single navigable document.

---

## Archive Index

| File | Version | Date | Role in Design History |
|---|---|---|---|
| `strategic_architecture_review_v1.md` | v1.0 | 2026-03-02 | Initial stress test. Identified evaluation-first principle and factor collapse as primary risks. Contained optimism bias on Sharpe estimates. |
| `strategic_architecture_review_v2.md` | v2.0 | 2026-03-02 | Correction pass. Revised net Sharpe base case to 0.28–0.40. Added treasury layer discussion. Established four-stream P&L as non-negotiable. |
| `strategic_architecture_review_v3.md` | v3.0 | 2026-03-02 | Evolution pass. Added 1W regime overlay and short positions under gross ≤ 1. Introduced four regime-adjacent signals without conflict resolution — later corrected. |
| `strategic_architecture_review_v4.md` | v4.0 | 2026-03-02 | Independent quant audit of v3. Adversarial review. Identified 3 mandatory corrections: FLAM derivation error, K4 false-kill rate, crypto stop-loss cost model failure. All three incorporated into v5 charter. |
| `deep-research-report.md` | — | 2026-03-02 | Literature-backed feasibility validation. Provides academic references for core design choices. Not an active specification. |

---

## Notes on v4

`strategic_architecture_review_v4.md` is the most important archive document. It contains the specific numerical derivations and adversarial challenges that produced the three mandatory corrections in `CHARTER.md`. If a future review challenges the FLAM derivation, stop-loss cost model, or K4 definition, read v4 Section 1.3, 4.3, and 5.3 respectively before responding.

---

## Notes on `deep-research-report.md`

Contains literature citations for:
- Selection bias and multiple testing controls (Harvey-Liu framework)
- Covariance estimation (Ledoit-Wolf shrinkage rationale)
- Cost model calibration references
- Factor redundancy in small universes

Useful as background if academic justification for a design choice is needed.
