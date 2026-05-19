# Phase 24 Regression Decisions

Status: active T107 record
Date: 2026-05-15

This file records how Phase 23/24 discovered report issues were converted into
regression coverage or classified as docs-only accepted limitations.

## Regression Coverage Added

| Issue source | Risk | Regression decision |
|---|---|---|
| Phase 23/24 open-source evidence boundary | Report or packet copy could turn open-source/demo artifact quality into PMF, customer validation, market demand, or paid-pilot evidence claims. | Added `evidence_overclaim` claim-guard forbidden phrases and tests in `tests/unit/reporting/test_claim_guard.py`. |

The new claim-guard coverage blocks positive overclaims such as "proves PMF",
"demo evidence proves customer demand", and "open-source pack is paid-pilot
evidence". It intentionally allows negative boundary language such as "not PMF
evidence" and "not proof that traders will pay".

## Docs-Only Accepted Limitations

| Finding | Reason no code regression was added | Required preservation |
|---|---|---|
| `PH23-P2-001` SEC Form 4 source limitation | The report generator already supports limitation sections; the issue is source-shape truthfulness, not calculation behavior. | Keep SEC Form 4 as internal reference only and preserve the reviewed-report caveat that P&L, drawdown, leverage, and trading intent are unsupported. |
| `PH23-P2-002` public sample P&L wording caveat | The attribution engine is behaving as designed: affected P&L can be `0` when flagged rows are not realized closing rows. The current mitigation is reviewed-copy wording plus a future fixture where realized loss and violation rows align. | Keep the reviewed-copy caveat visible; fill `future_realized_loss_pnl_wording_001` before stronger P&L demo claims. |
| `PH23-P2-003` synthetic provenance caveat | Synthetic provenance is a case-bank labeling issue, not a report-generation defect. | Keep synthetic provenance visible and never present the pack as customer, market, PMF, or willingness-to-pay evidence. |
| `synthetic_limit_leverage_001` missing leverage | This is expected evaluator behavior already covered by unsupported leverage tests and visible report limitations. | Keep leverage as an accepted limitation unless an explicit leverage/margin field is available. |
| `synthetic_schema_reject_missing_price_001` missing price | This is expected schema rejection behavior; no report artifact is produced. | Keep the blocked/rejection-only status visible in dashboards and demo-pack talk tracks. |

## Follow-Up Test Candidates

These are not required for T107 because they need new fixtures, but they remain
the next useful regression expansion:

1. `future_session_timezone_boundary_001` for local session start/midnight
   grouping.
2. `future_drawdown_only_001` for drawdown-only report wording.
3. `future_realized_loss_pnl_wording_001` for unambiguous affected-P&L
   language.
4. `future_no_breach_control_001` for no-breach wording without performance
   endorsement.
