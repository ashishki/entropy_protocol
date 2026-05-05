# P4 Coverage Window Strategy Decision

Date: 2026-05-05
Status: DECIDED
Decision ID: P4-WINDOW-001

## Decision

Do not continue broad collection under the current 2023-01 through 2025-12
20-asset matrix until the P4 coverage window is revised.

The next step is P0.7-009: P4 Extended History Eligibility Probe. It must check
which approved Binance public archive symbols can provide enough history to
produce 156 valid post-warmup P4 labels under `P4-RBL-v1`, before any larger
download plan is created.

## Evidence Basis

P0.7-007 converted the full planned BTCUSDT 2023-01 through 2025-12 window:

| Metric | Result |
|---|---|
| Dataset hash | `15dd83aa0222f764247f535fbd5ac1c8c67cdd50770870f5fc9aa66dac0f4592` |
| Daily bars | 1096 |
| Data quality status | `PASS` |
| P4 generated labels | 156 |
| P4 valid post-warmup labeled weeks | 1 |
| P4 required valid labeled weeks | 156 |
| Gate evidence complete | `false` |

The data path is healthy, but the evidence window is too short for the encoded
label semantics. Under the current labeler, the first 155 completed weekly bars
are warmup. A 3-year daily window yields about 156 completed weekly labels, which
leaves only about 1 post-warmup valid label.

## Options Considered

| Option | Decision | Rationale |
|---|---|---|
| Continue current 2023-2025 matrix | Rejected | It would likely produce the same valid-label insufficiency across assets while consuming time and artifact space. |
| Treat 156 generated labels as satisfying the gate | Rejected | That would silently change the encoded acceptance meaning and weaken the no-claim boundary. |
| Expand the source window blindly | Rejected for immediate execution | Some current universe assets may not have enough Binance history; eligibility must be checked first. |
| Run an extended-history eligibility probe | Accepted | It is cheap, source-approved, and directly answers whether the current universe can satisfy the encoded P4 gate. |

## Required Probe

P0.7-009 must:

- Use only approved Binance public archive URLs.
- Avoid full broad downloads unless a symbol/month is selected for a canary.
- Check whether each target symbol has enough monthly `1d` archives to support
  at least 312 completed weekly labels, which is the practical minimum for 156
  valid post-warmup labels under the current labeler.
- Report eligible assets, ineligible assets, earliest available months, missing
  months, and whether the current 20-asset universe can produce at least 15
  passing assets without a universe revision.
- Keep gate claim disabled.

## Boundary

This decision does not revise the charter, approve Phase 0, start Phase 1, or
make performance claims. It only redirects P4 evidence collection away from a
known-insufficient 3-year matrix and toward a source-history eligibility check.

## Next Step

Start P0.7-009: P4 Extended History Eligibility Probe.
