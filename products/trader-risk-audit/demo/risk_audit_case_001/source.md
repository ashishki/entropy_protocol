# Synthetic Risk Audit Case 001 Source Metadata

source_name: Synthetic broker-export-like risk audit fixture
source_class: sanitized synthetic edge case
source_url: none; generated fixture
source_accessed_date: 2026-05-15
source_record_type: broker/export-like trade rows
public_sample_label: synthetic artifact validation; not customer evidence
intended_use: artifact_quality_only
privacy_reviewed_by: codex
privacy_review_date: 2026-05-15

## Selection Rationale

This fixture is a compact positive-finding case for the open-source case bank.
It exercises broker/export-like rows with realized P&L, cooldown-after-loss,
forbidden-asset, max-position-size, and max-daily-loss policy coverage.

## Expected Outcome

- expected_case_type: positive_finding
- expected_evaluable_fields: timestamp, symbol, side, quantity, price, fees,
  account_id
- expected_limitations: synthetic provenance; not public market or customer
  evidence
- expected_report_behavior: should produce deterministic violations and P&L
  attribution after T101 runs the audit batch.

## Evidence Boundary

The rows are synthetic and represent no real trader, account, broker, or
customer. This pack can support artifact-quality validation only.
