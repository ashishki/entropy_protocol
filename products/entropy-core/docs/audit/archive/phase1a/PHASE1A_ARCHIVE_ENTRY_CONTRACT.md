# Phase 1A Archive Entry Contract

Date: 2026-05-05
Task: P1A-001
Status: APPROVED_FOR_NEXT_TASK_GRAPH

## Decision

Phase 1A may proceed only as archive-only baseline planning and instrumentation.
This contract freezes the entry boundaries before any long-only skill,
portfolio-layer, archive-evaluation, Growth monitoring, or RDL-adjacent
implementation.

This contract does not authorize Phase 1 implementation, live feeds, live
capital, streaming providers, live broker integration, OOS/performance claims,
RDL hypothesis generation, or RBE activation.

## Finding Closure Map

| Finding | Required closure | Contract section |
|---|---|---|
| F-C3-001 | Archive dataset freeze rules | Dataset Freeze |
| F-C3-002 | IS/OOS split contract | Archive Split Contract |
| F-C3-003 | Baseline long-only skill boundary | Skill Boundary |
| F-C3-004 | Portfolio constraints | Portfolio Boundary |
| F-C3-005 | Growth monitoring-only scope | Growth Boundary |
| F-C3-006 | RDL dormancy attestation | RDL Boundary |

## Dataset Freeze

The initial Phase 1A archive dataset universe is restricted to the 15
archive-validated assets already used by the revised P4 and archive
data-stability packets:

`ADAUSDT`, `ALGOUSDT`, `ATOMUSDT`, `BCHUSDT`, `BNBUSDT`, `BTCUSDT`, `DOGEUSDT`,
`ETCUSDT`, `ETHUSDT`, `LINKUSDT`, `LTCUSDT`, `TRXUSDT`, `VETUSDT`, `XLMUSDT`,
`XRPUSDT`.

Admissible initial dataset artifacts:

| Dataset family | Window | Timeframe | Status |
|---|---|---|---|
| Revised Binance public archive converted full windows | 2020-01-01 through 2025-12-31 | 1d | Frozen for initial Phase 1A planning |

Freeze rules:

- Dataset rows, schema, and hashes are immutable inputs.
- Any additional timeframe, asset, source, or window requires a new source
  manifest and an explicit contract addendum before strategy code may inspect
  it.
- Missing live data is not a blocker for Phase 1A because Phase 1A is
  archive-only.
- Archive source evidence must cite the existing conversion manifests and the
  archive data-stability manifest.
- No result generated from these archives may be labeled live, production, or
  capital-ready.

## Archive Split Contract

The first archive split policy is contract-only and must be implemented in a
later task before any archive evaluation run.

| Segment | Window | Label | Use |
|---|---|---|---|
| Archive formation | 2020-01-01 through 2022-12-31 | `ARCHIVE_FORMATION` | Feature/skill design, warmup, implementation tests |
| Archive validation | 2023-01-01 through 2024-12-31 | `ARCHIVE_VALIDATION` | Registered archive walk-forward development |
| Archive holdout | 2025-01-01 through 2025-12-31 | `ARCHIVE_HOLDOUT` | Final archive-only sanity check after registration |

Rules:

- `ARCHIVE_HOLDOUT` must not be read during feature design, skill selection,
  parameter selection, portfolio constraint selection, or registry-family
  selection.
- No artifact may call archive holdout output `OOS performance`.
- Archive reports must use the label `archive-only`, not `live`, `production`,
  or `capital-ready`.
- P4 labels referenced by archive reports must preserve their existing
  `p4_version`, `p4_param_hash`, `label_generation_ts`, and `dataset_hash`.
- Purge/embargo must use the accepted max-horizon methodology already included
  in the registered leakage gate packet.

## Skill Boundary

Phase 1A does not implement skills. It freezes what a later archive-only skill
task may propose.

Allowed baseline scope:

- long-only only;
- maximum 6 skill families;
- 1d archive inputs for the initial contract;
- OHLCV-derived deterministic features only;
- preregistered parameters before validation or holdout reads;
- no short selling, leverage, derivatives, treasury allocation, RDL-generated
  hypotheses, AI-generated signals, or Growth-generated signal changes.

Any modification to signal entry conditions, exit conditions, feature
definitions, or look-back parameters after registration is treated as a new
trial-family event and requires preregistration before related data is examined.

## Portfolio Boundary

Phase 1A portfolio work, when separately approved, must stay within these
constraints:

| Constraint | Value |
|---|---|
| Direction | Long-only |
| Gross exposure | `0.0 <= gross <= 1.0` |
| Short exposure | `0.0` |
| Leverage | None |
| Rebalance policy | Must be deterministic and preregistered before archive validation |
| Regime controls | P1/P3/P4 states may be reported or applied only according to registered policy |
| Treasury stream | Report-only if present; excluded from Net Sharpe |

Portfolio allocation changes may not change signal definitions. Allocation-only
changes that affect evaluation must be registered with a policy hash before the
archive validation segment is read.

## Growth Boundary

Growth Layer work in Phase 1A is monitoring-only and facts-only.

Allowed:

- define metric schemas for CRR, capital utilization, N_eff, turnover, and
  cost-drag reporting;
- emit factual state reports with visible denominators and basis counts;
- store policy hashes and report hashes for later audit.

Forbidden:

- RBE step transition above Step 0;
- recommendations, rankings, severity framing, or action prescriptions;
- signal changes;
- position-sizing changes;
- gross or volatility target increases;
- any claim that Growth output improves performance.

## RDL Boundary

RDL remains dormant for Phase 1A.

Allowed:

- documentation of the dormancy check;
- schema placeholders only if a later task explicitly approves scaffolding;
- no runtime module connected to portfolio, registry submission, Growth, RBE,
  or evaluation paths.

Required attestation before any RDL-adjacent task:

| Check | Required result |
|---|---|
| `RDL_MODE` | `scaffold_only` or absent with no runtime RDL module |
| Portfolio reads from RDL | none |
| RBE reads from RDL | none |
| Trial Registry `RDL-*` submissions | none in Phase 1A |
| RDL-generated hypotheses | none |

## No-Claim Labels

Allowed report labels:

- `archive-only`;
- `archive-formation`;
- `archive-validation`;
- `archive-holdout`;
- `implementation-evidence`;
- `not_phase_gate_approval`.

Forbidden report labels:

- `live`;
- `production`;
- `capital-ready`;
- `OOS performance`;
- `validated alpha`;
- `RDL telemetry closed`;
- `K-report closed`;
- `RBE activated`.

## Next Task Gate

P1A-001 is complete when this contract is indexed and Cycle 3 findings
F-C3-001 through F-C3-006 are marked closed by contract. The next implementation
task must derive from this contract and must not inspect archive validation or
holdout results before its own registration boundary is recorded.

