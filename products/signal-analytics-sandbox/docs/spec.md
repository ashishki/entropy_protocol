# Specification — Signal Analytics Sandbox

Version: 1.0
Last updated: 2026-05-07
Status: Phase 1 Draft (pending Phase 0 gates SAS-001 + SAS-002)

---

## Overview

Signal Analytics Sandbox produces an evidence-backed audit report of a public signal source's historical performance. An operator points the system at a public Telegram channel, X account, or website ledger; the system normalizes messy historical trading calls into a structured signal ledger, deterministically matches them against historical market data via a configurable price-data adapter, and renders a Markdown report citing per-signal evidence, deterministic outcome rules, and immutable price-snapshot provenance.

The product is a local-first Python library + CLI in v1. It does not trade, copy-trade, scrape private sources, or claim to predict future performance.

---

## User Roles

| Role | Capabilities |
|------|--------------|
| Operator | Declares sources, captures public posts, runs extraction/review/snapshot/match/report subcommands, approves reports for delivery. |
| Reviewer (human, may be the operator) | Reviews extraction drafts and approves final signal records before evaluation; approves source eligibility and report release. |
| Pilot user | Receives a delivered Markdown report. Does not interact with the system directly in v1. |

There is no programmatic API surface in v1. There is no multi-user, hosted, or shared-state surface.

---

## Feature Areas

### F1 — Source Manifest and Eligibility

**Description.** The system records each public signal source with a manifest containing: source identifier, public URL, source type (telegram_public, x_public, website_public), capture method, ToS posture (per SAS-002), eligibility verdict (approved | blocked | pending), and operator notes.

**Acceptance criteria.**
1. Creating a SourceManifest with `source_type=telegram_public` and `eligibility_verdict=approved` succeeds and is persisted as JSON in `<workspace>/sources/<source_id>.json`.
2. Creating a SourceManifest without `eligibility_verdict` raises a validation error (Pydantic `ValidationError`).
3. Loading any source whose `eligibility_verdict != "approved"` from a downstream subcommand raises `SourceNotApproved` and aborts the run.
4. Source types not in `{telegram_public, x_public, website_public}` are rejected at validation time. Adding a new source type requires an ADR.

**Out of scope for v1.** Private group sources, paywalled sources, sources requiring authentication.

---

### F2 — Capture Loader

**Description.** Operator-captured raw posts are loaded from `<workspace>/captures/<source_id>/<capture_id>.{json,md}`. Each capture must declare URL, capture timestamp (ISO-8601 UTC), raw text, and SHA-256 of the raw text.

**Acceptance criteria.**
1. Loading a valid capture file produces a `CapturedPost` object whose `text_sha256` matches the on-disk SHA-256.
2. Loading a capture file whose declared `text_sha256` mismatches the recomputed SHA-256 raises `CaptureChecksumMismatch` and refuses to return the post.
3. Loading a capture file with a non-public URL (matches private-source patterns from SAS-002) raises `PrivateSourceForbidden`.
4. Captures are sorted deterministically by `(capture_timestamp_utc, capture_id)` when batch-loaded.

**Out of scope for v1.** Automated post fetching from any source. All captures are operator-supplied.

---

### F3 — Extraction Adapters

**Description.** Extraction transforms a `CapturedPost` into a draft `SignalRecord`. v1 ships a `ManualExtractionAdapter` and a `RuleExtractionAdapter`. An `LLMExtractionAdapter` is implemented but disabled by default; activation requires `SIGNAL_SANDBOX_ENABLE_LLM=1` plus an explicit per-run `--llm-approved` flag.

**Acceptance criteria.**
1. `ManualExtractionAdapter.extract(post)` opens the operator's editor with a pre-filled template containing every required `SignalRecord` field plus the post's `evidence_url` and `text_sha256`. The returned draft preserves these evidence fields exactly.
2. `RuleExtractionAdapter` accepts a named rule template and produces a draft if the post matches the template; if not, returns `ExtractionResult(status="defer_to_human", reason=...)`.
3. `LLMExtractionAdapter.extract(post)` raises `LLMNotApproved` unless both `SIGNAL_SANDBOX_ENABLE_LLM=1` and `--llm-approved` are set.
4. When the LLM adapter is approved, every draft it returns has `status="draft_pending_review"` and `extraction_metadata.adapter_id="llm/<provider>/<model>"`. No path can write an LLM draft directly to the approved ledger.
5. The LLM adapter aborts the run when accumulated `cost_usd` exceeds `SIGNAL_SANDBOX_COST_CAP_USD`, raising `CostCapExceeded`.

