# Client-Ready Redacted Buyer Demo Subset

Date: 2026-05-29
Status: `clientready_redacted_buyer_demo_subset`
Gate decision: `blocked_internal_only`
Showable now: `false`

## Boundary

- This subset uses compact channel fields, visible caveats, and source-linked
  examples only.
- It does not expose the full evidence appendix, raw media, workspace paths, or
  unaccepted media metrics.
- No operator-accepted media rows exist yet.
- No market outcomes were recomputed for client-ready use.
- Post-factum rows are excluded from predictive-call metrics.

## Compact Fields

| channel | window | text claims | media refs | model-reviewed candidates | accepted | recomputed | gate |
|---|---|---:|---:|---:|---:|---:|---|
| `bablos79` | `2026-03-22..2026-05-22` | 14 | 196 | 1 | 0 | 0 | `blocked_internal_only` |
| `nemphiscrypts` | `2026-03-22..2026-05-22` | 49 | 63 | 1 | 0 | 0 | `blocked_internal_only` |
| `pifagortrade` | `2026-03-22..2026-05-22` | 107 | 36 | 7 | 0 | 0 | `blocked_internal_only` |

## Source-Linked Examples

These examples are included only to show traceability. They are not accepted
outcomes and they do not create demo-safe metrics.

| channel | source | redacted note |
|---|---|---|
| `bablos79` | [source](https://t.me/bablos79/10450) | Setup-like media candidate; still needs operator acceptance and provider/proxy approval. |
| `nemphiscrypts` | [source](https://t.me/nemphiscrypts/3958) | Incomplete setup candidate; missing fields remain unresolved. |
| `pifagortrade` | [source](https://t.me/pifagortrade/3234) | Setup-like media candidate; not counted as an accepted outcome. |

## Visible Caveats

- Internal diligence subset only.
- No operator-accepted media rows exist yet.
- No market outcomes were recomputed for client-ready use.
- Provider gaps and missing fields remain exclusions.
- Post-factum rows remain outside predictive-call metrics.

## Showability

`showable_now: false`

Reason: current accepted outcomes contain 0 accepted rows, 0 recomputed rows,
and 0 buyer-demo-safe rows.
