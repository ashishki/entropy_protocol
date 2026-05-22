# Dune Public Wallet Rehearsal

Status: complete development rehearsal
Date: 2026-05-19

## Purpose

Use Dune as a real public-data source while no operator-approved
private/anonymized trader export exists for T116.

This rehearsal strengthens the technical and product hypothesis that the local
audit workflow can ingest real public DEX rows, preserve provenance, generate a
reviewed report, and surface unsupported-data limitations. It does not prove
customer demand, PMF, willingness to pay, private report readiness, or paid
pilot readiness.

## Result

| Artifact | Location |
|---|---|
| Case pack | `demo/dune_public_wallet_dex_001/` |
| Source metadata and SQL | `demo/dune_public_wallet_dex_001/source.md` |
| Canonical audit input | `demo/dune_public_wallet_dex_001/trades.csv` |
| Policy | `demo/dune_public_wallet_dex_001/policy.yaml` |
| Reviewed report | `demo/dune_public_wallet_dex_001/output/report_reviewed.md` |
| Reproducibility status | `demo/dune_public_wallet_dex_001/output/reproducibility_status.json` |
| Manual review | `docs/audit/real_open_data_case_reviews/dune_public_wallet_dex_001.md` |

## What Was Queried

Discovery used Dune `dex.trades` on Ethereum over a trailing 14-day window to
find public `tx_from` submitter addresses with 20-150 DEX rows. The selected
address had 127 rows and about 4.1M USD notional in the discovery result.

Extraction then selected 80 real public rows for that address:

- `block_time`
- project/version metadata
- transaction hash and event index
- public DEX participants
- token pair and bought/sold token fields
- token amounts
- `amount_usd`

The committed case uses only transformed canonical audit rows and source
metadata. No key, credential, private row, private path, customer identifier, or
wallet-owner claim is committed.

## Transformation

The case pack maps Dune rows into the existing canonical CSV:

| Canonical field | Dune source |
|---|---|
| `timestamp` | `block_time` |
| `symbol` | `token_bought_symbol` |
| `side` | fixed to `buy`, meaning bought-token side of the swap |
| `quantity` | `token_bought_amount` |
| `price` | `amount_usd / token_bought_amount` |
| `fees` | `0` schema placeholder |
| `account_id` | safe public-scope label |

The policy intentionally checks `max_position_size` against a 25,000 USD
threshold and includes `max_leverage` as an unsupported-data limitation.

## Evidence Produced

- 80 real public Dune DEX rows were transformed into canonical audit input.
- The audit generated 76 deterministic max-position findings.
- The report preserved one unsupported leverage limitation.
- `case-bank validate` passed for the new case pack.
- A deterministic rerun produced matching stable manifest content hashes.

## What This Shows

This is useful evidence for:

- real public DEX extraction through Dune;
- source-row provenance using query metadata, transaction hashes, and event
  indexes;
- deterministic report generation on real non-synthetic public rows;
- clear unsupported-data behavior for leverage and execution costs;
- client conversation material for report usefulness and trust review.

## What It Does Not Show

This does not show:

- who owns the wallet;
- that the wallet is one discretionary trader;
- private exchange account history;
- written trader risk rules;
- gas, LP fees, MEV/slippage, or all-in execution costs;
- leverage, margin, balances, deposits, withdrawals, or account equity;
- verified realized trader P&L;
- customer demand, paid-pilot readiness, PMF, or willingness to pay.

## How To Use In A Client Conversation

Show the reviewed report only after saying the boundary aloud:

> This is a real public Dune DEX rehearsal, not your private account and not a
> paid pilot. I use it to show the report shape, source traceability, and where
> the system refuses to infer missing leverage or fee data.

Ask:

- Does this finding table make sense without extra explanation?
- Which missing fields would block trust for your workflow?
- Would you want this report on your own export if wallet/account identity and
  policy were approved by you?
- What would need to be present before you would pay for one reviewed audit?

Record only aggregate, non-identifying answers using the Phase 30 safe
aggregate evidence format.

## Gate Decision

This rehearsal supports technical and report-review confidence, but T116 remains
blocked. The paid-pilot ready gate remains `needs_fixes` until one
operator-approved private or anonymized export is run and manually reviewed
outside git.
