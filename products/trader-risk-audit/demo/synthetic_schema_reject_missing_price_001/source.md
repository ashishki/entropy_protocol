# Synthetic Missing Price Reject Case Source Metadata

source_name: Synthetic missing-price schema reject fixture
source_class: sanitized synthetic edge case
source_url: none; generated fixture
source_accessed_date: 2026-05-15
source_record_type: malformed broker/export-like trade rows
public_sample_label: synthetic artifact validation; reject case
intended_use: artifact_quality_only
privacy_reviewed_by: codex
privacy_review_date: 2026-05-15

## Selection Rationale

This fixture exists to preserve a reject/schema case in the Phase 23 batch. It
intentionally omits the required `price` column so the import path should block
with an explicit schema error before report generation.

## Expected Outcome

- expected_case_type: reject
- expected_evaluable_fields: none until the missing price column is supplied
- expected_limitations: required source column is absent
- expected_report_behavior: should reject before deterministic audit artifacts
  are generated.

## Evidence Boundary

The rows are synthetic and represent no real trader, account, broker, or
customer. This pack can support artifact-quality validation only.
