# Counterexamples And Weak Evidence Register - bablos79

Date: 2026-05-15
Status: active_phase24_balance_register

This register preserves weak, blocked, unresolved, ambiguous, non-measurable,
and unsupported-media examples before any author-strength conclusion is drafted.
It is required input for later author capability reporting.

## Summary

| Field | Count |
|---|---:|
| confirmed outcome examples | 0 |
| contradicted outcome examples | 0 |
| unresolved examples listed | 7 |
| ambiguous/weak examples listed | 5 |
| non-measurable examples listed | 4 |
| unsupported-media examples listed | 4 |
| computed outcome metrics available | 0 |

No contradicted computed outcomes exist yet because
`docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.md` records 0 computed metrics, 0
approved proxies, and 0 market-data snapshots. This is not positive evidence
for the author; it means the current corpus cannot yet support confirmed or
contradicted performance examples.

## Contradicted Examples

None available.

Reason: no claim has an approved proxy, market-data snapshot, horizon, and
outcome method. Later phases must add contradicted examples here if
deterministic outcome evaluation finds them.

## Unresolved Examples

| claim_id | source ref | category | why unresolved | required next step |
|---|---|---|---|---|
| `claim_text_bablos79_10442` | `https://t.me/bablos79/10442` | `directional_bias` | `X5` ticker candidate exists, but direction, horizon, entry, stop, and target are missing. | Human review must decide whether this is only context or a measurable bias. |
| `claim_text_bablos79_10443` | `https://t.me/bablos79/10443` | `directional_bias` | `VTBR` ticker candidate exists, but direction and outcome horizon are missing. | Human review must supply or reject direction/horizon before proxy mapping. |
| `claim_text_bablos79_10450` | `https://t.me/bablos79/10450` | `directional_bias` | `MAGN` and negative short language exist, but current entry/stop/target and horizon are absent. | Link original setup or keep as historical context. |
| `claim_text_bablos79_10464` | `https://t.me/bablos79/10464` | `level_timing_call` | `X5` close/re-entry language lacks original setup and evaluable levels. | Link original setup or mark as management-only context. |
| `claim_text_bablos79_10499` | `https://t.me/bablos79/10499` | `level_timing_call` | `SFIN` close/exit language lacks original entry, stop, target, and horizon. | Link source setup before any outcome evaluation. |
| `claim_text_bablos79_10500` | `https://t.me/bablos79/10500` | `level_timing_call` | `CHMF` partial fixation and moved stop lack original setup fields. | Link original setup or keep as non-evaluable management context. |
| `claim_text_bablos79_10501` | `https://t.me/bablos79/10501` | `level_timing_call` | `MAGN` partial close and moved stop lack original setup fields. | Link original setup or keep as non-evaluable management context. |

## Ambiguous Or Weak Examples

| claim_id | source ref | category | weak/ambiguous reason | report use |
|---|---|---|---|---|
| `claim_text_bablos79_10459` | `https://t.me/bablos79/10459` | `directional_bias` | Author says he will not short AMD yet; negative/deferral pattern exists but no current trade or horizon exists. | Weak/blocked example, not performance evidence. |
| `claim_text_bablos79_10470` | `https://t.me/bablos79/10470` | `watchlist` | Currency-market watch language says signs may appear later; no explicit pair/proxy or current call. | Watchlist/context example only. |
| `claim_text_bablos79_10504` | `https://t.me/bablos79/10504` | `directional_bias` | Short-management language says picture is unchanged, but asset/proxy and horizon are absent. | Weak directional context only. |
| `claim_transcript_bablos79_10476_claim2` | `https://t.me/bablos79/10476` | `directional_bias` | Broad Moscow-exchange downside thesis has no approved proxy and transcript is LLM-reviewed internal only. | Internal-only weak media-backed example. |
| `claim_transcript_bablos79_10478_claim1` | `https://t.me/bablos79/10478` | `event_risk` | Event-risk thesis has no approved proxy/event window and transcript is LLM-reviewed internal only. | Internal-only weak media-backed example. |

## Non-Measurable Examples

| claim_id | source ref | category | non-measurable reason |
|---|---|---|---|
| `claim_text_bablos79_10465` | `https://t.me/bablos79/10465` | `macro_context` | Macro/geopolitical context has no approved benchmark, direction, horizon, or outcome method. |
| `claim_transcript_bablos79_10476_claim1` | `https://t.me/bablos79/10476` | `macro_context` | Broad geopolitical thesis has no explicit asset/proxy or measurable outcome and is LLM-reviewed internal only. |
| `claim_transcript_bablos79_10476_claim2` | `https://t.me/bablos79/10476` | `directional_bias` | Broad market downside claim lacks explicit asset/trade setup and approved proxy. |
| `claim_transcript_bablos79_10478_claim1` | `https://t.me/bablos79/10478` | `event_risk` | Russian-exchange event-risk claim lacks approved proxy and deterministic event window. |

## Unsupported-Media Examples

| blocked id | source ref | unsupported reason | required next step |
|---|---|---|---|
| `blocked_image_channel_level_screenshot` | `docs/pilot/bablos79_IMAGE_REVIEW_QUEUE.md` | No exact public source URL, capture ID, source-document ID, or checksumable media. | Provide source-linked public image artifact. |
| `blocked_chart_channel_level_screenshot` | `docs/pilot/bablos79_IMAGE_REVIEW_QUEUE.md` | No exact chart source linkage; chart interpretation remains manual-review-only. | Provide source-linked chart artifact and manual review. |
| `blocked_gap_pre_seed_window_images` | `docs/pilot/bablos79_CORPUS_GAP_REGISTER.md` | No source rows exist for pre-seed locked-window media review. | Capture/register source rows or mark unavailable. |
| `blocked_gap_post_seed_window_images` | `docs/pilot/bablos79_CORPUS_GAP_REGISTER.md` | No source rows exist for post-seed locked-window media review. | Capture/register source rows or mark unavailable. |

## Report Gate

Before any positive author-strength conclusion, the report gate must check this
register and explicitly state:

- whether confirmed and contradicted deterministic examples exist;
- how many unresolved, weak, non-measurable, and unsupported examples remain;
- whether the corpus is sufficient for an author-strength conclusion;
- whether media-backed examples are human/operator accepted for external use;
- why the conclusion is balanced rather than cherry-picked.

Current gate decision: no positive author-strength conclusion is allowed. The
available evidence is useful for internal corpus characterization only.
