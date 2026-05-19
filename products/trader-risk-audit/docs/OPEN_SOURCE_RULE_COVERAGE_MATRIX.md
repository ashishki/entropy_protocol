# Open-Source Rule Coverage Matrix

Status: active matrix with Phase 27 rehearsal update
Date: 2026-05-19

This matrix maps the current open-source validation packs to deterministic rule
coverage, required data fields, unsupported fields, report sections, and
follow-up coverage needs. It is artifact-quality evidence only. It is not
paid-pilot evidence, PMF evidence, customer validation, trading advice, or a
claim that the report is ready for hosted uploads or live exchange control.

## Pack Coverage

| Case pack | Pack status | Rule types exercised | Required fields exercised | Unsupported or absent fields | Report sections exercised | Current limitation |
|---|---|---|---|---|---|---|
| `open_source_sec_form4_001` | complete reference | `max_position_size` as transaction-notional proxy; `forbidden_assets`; unsupported `max_leverage` register | `timestamp`, `symbol`, `side`, `quantity`, `price`, `fees`, `account_id` | Real account ledger, realized P&L semantics, drawdown, balances, leverage, trader intent | executive summary, run context, rule coverage, violation table, P&L attribution, limitation register, operator checklist | SEC rows are public disclosures, not customer trades; position size is a proxy and P&L/drawdown/leverage cannot be inferred. |
| `public_sample_001` | complete positive-finding pack | `max_daily_loss`, `max_drawdown`, `cooldown_after_loss`, `max_position_size`, `forbidden_assets` | `timestamp`, `symbol`, `side`, `quantity`, `price`, `fees`, `account_id`; realized-P&L behavior through report attribution | Real customer source provenance; live fee schedule; market-data validation; paid-pilot evidence | executive summary, run context, rule coverage, violation table, P&L attribution, operator checklist | Public-like approved sample; P&L wording needs operator caveat because affected P&L can be `0` when flagged rows are not realized-loss rows. |
| `risk_audit_case_001` | complete positive-finding pack | `max_daily_loss`, `cooldown_after_loss`, `forbidden_assets`, `max_position_size` | `timestamp`, `symbol`, `side`, `quantity`, `price`, `fees`, `account_id`; non-zero violating P&L attribution | Real customer source provenance; drawdown; leverage; live fee schedule; paid-pilot evidence | executive summary, run context, rule coverage, violation table with non-zero P&L impact, P&L attribution, operator checklist | Synthetic broker/export-like pack; useful for deterministic rule and attribution coverage only. |
| `synthetic_limit_leverage_001` | complete limitation pack | unsupported `max_leverage`; non-breaching `max_position_size` | `timestamp`, `symbol`, `side`, `quantity`, `price`, `fees`, `account_id` | `leverage`; margin mode; collateral/equity context; real customer source provenance | executive summary, run context, limitation register, P&L attribution, operator checklist | Intended limitation case; the report must refuse to infer leverage from unsupported fields. |
| `synthetic_schema_reject_missing_price_001` | rejected schema pack | schema gate before `max_position_size` evaluation | none until schema is fixed; malformed input intentionally omits `price` | `price`; runnable normalized trades; report artifacts | safe `run_status.json` rejection only; no report, no violation table, no packet | Intended rejection case; proves missing canonical fields block report generation before partial claims are emitted. |
| `real_open_dex_swaps_001` | complete real-open-data rehearsal | `max_position_size`; unsupported `max_leverage` register | `timestamp`, `symbol`, `side`, `quantity`, `price`, schema-placeholder `fees`, safe pair-scope `account_id` | Trader account ledger, user identity, written private rules, gas/LP/all-in fees, leverage, margin, balances, verified realized P&L, intent | executive summary, violation table, P&L attribution, limitation register, reviewed caveat header | Real Uniswap V2 pair-level market-flow data; useful for real public extraction rehearsal only, not private/paid/customer evidence. |
| `real_open_dex_contract_sequence_001` | complete real-open-data no-breach/control rehearsal | non-breaching `max_position_size`; unsupported `max_leverage` register | `timestamp`, `symbol`, `side`, `quantity`, `price`, schema-placeholder `fees`, safe contract-recipient-scope `account_id` | Trader account ledger, user identity, written private rules, gas/LP/all-in fees, leverage, margin, balances, verified realized P&L, intent | executive summary, no-violation section, P&L attribution, limitation register, reviewed caveat header | Real Uniswap V2 swaps filtered to a repeated public contract recipient; useful as contract-scoped rehearsal only, not private/paid/customer evidence. |

## Rule-Type Coverage

