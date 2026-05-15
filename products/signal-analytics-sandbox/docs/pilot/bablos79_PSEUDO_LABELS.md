# bablos79 Pseudo-Labels - Draft Only

Date: 2026-05-08
Source: `bablos79` public Telegram captures
Artifact: `workspace/extraction/bablos79_pseudo_labels.jsonl`

## Boundary

These rows are offline pseudo-labels for reviewer and validator work only. They are not approved signal records, must not be written to the ledger, and must not be used for customer-facing performance claims. Every candidate field remains draft-only until deterministic validation and human review approve it.

## Schema

Each JSONL row includes `capture_id`, `suggested_status`, `candidate_fields`, `missing_fields`, `evidence_spans`, `confidence`, `uncertainty_reason`, `lexicon_terms_found`, and `draft_only=true`. Non-empty candidate fields include field-level evidence spans intended for deterministic checking in the next task.

## Summary

- Captures labeled: 60
- Draft-only rows: 60
- `not_a_signal`: 50
- `insufficient_fields`: 7
- `needs_review`: 3
- Rows with candidate evidence spans: 17
- Rows with uncertainty or review markers: 18
- Approved ledger rows created: 0

## Uncertainty / Needs-Review Queue

| capture_id | suggested_status | confidence | reason |
|------------|------------------|------------|--------|
| `bablos79-10442` | `insufficient_fields` | 0.39 | Ticker is present, but phrase is accumulation/commentary without an actionable entry, stop, or target. |
| `bablos79-10443` | `insufficient_fields` | 0.36 | VTBR risk commentary is present, but no trade setup fields are stated. |
| `bablos79-10446` | `not_a_signal` | 0.62 | Ticker appears in a liquidity/reserve news comment, not a trade instruction. |
| `bablos79-10450` | `insufficient_fields` | 0.49 | Historical short mention exists, but the current post lacks a precise entry, stop, and target. |
| `bablos79-10453` | `not_a_signal` | 0.60 | Ticker-only topic marker; no trade intent or levels. |
| `bablos79-10458` | `not_a_signal` | 0.55 | Ticker appears with an implied follow-up/comment, but no standalone trade fields. |
| `bablos79-10459` | `needs_review` | 0.42 | Author explicitly says he will not short yet; this is a useful negative/deferral pattern, not an actionable signal. |
| `bablos79-10464` | `insufficient_fields` | 0.52 | Close/re-entry language exists, but the original setup and evaluable levels are absent. |
| `bablos79-10467` | `not_a_signal` | 0.66 | Sarcastic investment commentary; no author trade setup. |
| `bablos79-10470` | `needs_review` | 0.34 | Currency-market watch language says signs may appear later; possible watchlist pattern, not a current trade. |
| `bablos79-10489` | `not_a_signal` | 0.58 | Ticker plus aesthetic/commentary phrase; no trade intent or levels. |
| `bablos79-10490` | `not_a_signal` | 0.63 | Comment about investors returning to profit, not an author trade setup. |
| `bablos79-10492` | `not_a_signal` | 0.61 | Mentions another person buying SBER humorously; not the author issuing a signal. |
| `bablos79-10497` | `not_a_signal` | 0.61 | Criticism of another promoter around MAGN; no author setup. |
| `bablos79-10499` | `insufficient_fields` | 0.55 | Close/exit language exists, but no original entry/stop/target is provided in this post. |
| `bablos79-10500` | `insufficient_fields` | 0.58 | Partial fixation and moved stop are trade-management language, but original setup levels are missing. |
| `bablos79-10501` | `insufficient_fields` | 0.57 | Partial close and moved stop are trade-management language, but no entry/target/stop values are stated. |
| `bablos79-10504` | `needs_review` | 0.41 | Mentions closing part of shorts without symbol; may link to prior posts, so needs human/context review. |

## Pseudo-Label Rows

