# Phase 36 Scope - pifagortrade Corpus Completion

Date: 2026-05-22
Status: `scope_ready_completion_required`
Channel: `pifagortrade`

This scope applies the same Phase 36 truth and impact framework used for
`bablos79`: signal performance, trend sense, insight depth, methodology, risk
management, practical usefulness, creativity/differentiation, and evidence
confidence. It is a completion plan, not an external-ready approval.
risk management is reviewed as its own non-PnL impact dimension.
evidence confidence is reviewed as its own non-PnL impact dimension.

## Current Evidence Snapshot

| Area | Current state |
| --- | --- |
| Public text rows | 492 |
| Market candidates | 425 |
| Explicit setup candidates | 43 |
| Position/trade-language candidates | 60 |
| Directional-bias candidates | 271 |
| V1 evaluable claims | 107 |
| V1 confirmed / contradicted | 56 / 51 |
| V1 hit rate | 52.336449% |
| Average directional return | -0.153127% |
| Provider coverage | Binance only: BTC, DOT, ETH, TON |
| Media state | 0 acquired audio refs, 0 transcript refs, 0 reviewed source-linked chart/OCR refs |
| External state | internal-only until completion, review, and gate rerun |

## Missing Periods And IDs

Phase 36 has not yet audited `pifagortrade` message-ID continuity or full period
coverage. Missing periods/IDs are therefore recorded as
`not_audited_in_phase36_yet`, not as clean coverage.

Required next steps:

1. Build a source coverage manifest from public Telegram `/s/pifagortrade`
   captures.
2. Record first/last timestamp, message-ID ranges, deleted/unavailable rows,
   media-only rows, and capture gaps.
3. Separate unavailable rows from author evidence; missing rows are not wins,
   losses, or weak/strong evidence.

## Media Completion

No current V1 workspace media is acquired for this channel. Completion requires:

- source-linked public audio/image/chart candidates, if present;
- checksumable local file or authorized external reference;
- transcript/OCR draft artifacts only after source linkage;
- human/operator acceptance before customer-facing media claims;
- chart interpretation as manual-review-only.

## Claim And Truth Mapping

Use the same truth layers as `CHANNEL_IMPACT_FRAMEWORK.md`:

- author-statement truth: what the channel actually said;
- interpretation truth: how the system normalized the statement;
- market-outcome truth: what public market data can verify;
- product-conclusion truth: what can safely be shown in dashboard/deep report.

V1 metrics are useful but not sufficient for Phase 36 external comparison. The
scope must review false negatives, needs-context rows, unsupported assets,
mixed-direction rows, custom trap-line/setup language, and provider gaps before
cross-channel scoring.

## Stop Conditions

- Do not approve external delivery from the current scope alone.
- Do not count provider gaps or unsupported proxies as losses.
- Do not include media/OCR/chart claims until source-linked and accepted.
- Do not rank channels until all three have equivalent completion artifacts.

## Next Artifacts

- media linkage queue for `pifagortrade`;
- transcript/OCR acceptance artifacts only if media exists;
- Phase 36 claim ledger and outcome recompute;
- channel gate using the same no-advice, no-ranking boundary.