| Rule or behavior | Covered by | Coverage status | Gap before private pilot readiness |
|---|---|---|---|
| `max_position_size` | `open_source_sec_form4_001`, `public_sample_001`, `risk_audit_case_001`, `synthetic_limit_leverage_001`, schema gate in `synthetic_schema_reject_missing_price_001`, `real_open_dex_swaps_001`, `real_open_dex_contract_sequence_001` | covered for positive, proxy, non-breach, schema-reject, and real-open-data rehearsal behavior | Add one real private-pilot CSV later to confirm broker export semantics without changing open-source evidence claims. |
| `forbidden_assets` | `open_source_sec_form4_001`, `public_sample_001`, `risk_audit_case_001` | covered for source-row traceability and repeated findings | No additional open-source blocker; keep as artifact coverage only. |
| `max_daily_loss` | `public_sample_001`, `risk_audit_case_001` | covered for positive findings | Add a no-breach daily-loss pack or pilot case so reporting does not only demonstrate failing outcomes. |
| `max_drawdown` | `public_sample_001` | thin coverage | Follow-up case needed: drawdown-only scenario with clear equity curve explanation and no cooldown/asset confounder. |
| `cooldown_after_loss` | `public_sample_001`, `risk_audit_case_001` | covered for positive findings | Follow-up case needed: timezone-boundary cooldown case crossing session start/end. |
| `max_leverage` | `open_source_sec_form4_001`, `synthetic_limit_leverage_001`, `real_open_dex_swaps_001`, `real_open_dex_contract_sequence_001` as unsupported limitation only | accepted limitation | Follow-up case needed before claiming leverage support in demo: fixture with explicit leverage/margin fields or keep leverage as unsupported for paid pilot intake. |
| P&L attribution | `public_sample_001`, `risk_audit_case_001`, `synthetic_limit_leverage_001`, SEC report limitation, `real_open_dex_swaps_001` rehearsal caveat | covered, but not evenly | Follow-up case needed: clear realized-loss row where affected P&L and daily-loss/drawdown wording cannot be confused. Real-open DEX P&L remains rehearsal-only. |
| Fees | required field exists in complete packs; `real_open_dex_swaps_001` uses `0` schema placeholder with caveat | field presence covered, fee-specific rule not covered | Accepted limitation for now; follow-up case needed only if fee-slippage or fee-threshold rules enter the catalog. |
| Session timezone | policies include UTC and Europe/Moscow | basic timezone setting covered | Follow-up case needed: session-boundary case crossing midnight/local session start with explicit expected grouping. |
| Schema rejection | `synthetic_schema_reject_missing_price_001` | covered for missing required `price` | Add future malformed cases only if new intake blockers appear, such as invalid timestamp or non-numeric quantity. |

## Required Field Coverage

| Field | Covered packs | Notes |
|---|---|---|
| `timestamp` | all complete packs; malformed pack still contains it | Timezone-aware rendering appears in reports; session-boundary behavior needs a dedicated follow-up. |
| `symbol` | all packs | Forbidden-asset traceability covered; symbols are synthetic, disclosure-derived, or real-open-data pair labels and not customer evidence. |
| `side` | all complete packs | Basic normalization covered; DEX side is WETH-relative, not trader-intent proof. |
| `quantity` | all complete packs | Position-size and notional checks depend on it. |
| `price` | all complete packs; intentionally absent in `synthetic_schema_reject_missing_price_001` | Missing-price rejection is explicit and blocks report generation. |
| `fees` | all complete packs | Present for canonical compatibility; no fee-specific rule coverage yet. DEX pack uses `0` as unsupported-cost placeholder only. |
| `account_id` | all complete packs | Uses safe demo/synthetic/disclosure/pair-scope labels only; no private account identifiers are committed. |

## Follow-Up Cases And Accepted Limitations

Follow-up cases before broader private-pilot readiness:

1. `future_drawdown_only_001`: synthetic or lawful open-source fixture with
   one drawdown-focused finding, explicit equity curve explanation, and no
   forbidden-asset/cooldown overlap.
2. `future_session_timezone_boundary_001`: fixture with trades crossing local
   session start or midnight to verify daily loss and cooldown grouping.
3. `future_realized_loss_pnl_wording_001`: fixture where affected P&L,
   violating P&L, and daily-loss wording are unambiguous on the same row set.
4. `future_no_breach_control_001`: runnable pack with zero findings and a clear
   report explaining that "no breach" is not a performance endorsement.

Accepted limitations unless a future task explicitly reopens them:

- `max_leverage` remains unsupported without an explicit leverage or margin
  field and must stay visible in report limitations.
- Fee-specific risk rules are not covered by the current rule catalog and
  should not be implied from the presence of a `fees` column.
- Open-source and synthetic packs remain artifact-quality evidence only; they
  do not count as paid-pilot readiness, PMF, customer validation, or evidence
  that traders will pay.
- Real open-data rehearsal packs remain development evidence only; they do not
  count as private, paid-pilot, PMF, customer validation, market-demand, or
  willingness-to-pay evidence.
- Rejected schema packs do not produce reports or Telegram packets; their
  evidence is the safe rejection status.

## Coverage Decision

The current bank is strong enough for Phase 24 report-quality comparison
because it includes positive, limitation, and rejection examples across
multiple data shapes. It is not strong enough to claim private-pilot readiness
without the follow-up cases above or an accepted scope statement that excludes
drawdown-only, leverage-supported, fee-specific, and session-boundary claims.
