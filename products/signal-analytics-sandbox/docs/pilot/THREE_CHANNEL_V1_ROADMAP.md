# Three-Channel V1 Roadmap

Date: 2026-05-19
Status: planned after `SAS-ER-004`

## Goal

Turn the internal V0 metric comparison into a reviewed V1 channel utility
report that can be considered for customer-facing use.

V0 proved the end-to-end path:

public post -> normalized claim -> open/public market data window -> metric ->
channel comparison.

V1 must make that reliable enough to explain, defend, and potentially sell.

## Phase 27 Task Flow

| Task | Purpose | Output |
|---|---|---|
| `SAS-V1-001` | Approve evaluator types, claim types, proxies, providers, horizons, and exclusions per channel. | `three_channel_V1_APPROVAL_MATRIX.md` |
| `SAS-V1-002` | Review V0 false positives/false negatives and define extractor calibration rules. | `three_channel_V1_EXTRACTION_REVIEW.md`, `three_channel_V1_EXTRACTOR_CALIBRATION.md` |
| `SAS-V1-003` | Build reusable structured claim extractor V1. | `src/signal_sandbox/claims/`, extractor tests |
| `SAS-V1-004` | Add level-aware outcome engine for entry/stop/target/timeout/RR. | `claims/outcomes.py`, outcome tests |
| `SAS-V1-005` | Add reviewed transcript/OCR/image claim extraction into the same claim surface. | media inventory and multimodal claim tests |
| `SAS-V1-006` | Expand provider/proxy mapping without bulk market-history storage. | provider config and window-planning tests |
| `SAS-V1-007` | Recompute V1 metrics and channel scorecard. | `three_channel_V1_METRIC_RESULTS.json`, `three_channel_V1_SCORECARD.md` |
| `SAS-V1-008` | Produce customer-facing candidate report and external gate. | V1 report and external-ready gate |
| `SAS-V1-009` | Run mandatory phase boundary deep review. | `PHASE27_REVIEW.md` |

## Required Improvements Over V0

1. **Human/operator review of extraction quality.**
   V0 hit rates are not customer-facing until false positives and false
   negatives are sampled and documented.

2. **Structured fields beyond direction.**
   V1 must extract entry, stop/invalidation, target, timeout, horizon, RR, and
   ambiguity blockers when evidence supports them.

3. **Level-aware outcomes.**
   Direction-only 7d returns stay available, but explicit trade setups need
   entry-fill, stop/target/timeout, return %, MFE, MAE, and RR.

4. **Multimodal evidence.**
   Text, reviewed transcripts, and reviewed OCR/chart evidence must normalize
   into the same claim surface. Unreviewed media remains internal-only.

5. **Provider/proxy expansion.**
   V1 must explicitly approve or reject provider paths for crypto, MOEX, US
   equities/funds, futures/proxies, and benchmarks. Unsupported assets must be
   exclusions, not wins/losses.

6. **Customer-facing gate.**
   A report can be external only if the gate confirms evidence integrity,
   reviewed media posture, metric reproducibility, and no overclaim risk.

## Non-Goals

- No private Telegram scraping.
- No bulk market-history database.
- No paid X/Twitter dependency before Telegram/public-source validation.
- No future-profit claims.
- No investment advice.
- No unreviewed transcript/OCR/chart claims in customer-facing metrics.

## Success Criteria

V1 is successful when the project has:

- a reviewed extraction calibration pack;
- a reusable structured claim extractor;
- deterministic level-aware outcome metrics;
- provider/proxy coverage with explicit gaps;
- a three-channel V1 scorecard;
- a report draft with confirmed and contradicted examples;
- an external-ready gate that either approves, rejects, or keeps the report
  internal-only with concrete blockers.
