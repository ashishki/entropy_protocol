# Statistical Report Gate Packet

Date: 2026-05-05
Status: ACCEPTED_AS_REPORT_BOUNDARY_EVIDENCE

## Scope

Accept the revised Sharpe CI and Harvey-Liu family workflow as report-boundary
tooling, while preserving the no-performance-claim boundary.

## Artifact

| Artifact | Path |
|---|---|
| Manifest | `artifacts/evidence/statistical_gate/STATISTICAL_REPORT_GATE_MANIFEST.json` |

## Sharpe CI

Method: `CI-SR-ACF-v1`.

Accepted report fields:

- return frequency;
- annualization factor;
- `n`;
- preregistered lag;
- autocorrelation hash;
- `n_eff`;
- `T_eff_years`;
- Sharpe estimate;
- Sharpe standard error;
- 68% CI lower/upper;
- method ID;
- policy hash.

Status: accepted as report-boundary tooling.

## Harvey-Liu

Method: `HL-HB-v1`.

Accepted helper:

- `compute_harvey_liu_family()`.

Rejected for gate/report proof:

- legacy `compute_harvey_liu_deflation()` single-trial scaffold;
- missing family rows;
- inconsistent `M_total`;
- missing code hash or policy hash.

Status: accepted as report-boundary tooling.

## Verification

Commands:

- `.venv/bin/pytest tests/unit/test_stats.py`
- `.venv/bin/ruff check entropy/stats/analysis.py tests/unit/test_stats.py`

Result:

- pytest: 10 passed;
- ruff: passed.

## Acceptance

Accept this packet as the current statistical report-boundary evidence. The
Sharpe CI and Harvey-Liu report packet blocker is closed for tooling/report
shape.

## Boundary

This packet does not approve Phase 0, start Phase 1, validate any strategy,
authorize OOS/performance claims, or replace future real family/report rows.