**Out of scope for v1.** Multimodal/OCR extraction; autonomous extraction; LLM output written to the approved ledger without human review.

---

### F4 — Signal Record Schema and Ledger I/O

**Description.** A `SignalRecord` is the canonical structured representation of one trading call: source_id, capture_id, evidence_url, text_sha256, extracted_timestamp_utc, asset_symbol, direction (long | short | flat | unknown), entry, stop, target, confidence_flags, ambiguity_flags, extraction_metadata. The ledger is persisted as Parquet at `<workspace>/ledger/<source_id>.parquet`.

**Acceptance criteria.**
1. A `SignalRecord` with `direction="unknown"` or any non-empty `ambiguity_flags` is accepted by the schema but is excluded from outcome matching unless explicitly opted-in.
2. Writing the same approved set of records twice to the same ledger path produces a byte-identical Parquet file (deterministic column order, no timestamp metadata that varies per write).
3. Reading a ledger file and writing it back without changes produces a byte-identical Parquet file.
4. The dedup key for a record is the SHA-256 of the canonical JSON encoding of `{source_id, extracted_timestamp_utc, asset_symbol, direction, entry, stop, target}` and is computed and stored at write time.
5. Writing two records with the same dedup key into the same ledger raises `DuplicateSignalRecord` unless `--force-duplicate` is passed; with `--force-duplicate`, both records are flagged with `ambiguity_flags=["duplicate_dedup_key"]`.

**Out of scope for v1.** Cross-source ledgers; multi-asset combined records.

---

### F5 — Price-Data Adapters and Snapshots

**Description.** `PriceDataProvider` is an abstract interface with an `as_of` parameter. v1 ships `OperatorFilePriceProvider` (reads CSV/Parquet supplied by the operator), `ExchangePublicOHLCVProvider` (ccxt-style), `YFinanceDevProvider` (dev/prototype, never canonical without explicit approval), and `PaidPriceDataProvider` (gated, off by default). A snapshot is a serialized OHLCV bundle plus a metadata record (`provider_id`, `as_of_utc`, `range_start_utc`, `range_end_utc`, `assets`, `sha256`).

**Acceptance criteria.**
1. `PriceDataProvider.snapshot(assets, range_start, range_end)` returns a `PriceSnapshot` whose `sha256` is the SHA-256 of the canonical byte representation of the OHLCV bundle.
2. The same provider invoked twice for the same `(assets, range_start, range_end)` and the same upstream data produces a `PriceSnapshot` with an identical `sha256`. Snapshots are immutable on disk.
3. `YFinanceDevProvider.snapshot(...)` always sets `provider_status="prototype"` on the snapshot. The report generator MUST include a "non-canonical price source" warning block when the active snapshot's `provider_status="prototype"` and the run does not pass `--accept-prototype-prices`.
4. `PaidPriceDataProvider` raises `PaidProviderNotApproved` unless `SIGNAL_SANDBOX_ENABLE_PAID_PRICE=1` and `--paid-prices-approved` are both set.
5. A run aborts with `CostCapExceeded` if cumulative paid-provider cost exceeds `SIGNAL_SANDBOX_COST_CAP_USD`.

**Out of scope for v1.** Real-time price feeds, intraday tick data, options chains, futures roll-aware adapters.

---

### F6 — Outcome Matching

**Description.** The outcome matcher takes an approved ledger and a price snapshot and produces per-signal `OutcomeRecord` rows: `dedup_key`, `outcome` (target_hit | stop_hit | timeout_no_hit | excluded_ambiguous | excluded_no_price), `entry_fill_timestamp`, `exit_timestamp`, `return_pct`, `mae_pct`, `mfe_pct`, `outcome_rule_id`, `snapshot_sha256`.

