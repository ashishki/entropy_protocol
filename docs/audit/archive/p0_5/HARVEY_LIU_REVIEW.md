# HARVEY_LIU_REVIEW
_Date: 2026-05-05 · Scope: P0.6-005 implementation review of `HL-HB-v1`_

## Verdict

Decision: `IMPLEMENTATION_REVISED_PACKET_REQUIRED`.

The P0.6-005 `compute_harvey_liu_family()` workflow implements the required
family-table `HL-HB-v1` shape: complete family membership, one-sided
positive-edge p-values, sorted Holm-Bonferroni adjustment, Sharpe-equivalent
deflated values, and required report hashes.

This is still not a Phase 0 gate approval by itself. A concrete report packet
must supply the actual Main/AT/`RDL-*` family rows, policy/code hashes, and
reviewed source context before Harvey-Liu values can support report or gate
claims. The legacy `compute_harvey_liu_deflation()` helper remains a provisional
single-trial scaffold and must not be used as gate proof.

## Reviewed Artifacts

| Artifact | Role |
|----------|------|
| `docs/core/PROTOCOL_SPEC.md` Harvey-Liu Haircut Method | Canonical workflow |
| `docs/core/GLOSSARY.md` Deflated Sharpe | Canonical report fields and interpretation |
| `docs/audit/D010_CLOSURE_PACKET.md` F-1 | Audit closure rationale and evidence requirements |
| `docs/audit/T23_FORMULA_GOVERNANCE_DISPOSITION.md` | Narrow permission for provisional helper |
| `entropy/stats/analysis.py` | Current implementation |
| `tests/unit/test_stats.py` | Current implementation tests |

## Canonical Requirements

`HL-HB-v1` requires:

- family-scoped trial set;
- `M_total` across Main Track, AT, and `RDL-*` submissions;
- `raw_sharpe_annual_i / se_sharpe_annual_i` per family member;
- one-sided positive-edge p-value per family member;
- sorted Holm-Bonferroni adjustment;
- mapping back to Sharpe-equivalent deflated values;
- report fields: `M_total`, family membership, raw p-value, adjusted p-value,
  raw Sharpe, deflated Sharpe, haircut units, method ID, code hash, and policy
  hash;
- no gate claim if any required family p-value is unavailable.

## Current Helper Assessment

| Check | Result | Notes |
|-------|--------|-------|
| Method ID exposed | Pass | `HL-HB-v1` is exposed |
| Legacy scaffold warning | Pass | `compute_harvey_liu_deflation()` keeps explicit stub warning |
| Returns raw/deflated/haircut fields | Pass | `DeflatedSharpe` exposes raw, deflated, and haircut units |
| Full family input | Pass | `HarveyLiuTrial` table is required by `compute_harvey_liu_family()` |
| One-sided positive-edge p-value | Pass | Computed from `raw_sharpe_annual / se_sharpe_annual` |
| Holm sorted workflow | Pass | Sorted Holm-Bonferroni adjustment is applied and mapped back by trial ID |
| Family membership fields | Pass | Result includes family tag, family membership, rank, and `M_total` |
| Required hashes | Pass | Trial inputs require nonblank code hash and policy hash |
| Missing-family-p-value guard | Pass | `M_total` must equal supplied family membership count |
| Gate/report acceptance | Packet-required | Tooling is implemented; actual report packet and reviewer acceptance remain required |

## Worked Example

P0.6-005 tests reproduce the canonical three-trial family example:

| Trial | Raw Sharpe | SE | z | Raw p | Holm p | Deflated Sharpe | Haircut |
|-------|------------|----|---|-------|--------|------------------|---------|
| A | 0.35 | 0.25 | 1.40 | ~0.0808 | ~0.242 | ~0.175 | ~0.175 |
| B | 0.25 | 0.25 | 1.00 | ~0.1587 | ~0.317 | ~0.119 | ~0.131 |
| C | 0.10 | 0.25 | 0.40 | ~0.3446 | ~0.345 | ~0.100 | ~0.000 |

Any future accepted report packet must include enough precision for a second reviewer to
reproduce the p-values, ranks, adjusted p-values, inverse-normal mapping, and
haircut units.

## Failure Cases Covered

P0.6-005 tests cover:

- inconsistent `M_total` versus family membership count;
- duplicate trial IDs;
- missing family tag;
- zero or negative Sharpe SE;
- policy hash or code hash omitted from report context;
- legacy single-trial scaffold still marked with `stub_pending_formula_verification`.

## Remaining Packet Requirements

Before report/gate use, the next packet layer must add:

1. Actual Main Track, AT, and `RDL-*` family rows for the report scope.
2. Report-level guard rejecting any missing required family row.
3. Report-level guard rejecting `stub_pending_formula_verification` values as
   phase-exit proof.
4. Human review of policy hash, code hash, and family-membership context.
5. Phase packet text that clearly separates helper implementation from accepted
   Harvey-Liu evidence.

## Decision Boundary

This review accepts the P0.6-005 implementation as deterministic tooling for
future Harvey-Liu packets. It does not approve OOS claims, final report claims,
or Phase 0 gate closure without a concrete packet using real family membership
and reviewed hashes.
