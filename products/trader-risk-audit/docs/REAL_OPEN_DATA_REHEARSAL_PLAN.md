# Real Open Data Rehearsal Plan

Status: planned development route
Date: 2026-05-19
Audience: operator + development

This plan defines a real, open-data rehearsal path for Trader Risk Audit while
private pilot evidence is unavailable. It uses only real public data, not
synthetic rows, and it must remain clearly labeled as rehearsal evidence. It
does not satisfy the Phase 25 paid-pilot ready gate and does not replace T116
operator-approved private/anonymized evidence.

## Decision

Recommended primary source: public on-chain DEX swaps.

Why:

- swaps are real executed transactions recorded on-chain;
- a public address can produce a sequence of account-like actions;
- timestamp, asset, quantity, execution value, and transaction hash can be
  traced back to a public source;
- the shape is closer to a trader export than exchange-wide market tape.

Do not use synthetic rows for this route. Do not use open-source data as paid
pilot, PMF, market-demand, customer-validation, or willingness-to-pay evidence.

## Source Ranking

| Rank | Source | Use | Why | Main limitation |
|---|---|---|---|---|
| 1 | Dune curated DEX trades or equivalent public blockchain query | Primary candidate | Real swap rows with address-level sequence and public provenance. | Wallet choice can create privacy/doxxing risk; P&L and fees may be incomplete. |
| 2 | Google BigQuery public blockchain datasets | Alternative DEX/on-chain extraction path | Real public chain data with queryable transactions/logs. | Requires SQL, cost controls, and chain-specific decoding. |
| 3 | SEC Insider Transactions Data Sets | Official reference case | Official SEC real transaction disclosures with structured data. | Disclosure records are not trader account ledgers; already known caveat. |
| 4 | Binance public data | Market-data control case only | Real exchange prints and klines with reproducible files. | Exchange-wide tape, not one trader/account; not suitable for trader-risk report claims. |

Source references:

- Dune curated datasets: `https://docs.dune.com/data-catalog/curated/overview`
- Dune data catalog: `https://docs.dune.com/data-catalog/overview/`
- Google Cloud Ethereum public dataset overview:
  `https://cloud.google.com/blog/products/data-analytics/ethereum-bigquery-public-dataset-smart-contract-analytics`
- Google Cloud expanded blockchain public datasets:
  `https://cloud.google.com/blog/products/data-analytics/data-for-11-more-blockchains-in-bigquery-public-datasets`
- SEC Insider Transactions Data Sets:
  `https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets`
- Binance public data:
  `https://github.com/binance/binance-public-data`

## Non-Negotiable Labels

Every artifact must use one of these labels:

- `real_open_data_rehearsal_not_private_evidence`
- `official_disclosure_reference_not_trader_ledger`
- `market_tape_control_not_account_ledger`

Forbidden labels:

- `private_pilot_evidence`
- `paid_pilot_evidence`
- `customer_validation`
- `PMF`
- `market_demand`
- `production_ready`

## Acceptance Boundary

The rehearsal is successful only if it proves:

- the source can be selected with clear provenance and terms/licensing notes;
- real rows can be transformed into the project case-pack contract;
- report language preserves source limitations;
- no private data or private paths enter git;
- the resulting report is reproducible and manually reviewed;
- the ready gate remains `needs_fixes` until true private/anonymized evidence
  exists.

The rehearsal fails if:

- source provenance is unclear;
- the selected address appears to identify a private individual in a risky way;
- row transformation requires fabricated values;
- P&L is guessed from unsupported fields;
- report wording implies private pilot, customer, PMF, or paid evidence;
- any secret, private path, raw private data, or customer identifier is added.

## Phase 27 Development Tasks

### T117 - Real Open Data Source Selection

Goal: select one real open-data source for rehearsal.

Deliverables:

- `docs/REAL_OPEN_DATA_SOURCE_SELECTION.md`
- source provenance, license/terms notes, and rejection notes;
- chosen source label;
- explicit evidence boundary.

Acceptance:

- source is real and public;
- no synthetic rows;
- no random retail wallet unless privacy risk is reviewed;
- DEX/on-chain source is preferred unless blocked.

### T118 - Open Data Extraction Contract

Goal: define the exact extraction fields before any data is committed.

Deliverables:

