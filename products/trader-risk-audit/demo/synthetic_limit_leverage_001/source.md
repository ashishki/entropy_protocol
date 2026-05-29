# Synthetic Leverage Limitation Case Source Metadata

source_name: Synthetic missing-leverage limitation fixture
source_class: sanitized synthetic edge case
source_url: none; generated fixture
source_accessed_date: 2026-05-15
source_record_type: broker/export-like trade rows without leverage fields
public_sample_label: synthetic artifact validation; limitation case
intended_use: artifact_quality_only
privacy_reviewed_by: codex
privacy_review_date: 2026-05-15

## Selection Rationale

This fixture exists to preserve a limitation case in the Phase 23 batch. The
policy asks for a max-leverage rule, while the input fixture intentionally has
no leverage field. A valid audit should report an unsupported-data limitation
instead of inventing leverage evidence.

## Expected Outcome

- expected_case_type: limitation
- expected_evaluable_fields: timestamp, symbol, side, quantity, price, fees,
  account_id
- expected_limitations: max_leverage cannot be evaluated from this CSV shape
- expected_report_behavior: should preserve the unsupported leverage
  limitation and avoid a guessed violation.

## Evidence Boundary

The rows are synthetic and represent no real trader, account, broker, or
customer. This pack can support artifact-quality validation only.
