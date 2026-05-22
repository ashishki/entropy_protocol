# ARCH_REPORT - Cycle 35
_Date: 2026-05-19_

## Component Verdicts

| Component | Verdict | Note |
|-----------|---------|------|
| Dune source discovery | PASS | Real public `dex.trades` rows were queried without committing the supplied key. |
| Dune case pack | PASS | Canonical CSV, policy, report, manifest, reviewed report, and reproducibility status exist. |
| Case validator | PASS | New pack passes the existing open-source case-pack contract. |
| Docs | PASS | Dune usage, review caveats, and gate limits are documented. |
| Paid-pilot ready gate | PASS | Gate remains `needs_fixes`; Phase 32 does not close T116. |

## Contract Compliance

| Rule | Verdict | Note |
|------|---------|------|
| Deterministic violation truth | PASS | Existing evaluator/reporting logic was reused; 76 max-position findings are source-row traceable. |
| Human approval boundaries | PASS | T116 still requires operator-approved private/anonymized input outside git. |
| Evidence boundary | PASS | Dune public data is development/report-review evidence only. |
| Confidential data handling | PASS | No key, private rows, private paths, customer identifiers, or wallet-owner claims are committed. |
| Report claim boundaries | PASS | Reviewed report and docs preserve unsupported fee/leverage/P&L limitations. |
| Runtime boundary | PASS | No hosted service, checkout, live exchange control, or background import was added. |

## Architecture Findings

| ID | Severity | Finding | Status |
|----|----------|---------|--------|
| PH32-P2-001 | P2 | Public Dune submitter scope is not a verified private trader ledger. | Accepted limitation |
| PH32-P2-002 | P2 | Dune transform lacks execution costs, leverage, balances, and verified realized P&L. | Accepted limitation |

## Right-Sizing / Runtime Checks

| Check | Verdict | Note |
|-------|---------|------|
| Solution shape still appropriate | PASS | Phase 32 stays in local CLI/docs/artifact workflow. |
| Runtime tier unchanged | PASS | Runtime remains T0 local CLI/file workflow plus one manual Dune API extraction. |
| Scope boundary preserved | PASS | No SaaS/checkout/live-control expansion; T116 remains blocked. |

## Doc Patches Applied

| File | Section | Change |
|------|---------|--------|
| `docs/tasks.md` | Phase 32 / T137-T140 | Added completed Dune rehearsal tasks. |
| `docs/DUNE_PUBLIC_WALLET_REHEARSAL.md` | New | Documented source, transform, evidence, and conversation use. |
| `docs/PAID_PILOT_READY_GATE.md` | Evidence review | Added Dune row while preserving `needs_fixes`. |
| State docs | Active State | Recorded T140 completion and T116 blocker. |
