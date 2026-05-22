# Three-Channel V1 Scorecard

Date: 2026-05-19
Status: internal_v1_recompute_not_external_ready

## Method

- V1 applies `SAS-V1-002` review decisions to V0 evaluated claims.
- Reviewed false positives and `needs_context` rows are excluded.
- Reviewed false negatives are counted as pending extraction, not wins/losses.
- No unreviewed media claim is included.
- No bulk market-history database is used.

## Channel Scorecard

| Channel | Coverage | Extraction quality | Outcome quality | Risk quality | Evidence limitations |
|---|---:|---|---|---|---|
| `bablos79` | 14/19 evaluable | reviewed fp/context exclusions: 5 | hit rate 64.285714%, avg return 0.742848% | RR rows 0 | false negatives pending 0; media excluded |
| `nemphiscrypts` | 49/53 evaluable | reviewed fp/context exclusions: 4 | hit rate 57.142857%, avg return 0.434858% | RR rows 0 | false negatives pending 2; media excluded |
| `pifagortrade` | 107/112 evaluable | reviewed fp/context exclusions: 6 | hit rate 52.336449%, avg return -0.153127% | RR rows 0 | false negatives pending 3; media excluded |

## External Boundary

This scorecard is internal. Customer-facing use still requires the V1 external-ready gate.
