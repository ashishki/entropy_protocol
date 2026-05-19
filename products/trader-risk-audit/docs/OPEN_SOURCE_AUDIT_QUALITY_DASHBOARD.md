# Open-Source Audit Quality Dashboard

Status: active dashboard with Phase 27 rehearsal update
Date: 2026-05-19

This dashboard summarizes the Phase 23 case-bank outputs for Phase 24
readiness decisions. It is aggregate and privacy-safe. It does not include raw
trade rows and must not be used as paid-pilot, PMF, customer validation,
trading advice, or hosted-product readiness evidence.

## Readiness Summary

| Category | Count | Packs | Decision |
|---|---:|---|---|
| Controlled internal demo-quality | 3 | `public_sample_001`, `risk_audit_case_001`, `synthetic_limit_leverage_001` | Enough for Phase 24 controlled internal demo pack assembly: positive-finding and limitation examples are both represented. |
| Real open-data rehearsal only | 2 | `real_open_dex_swaps_001`, `real_open_dex_contract_sequence_001` | Useful for development rehearsal on real public data; not private, paid-pilot, customer, PMF, or market-demand evidence. |
| Internal reference only | 1 | `open_source_sec_form4_001` | Keep as the high-traceability reference, not as customer-ledger evidence. |
| Blocked / rejection-only | 1 | `synthetic_schema_reject_missing_price_001` | Keep visible as schema-rejection evidence; no report demo. |

No pack has unresolved P0 or P1 report-validity findings. The open Phase 23 P2
items remain accepted caveats and must stay visible in any reviewed demo copy.

## Pack Dashboard

| Case pack | Pack status | Quality class | Scorecard result | Findings | Limitations | Error-register status | Reproducibility status | Operator note |
|---|---|---|---|---:|---:|---|---|---|
| `open_source_sec_form4_001` | complete reference | internal reference only | 17 / 18, no fail condition | 7 | 3 | `PH23-P2-001` accepted source limitation | passed | Strong traceability reference, but SEC disclosures are not customer account ledgers and cannot support P&L, drawdown, leverage, or trading-intent claims. |
| `public_sample_001` | complete | controlled internal demo-quality positive example | 14 / 18, no fail condition; reviewed-copy caveat required | 9 | 0 | `PH23-P2-002` accepted P&L wording caveat | passed | Useful positive-finding sample only when the reviewed caveat about affected P&L wording stays above the generated body. |
| `risk_audit_case_001` | complete | controlled internal demo-quality positive example | 16 / 18, no fail condition; synthetic provenance required | 13 | 0 | `PH23-P2-003` accepted provenance caveat | passed | Best positive pack for non-zero violating P&L and source-row traceability; synthetic provenance must stay visible. |
| `synthetic_limit_leverage_001` | complete | controlled internal demo-quality limitation example | 15 / 18, no fail condition | 0 | 1 | expected limitation; no registered P2 | passed | Demonstrates that unsupported leverage is reported as a limitation rather than guessed. |
| `synthetic_schema_reject_missing_price_001` | rejected | blocked / rejection-only | not scored; no report artifact | 0 | 0 | expected schema rejection; no registered P2 | not applicable | Missing `price` blocks report generation; only safe `run_status.json` exists. |
| `real_open_dex_swaps_001` | complete rehearsal | real open-data rehearsal only | manual review complete; scorecard not used for private-readiness claims | 8 | 1 | `PH27-P2-001`, `PH27-P2-002` accepted caveats | passed | Real Uniswap V2 WETH/USDC pair-level swaps exercise the workflow on public on-chain data, but they are not a trader account ledger and do not close T116. |
| `real_open_dex_contract_sequence_001` | complete rehearsal | real open-data rehearsal only | manual review complete; scorecard not used for private-readiness claims | 0 | 1 | `PH28-P2-001`, `PH28-P2-002` accepted caveats | passed | Real Uniswap V2 WETH/USDC swaps filtered to a repeated public contract recipient; useful no-breach/control-style rehearsal, but still not a verified trader ledger and does not close T116. |

## Quality Class Definitions

Controlled internal demo-quality:

- reviewed report exists and passes the scorecard threshold of 14+ with no fail
  condition;
- no unresolved P0/P1 report-validity finding;
- caveats are visible before any generated report body;
- the pack is used only to show artifact quality, rule behavior, or limitation
  handling, not market demand or customer outcomes.

Internal reference only:

- report quality is high, but the source shape is too far from a customer
  ledger for positive demo positioning;
- useful for traceability, reproducibility, and limitation wording review.

Real open-data rehearsal only:

- data is real and public, not synthetic;
- source is not private/anonymized pilot data;
- useful for extraction and report-review development;
- cannot be counted as customer, paid-pilot, PMF, market-demand, or
  private-report readiness evidence.

Blocked / rejection-only:

- no generated report or delivery packet may be shown as an audit result;
- the safe rejection status can be used to explain intake/schema boundaries.

## Limitation And Finding Totals

| Metric | Count |
|---|---:|
| Complete packs | 6 |
| Rejected packs | 1 |
| Total deterministic findings in complete packs | 37 |
| Total explicit limitations in complete packs | 6 |
| Packs with passed reproducibility | 6 |
| Packs with not-applicable reproducibility due expected rejection | 1 |
| Unresolved P0/P1 findings | 0 |
| Accepted P2 caveats | 7 |

## Next Concrete Gap

The next case/data gap before private-pilot readiness is
`future_session_timezone_boundary_001`: a runnable fixture with trades crossing
local session start or midnight, exercising daily-loss and cooldown grouping
with an unambiguous P&L explanation. This should be filled before claiming the
reports are robust for real trader exports across timezones.

Secondary gaps remain:

1. `future_drawdown_only_001` for a drawdown-focused report without cooldown or
   forbidden-asset overlap.
2. `future_realized_loss_pnl_wording_001` for affected-P&L wording where the
   violation rows and realized-loss rows are intentionally aligned.
3. `future_no_breach_control_001` for a clean report that says "no breach"
   without implying profitable or safe trading.

Leverage-supported and fee-specific demos remain accepted limitations unless a
future fixture or pilot input includes explicit fields that the deterministic
rule catalog can evaluate.

## Dashboard Decision

Phase 24 has enough controlled internal demo-quality material to assemble a
positive-plus-limitation demo pack, but not enough evidence to claim
private-pilot readiness. The dashboard should drive T107 regression decisions
and T108 demo-pack assembly while keeping all P2 caveats and blocked/rejected
cases visible.

Phase 27 adds `real_open_dex_swaps_001` as development rehearsal evidence only.
It improves confidence that the local workflow can handle real public
transaction-like rows, but it does not change the paid-pilot ready gate:
`docs/PAID_PILOT_READY_GATE.md` remains `needs_fixes` until T116 private or
anonymized evidence exists.

Phase 28 adds `real_open_dex_contract_sequence_001` as a more scoped no-key
contract-recipient sequence. It is useful as real-open-data no-breach/control
coverage, but it still does not prove private report readiness.