| capture_id | status | assets | direction | entry | stop | target | missing_fields | confidence | evidence_spans | uncertainty_reason |
|------------|--------|--------|-----------|-------|------|--------|----------------|------------|----------------|--------------------|
| `bablos79-10442` | `insufficient_fields` | X5 | unknown | - | - | - | direction, entry, stop, target | 0.39 | asset_candidates=#X5 | Ticker is present, but phrase is accumulation/commentary without an actionable entry, stop, or target. |
| `bablos79-10443` | `insufficient_fields` | VTBR | unknown | - | - | - | direction, entry, stop, target | 0.36 | asset_candidates=#VTBR | VTBR risk commentary is present, but no trade setup fields are stated. |
| `bablos79-10444` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10445` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10446` | `not_a_signal` | VTBR | unknown | - | - | - | - | 0.62 | asset_candidates=#VTBR | Ticker appears in a liquidity/reserve news comment, not a trade instruction. |
| `bablos79-10447` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10448` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10449` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10450` | `insufficient_fields` | MAGN | short | - | - | - | entry, stop, target | 0.49 | asset_candidates=#MAGN; direction_candidate=шорт; direction_candidate=шортили | Historical short mention exists, but the current post lacks a precise entry, stop, and target. |
| `bablos79-10451` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10452` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10453` | `not_a_signal` | VKCO | unknown | - | - | - | - | 0.60 | asset_candidates=#VKCO | Ticker-only topic marker; no trade intent or levels. |
| `bablos79-10454` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10455` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10456` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10457` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10458` | `not_a_signal` | X5 | unknown | - | - | - | - | 0.55 | asset_candidates=#X5 | Ticker appears with an implied follow-up/comment, but no standalone trade fields. |
| `bablos79-10459` | `needs_review` | AMD | short | - | - | - | entry, stop, target | 0.42 | asset_candidates=#AMD; direction_candidate=шорт; direction_candidate=шортить | Author explicitly says he will not short yet; this is a useful negative/deferral pattern, not an actionable signal. |
| `bablos79-10460` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10461` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10463` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10464` | `insufficient_fields` | X5 | close_or_reduce | - | - | - | entry, stop, target | 0.52 | asset_candidates=#X5; direction_candidate=закрыл | Close/re-entry language exists, but the original setup and evaluable levels are absent. |
| `bablos79-10465` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10466` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10467` | `not_a_signal` | MAGN | unknown | - | - | - | - | 0.66 | asset_candidates=#MAGN | Sarcastic investment commentary; no author trade setup. |
| `bablos79-10468` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10469` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10470` | `needs_review` | - | unknown | - | - | - | asset_symbol, entry, stop, target | 0.34 | - | Currency-market watch language says signs may appear later; possible watchlist pattern, not a current trade. |
| `bablos79-10471` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10472` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10475` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10476` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10477` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10478` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10479` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10482` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10483` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10485` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10486` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10487` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10488` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10489` | `not_a_signal` | GAZP | unknown | - | - | - | - | 0.58 | asset_candidates=#GAZP | Ticker plus aesthetic/commentary phrase; no trade intent or levels. |
| `bablos79-10490` | `not_a_signal` | GAZP | unknown | - | - | - | - | 0.63 | asset_candidates=#GAZP | Comment about investors returning to profit, not an author trade setup. |
| `bablos79-10491` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10492` | `not_a_signal` | SBER | unknown | - | - | - | - | 0.61 | asset_candidates=#SBER | Mentions another person buying SBER humorously; not the author issuing a signal. |
| `bablos79-10493` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10495` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10496` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10497` | `not_a_signal` | MAGN | unknown | - | - | - | - | 0.61 | asset_candidates=#MAGN | Criticism of another promoter around MAGN; no author setup. |
| `bablos79-10498` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10499` | `insufficient_fields` | SFIN | close_or_reduce | - | - | - | entry, stop, target | 0.55 | asset_candidates=#SFIN; direction_candidate=закрыл | Close/exit language exists, but no original entry/stop/target is provided in this post. |
| `bablos79-10500` | `insufficient_fields` | CHMF | close_or_reduce | - | - | - | entry, stop, target | 0.58 | asset_candidates=#CHMF; direction_candidate=Зафиксировал; direction_candidate=Стоп перенес | Partial fixation and moved stop are trade-management language, but original setup levels are missing. |
| `bablos79-10501` | `insufficient_fields` | MAGN | close_or_reduce | - | - | - | entry, stop, target | 0.57 | asset_candidates=#MAGN; direction_candidate=закрыл; direction_candidate=Часть закрыл | Partial close and moved stop are trade-management language, but no entry/target/stop values are stated. |
| `bablos79-10502` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10503` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10504` | `needs_review` | - | close_or_reduce | - | - | - | asset_symbol, entry, stop, target | 0.41 | direction_candidate=закрыл; direction_candidate=закрыл часть | Mentions closing part of shorts without symbol; may link to prior posts, so needs human/context review. |
| `bablos79-10505` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10506` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10507` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |
| `bablos79-10508` | `not_a_signal` | - | unknown | - | - | - | - | 0.72 | - | - |

## Next Validation Work

- Verify every `evidence_spans[].text` value appears in the raw capture text.
- Reject any candidate field whose numeric value, ticker, or direction lacks a matching span.
- Keep `review_candidate`, `needs_review`, and uncertain rows out of the approved ledger until human review supplies `reviewer_id`.