**Acceptance criteria.**
1. Re-running the matcher on the same approved ledger and the same snapshot produces a byte-identical outcomes Parquet file.
2. Records with `direction in ("flat", "unknown")` or non-empty `ambiguity_flags` produce `outcome="excluded_ambiguous"`. They contribute to coverage stats but not to win/loss.
3. Records whose `asset_symbol` is not in the snapshot's `assets` produce `outcome="excluded_no_price"`.
4. Each `OutcomeRecord` cites a deterministic `outcome_rule_id` from the published rule registry; the report renders the rule text for every distinct rule cited.
5. Numerical fields (`return_pct`, `mae_pct`, `mfe_pct`) are computed in IEEE-754 double precision with explicit rounding to 6 decimal places; rounding is documented with the rule.

**Out of scope for v1.** Slippage modeling, fee modeling, partial fills, leverage-aware position sizing.

---

### F7 — Aggregated Summary

**Description.** Aggregator produces win/loss/coverage/drawdown-style summaries over an outcomes file: total signals, evaluated signals, excluded counts (by reason), wins/losses/timeouts, win rate, average return, median return, max drawdown of the equity-style cumulative-return series.

**Acceptance criteria.**
1. Re-running the aggregator on the same outcomes file produces an identical summary record (byte-identical JSON).
2. Win rate is reported only over evaluated signals (excludes ambiguous and no-price).
3. The aggregator never produces a "predicted future return" or any forward-looking value.
4. Equity-style series are labelled as "historical, assumes no slippage and no fees" in the rendered report.

**Out of scope for v1.** Risk-adjusted metrics (Sharpe, Sortino), cohort comparisons across sources.

---

### F8 — Markdown Report Generator

**Description.** Renders a Markdown report from `(SourceManifest, ledger, snapshot metadata, outcomes, summary)`. The report includes a non-advice disclaimer, source eligibility citation (SAS-002), per-signal evidence references, snapshot provenance, deterministic outcome-rule references, and limitations.

**Acceptance criteria.**
1. Rendering the same `(ledger SHA, snapshot SHA, outcomes SHA, summary SHA)` tuple twice produces a byte-identical Markdown report file.
2. Every report contains a non-advice disclaimer block matching the canonical disclaimer text in `src/signal_sandbox/reports/disclaimers.py`. Removal or modification of the disclaimer requires an ADR.
3. Every report cites the snapshot `provider_id`, `as_of_utc`, and `sha256` exactly once in the Provenance section.
4. Every per-signal row in the report includes the evidence URL, capture timestamp, and `text_sha256` linking back to the original capture.
5. If the snapshot's `provider_status="prototype"` and `--accept-prototype-prices` was not passed, rendering aborts with `PrototypeSnapshotNotAccepted`.
6. The report contains an "Excluded signals" table grouped by exclusion reason, with counts. No excluded signal contributes to win/loss numbers.

**Out of scope for v1.** PDF rendering, email delivery, scheduled report runs, per-user customization.

---

### F9 — `signal-sandbox status` Health Substitute

**Description.** A read-only CLI subcommand that prints configuration summary, version, workspace path, active adapter set, and cost-cap status. Replaces the playbook's HTTP `GET /health` for this CLI/library project.

**Acceptance criteria.**
1. `signal-sandbox status` exits 0 when configuration is valid and the workspace path exists; exits non-zero with a clear error when configuration is invalid.
2. Output never includes API keys, evidence URLs, raw post text, or operator-handle strings beyond `source_id`.
3. The subcommand performs no network calls.

**Out of scope for v1.** HTTP health endpoint; metrics scraping.

---

### F10 — CLI Surface

**Description.** Console script `signal-sandbox` exposes the operator workflow. Subcommands: `init-workspace`, `add-source`, `extract`, `review`, `snapshot`, `match`, `report`, `status`.

**Acceptance criteria.**
1. `signal-sandbox --help` lists every subcommand above with a one-line description.
2. Each subcommand has its own `--help` listing required arguments.
3. Unknown subcommands exit non-zero with a clear error message.
4. The CLI never performs network calls except via an explicitly active adapter (price provider or LLM extraction).

**Out of scope for v1.** Interactive TUI; web UI; streaming output.

---

## Reproducibility Contract (cross-feature)

Given the same approved ledger Parquet and the same price snapshot, the following must hold:

- `signal-sandbox match` produces an identical outcomes Parquet file every time.
- `signal-sandbox report` produces an identical Markdown file every time.
- A re-run produces identical report SHA-256, identical outcomes SHA-256, and identical summary SHA-256.

Violation of this contract is automatically a P1 finding. This is the load-bearing claim of the product.
