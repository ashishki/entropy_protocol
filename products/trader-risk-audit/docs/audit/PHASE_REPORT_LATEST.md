# Phase 32 Report - Dune Public Wallet Rehearsal

## What Was Built

Phase 32 added `demo/dune_public_wallet_dex_001/`, a real public Dune
`dex.trades` case pack scoped to one public Ethereum `tx_from` submitter.

It includes:

- source metadata and SQL provenance;
- canonical `trades.csv`;
- a local risk policy;
- generated and reviewed reports;
- manifest, violations, attribution, Telegram packet, and reproducibility
  status;
- manual review and error register.

## Validation

- `case-bank validate --case-dir demo/dune_public_wallet_dex_001` -> passed.
- Reproducibility status -> passed.
- Review: Cycle 35 / Phase 32, Stop-Ship: No, P0:0, P1:0, P2:2.

## Gate Decision

Phase 32 is complete with WARN health.

Decision: `supporting_report_review_artifact_ready`.

It does not close T116 and does not move `docs/PAID_PILOT_READY_GATE.md` out
of `needs_fixes`.

## Remaining Gaps

- T116 private/anonymized operator-approved report evidence.
- Privacy-safe aggregate problem-interview evidence.
- Privacy-safe aggregate report-review evidence.
- Export willingness and manual pilot evidence.

## Next Task

T116 - Operator-Approved Private Run And Reviewed Report Evidence.

Status: blocked until the operator supplies one approved private or anonymized
artifact outside git. If no export exists, use the Dune report in report-review
conversations and record only aggregate non-identifying outcomes.