- extraction query or download instructions;
- source-field to canonical-field mapping;
- unsupported fields register;
- privacy and provenance checklist.

Minimum target schema:

| Canonical field | DEX/open-data mapping |
|---|---|
| `timestamp` | block time or transaction time |
| `symbol` | token pair or selected base asset |
| `side` | derived buy/sell relative to selected base asset, with caveat |
| `quantity` | token amount for selected base asset |
| `price` | USD value divided by quantity when supported |
| `fees` | chain fee or `0` only if source documents fee absence and caveat is visible |
| `account_id` | safe public-source scope label, not raw wallet address in report copy |
| `source_row_number` | deterministic row sequence |

Forbidden transformations:

- fabricated fees;
- fabricated P&L;
- arbitrary side assignment without a visible mapping rule;
- hidden wallet/address identifiers in report copy.

### T119 - Real Open Data Case Pack

Goal: build one case pack under `demo/` from the selected source.

Suggested path:

- `demo/real_open_dex_swaps_001/`

Required files:

- `source.md`
- `input/trades.csv`
- `policy.yaml`
- `output/run_status.json`
- `output/report.md`
- `output/report_reviewed.md`
- `output/manifest.json`
- `output/reproducibility_status.json`

Rules:

- raw source download can be referenced, but only the transformed audit input
  may be committed after privacy/provenance review;
- reports must say `real_open_data_rehearsal_not_private_evidence`;
- source row ids may be deterministic public-source refs, but avoid exposing
  full wallet addresses unless the source is an explicitly public organization
  address and review approves it.

### T120 - Manual Review And Error Register

Goal: manually review the real open-data report.

Deliverables:

- `docs/audit/real_open_data_case_reviews/real_open_dex_swaps_001.md`
- update to `docs/audit/PHASE23_ERROR_REGISTER.md` or a Phase 27 register;
- reviewed report caveat header.

Review focus:

- source truth;
- account-like interpretation risk;
- side derivation;
- P&L support;
- fee support;
- limitation wording;
- claim guard safety.

### T121 - Rehearsal Gate Update

Goal: update docs with what the real open-data rehearsal proves and does not
prove.

Deliverables:

- update `docs/OPEN_SOURCE_AUDIT_QUALITY_DASHBOARD.md`;
- update `docs/OPEN_SOURCE_RULE_COVERAGE_MATRIX.md`;
- update `docs/PAID_PILOT_READY_GATE.md` only to record that this does not
  close T116;
- archive a Phase 27 review if the task batch is completed.

Gate result:

- PASS for development rehearsal only if report quality is truthful and
  reproducible;
- paid-pilot gate remains `needs_fixes` until T116 is completed with real
  private/anonymized evidence.

## Recommended First Implementation Route

1. Start with Dune or BigQuery DEX swaps because it is closest to a public
   account-like transaction sequence.
2. Select an address only if it is explicitly public or low-risk after privacy
   review.
3. Extract a small bounded period, for example 20-100 swaps.
4. Define side relative to one base asset and write the caveat before running.
5. Use rules that are meaningful for the mapped fields:
   - forbidden asset;
   - max position size or max trade notional;
   - cooldown-like sequence rule if timestamps support it;
   - unsupported leverage rule to verify limitation handling.
6. Run the existing local audit workflow.
7. Manually review report truth and limitation wording.
8. Update the ready gate as still `needs_fixes`, with this rehearsal listed as
   development evidence only.

## Why Not Start With Binance Public Data

Binance public data is real, but it is exchange-wide market tape. It does not
represent one trader's behavior and has no written rules or account scope. Use
it only as a market-data control case, not as the main rehearsal for trader
risk audit.

## Why Not Start With SEC Data

SEC insider data is official and real, but it is a disclosure dataset, not a
trader ledger. It is useful as an official-reference pack, and this repo
already carries the limitation that SEC rows must not be framed as customer
account history.

## Operator Approval Needed Before T117

Before implementation, the operator must choose:

- preferred source path: `dune`, `bigquery`, `sec`, or `binance_control`;
- whether public on-chain addresses may be used;
- whether full transaction hashes may appear in committed source refs or should
  be truncated;
- whether Dune/BigQuery credentials or paid query costs are allowed. If not,
  use only downloadable/public no-account sources.
