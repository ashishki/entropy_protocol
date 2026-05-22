# Three-Channel Buyer Demo Pack

Date: 2026-05-19
Status: internal_only_not_customer_facing
Gate: `approve_internal_only`

## Boundary

This pack is for internal buyer-discovery preparation only.

Guardrail: must not be sent as a customer-facing report, sales deck, public
claim, paid sample, channel ordering, or investment recommendation unless a
later external-ready gate explicitly approves that delivery.

## Included Artifacts

| Artifact | Path | Use |
|---|---|---|
| V2 metrics | `docs/pilot/three_channel_V2_METRIC_RESULTS.json` | Internal metric baseline with media exclusions. |
| V2 scorecard | `docs/pilot/three_channel_V2_SCORECARD.md` | Diagnostic channel utility dimensions. |
| Robustness appendix | `docs/pilot/three_channel_V2_ROBUSTNESS_APPENDIX.md` | Horizon/provider/sample-size limitations. |
| Media inventory | `docs/pilot/three_channel_V2_MEDIA_INVENTORY.md` | Public media refs, checksums, blockers, and review status. |
| Transcript workflow | `docs/pilot/three_channel_TRANSCRIPT_REVIEW.md` | Human/operator transcript decision workflow. |
| External gate | `docs/pilot/three_channel_V1_EXTERNAL_READY_GATE.md` | Current external delivery decision. |

## Methodology Summary

- Public/operator-authorized source rows only.
- Claims are normalized into reviewed structured claim rows.
- Unsupported provider/proxy rows are exclusions, not wins or losses.
- Market outcomes use deterministic provider snapshots and explicit horizons.
- Media-backed claims enter metrics only after human/operator review and
  provenance checks.
- Current V2 metrics include zero reviewed media claims and exclude all
  unreviewed/unlinked media rows.

## What Can Be Shown Internally

- The system can compare three public channels on coverage, clarity,
  extraction quality, outcome quality, risk quality, and limitations.
- The system can show how every supported metric should link to evidence,
  provider, snapshot, and review decision records.
- The system can show why current results are not externally robust yet.

## What Must Not Be Claimed

- Do not claim any channel is the best, top, or recommended channel.
- Do not claim the system predicts future profit.
- Do not present the current report as investment advice.
- Do not include unreviewed transcript, OCR, image, or chart claims in
  customer-facing material.
- Do not sell this pack as an external report while the gate remains
  `approve_internal_only`.

## Buyer Discovery Talk Track

1. Start with the pain: public trading channels produce many claims, but most
   are ambiguous, unsupported, or hard to verify.
2. Show the method: capture public evidence, normalize claims, review edge
   cases, fetch market data only when needed, and report exclusions honestly.
3. Show the current result: 170 V2 evaluable text claims, 93 confirmed hits,
   77 contradicted misses, and 0 reviewed media claims included.
4. Show the risk controls: unsupported assets, unreviewed media, missing
   benchmarks, missing setup levels, and provider gaps are blocked.
5. Ask discovery questions: which sources matter, what proof threshold is
   useful, what compliance constraints apply, and what format would be worth
   paying for after external gate approval.

## Open Limitations

- External delivery is not approved.
- Review coverage is incomplete.
- Provider gaps remain material.
- Setup/RR coverage is sparse.
- Benchmark-relative rows are not yet present in the current V2 dataset.
- Media claims are inventoried but not accepted for customer-facing use.

## Gate Status

Decision: `approve_internal_only`.

Required before external use:

- durable operator decisions;
- stronger review coverage;
- media/transcript/OCR acceptance where used;
- provider and benchmark robustness;
- customer-safe wording pass;
- rerun external-ready gate with explicit approval.
