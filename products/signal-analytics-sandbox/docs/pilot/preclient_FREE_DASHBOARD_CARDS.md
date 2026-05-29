# Pre-Client Free Dashboard Cards

Date: 2026-05-23T14:45:00Z
Status: `internal_dashboard_card_dataset_draft`

## Boundary

- Internal dashboard prototype only.
- No public display is approved by this artifact.
- Media and RR claims remain blocked until review gates accept them.

## Compact Cards

| channel | claims | text outcome | media | RR/setup | gate |
|---|---:|---|---|---|---|
| `bablos79` | 14 | Internal V1: 9 confirmed / 5 contradicted over 14 evaluable text claims; avg 7d directional return 0.742848%. | 196 public media refs; image=94, video=34, voice=68; model-reviewed packet candidates 1; all blocked. | One internal RR-ready draft exists, but it still needs operator acceptance and market recompute. | `internal_only_not_dashboard_safe` |
| `nemphiscrypts` | 49 | Internal V1: 28 confirmed / 21 contradicted over 49 evaluable text claims; avg 7d directional return 0.434858%. | 63 public media refs; image=63; model-reviewed packet candidates 1; all blocked. | RR is blocked for the accepted media candidate because target and position fields are missing. | `internal_only_not_dashboard_safe` |
| `pifagortrade` | 107 | Internal V1: 56 confirmed / 51 contradicted over 107 evaluable text claims; avg 7d directional return -0.153127%. | 36 public media refs; image=28, video=6, voice=2; model-reviewed packet candidates 7; all blocked. | No dashboard-safe RR yet; candidates need operator classification and recompute. | `internal_only_not_dashboard_safe` |

## Channel Notes

### bablos79

What it is: Public Telegram market commentary with MOEX equity coverage plus some crypto references.

Strengths:
- Largest public text corpus in the current V1 metric artifact.
- Measurable text claims cover both MOEX equities and one crypto proxy.
- One model-reviewed media setup has entry, stop, target, and internal draft RR fields.

Weaknesses:
- Media evidence is model-reviewed only and remains blocked pending operator review.
- Many media rows are context, non-market, rejected noise, or video/manual blockers.
- The measurable text edge is modest and not approved for external display.

### nemphiscrypts

What it is: Public Telegram crypto commentary with chart-driven directional ideas.

Strengths:
- V1 text metrics have a larger crypto sample than bablos79.
- Media review found one model-reviewed setup candidate with entry and stop fields.
- Coverage is mostly crypto, which simplifies provider routing through Binance proxies.

Weaknesses:
- The model-reviewed setup lacks targets and position sizing.
- All media-derived claims are blocked pending operator review.
- Provider gaps and unsupported assets remain material exclusions.

### pifagortrade

What it is: Public Telegram trading channel with crypto charts, setup language, and post-trade screenshots.

Strengths:
- Largest V1 evaluable claim count in the current metric artifact.
- Media review found the highest count of arbiter-accepted internal candidates.
- Several media rows contain explicit setup, risk, position, or post-factum evidence.

Weaknesses:
- Several accepted media candidates are post-factum and cannot be treated as forward-looking calls.
- RR is mostly blocked by missing or ambiguous stop, target, direction, or asset fields.
- Average directional return in V1 is slightly negative despite a near-even hit split.
