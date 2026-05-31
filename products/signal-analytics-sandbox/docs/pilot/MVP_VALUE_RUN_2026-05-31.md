# MVP Value Run - 2026-05-31

Status: `internal_mvp_value_assessment`

Question: is the current MVP valuable already?

## Verdict

The MVP is valuable as an internal diligence and evidence-quality product. It is
not ready as a customer-facing paid metrics product.

The current best route is a concierge source-diligence validation: use the
system to show how a source is audited, what evidence is usable, what is
blocked, and why. Do not sell public dashboard metrics, paid signal rankings,
or performance claims yet.

## What Was Run

This run combines the current pre-client and client-ready artifacts:

- `docs/pilot/preclient_FREE_DASHBOARD_CARDS.json`
- `docs/pilot/preclient_ARTIFACT_SAFETY_GATE.json`
- `docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.json`
- `docs/pilot/clientready_ACCEPTED_OUTCOMES.json`
- `docs/pilot/clientready_DISCOVERY_GATE.json`
- `docs/pilot/clientready_AUTO_VALIDATION_EVAL.json`

## Evidence Snapshot

| Area | Result | MVP meaning |
|---|---:|---|
| Channels reviewed | 3 | Enough for a narrow internal diligence demo. |
| V1 text-evaluable claims | 170 | Enough to compare sources internally, not enough for external promises. |
| Confirmed / contradicted text outcomes | 93 / 77 | Shows mixed but measurable signal quality. |
| Media candidates evaluated | 9 | Useful proof path for chart/setup validation. |
| Auto-accepted media rows | 0 | No media row can become a customer-facing metric. |
| Auto-rejected media rows | 4 | Automation catches post-factum risk. |
| Needs-human media rows | 5 | Operator/context bottleneck remains real. |
| Customer-facing rows | 0 | Paid/public metrics remain blocked. |
| Ready for discovery | false | Current artifact stack is still internal-only. |

## Channel Readout

| Channel | V1 claims | Confirmed / contradicted | Avg 7d return | Current read |
|---|---:|---:|---:|---|
| `bablos79` | 14 | 9 / 5 | 0.742848% | Modest positive internal text signal; sample and provider/operator gates are too weak for customer claims. |
| `nemphiscrypts` | 49 | 28 / 21 | 0.434858% | Cleaner crypto routing and a positive internal text read; media setup lacks target/position fields. |
| `pifagortrade` | 107 | 56 / 51 | -0.153127% | Largest sample and richest media candidates; near-even performance and post-factum media risk limit customer value. |

## Main Insights

1. The product already prevents bad customer-facing claims. That is real value:
   it rejected post-factum rows and routed ambiguous chart/setup rows to human
   review instead of producing false wins.
2. The strongest wedge is not "we found profitable signal channels." The wedge
   is "we can audit public signal sources and show what can and cannot be
   trusted."
3. The dashboard/product surface is ahead of the evidence gate. More UI will
   not fix the core blocker: 0 operator-accepted media claims and 0 recomputed
   accepted outcomes.
4. The internal text metrics are useful for analysis, but they are
   direction-only and mixed. They should support diligence questions, not public
   leaderboards.
5. Buyer value is still an assumption. The next proof is whether buyers already
   have a painful source-diligence workflow and would pay for a bounded report.

## Startup Pressure Test

| Dimension | Score | Read |
|---|---:|---|
| Pain intensity | 3 / 5 | The problem is plausible, but buyer pain is not yet proven. |
| Buyer clarity | 2 / 5 | Likely buyers exist, but ICP and budget owner are still loose. |
| Urgency | 2 / 5 | No evidence yet that this is urgent enough to buy now. |
| Differentiation | 4 / 5 | Conservative evidence gates and auditability are a real technical edge. |
| Speed to validate | 4 / 5 | A concierge diligence report can test demand quickly. |
| Founder/project advantage | 3 / 5 | Strong pipeline and artifacts; buyer access remains unknown. |

## Go / No-Go

Go:

- Continue building the internal diligence workflow.
- Run concierge discovery around source diligence.
- Try to get one operator-accepted media row recomputed end to end.

No-go:

- Do not launch a public dashboard.
- Do not sell paid performance metrics.
- Do not present media/chart rows as validated predictive calls.
- Do not claim "best channels", "winning signals", or future-profit value.

## Next Experiments

1. Five buyer discovery calls around source diligence pain.
   Success: at least 2 buyers describe an existing manual or paid workflow for
   vetting sources and ask to see a bounded diligence report.
2. One operator-accepted media row recomputed end to end.
   Success: source time, asset/proxy, direction, entry, stop, target, horizon,
   recompute provenance, and policy gate all line up.
3. One concierge internal diligence report for a single source.
   Success: a buyer says it would affect source selection, risk review, or paid
   vendor diligence.

## Kill Criteria

- No buyer confirms a painful source-diligence workflow.
- Buyers consider public-source evidence insufficient for any real decision.
- The team cannot produce at least one operator-accepted and recomputed media
  row.
- Buyers only want forward-looking trade recommendations, which this product
  must not provide.
