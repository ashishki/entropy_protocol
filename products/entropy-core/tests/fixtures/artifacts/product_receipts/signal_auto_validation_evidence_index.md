# Signal Auto-Validation Receipt Evidence Lookup Example

This is a Core-local synthetic evidence lookup table for a product receipt
shape. It contains metadata only and does not include product runtime payloads,
raw source text, customer data, credentials, holdout data, or delivery approval.

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|
| signal-auto-validation:asset-ref | Product receipt evidence example | `tests/fixtures/artifacts/product_receipts/signal_auto_validation_valid.json`; `tests/fixtures/artifacts/product_receipts/signal_auto_validation_evidence_index.md` | Synthetic Signal receipt asset evidence ref resolves to safe local metadata without raw source text or product runtime logic | 2026-05-31: fixture example | Yes |
| signal-auto-validation:market-1 | Product receipt evidence example | `tests/fixtures/artifacts/product_receipts/signal_auto_validation_valid.json`; `tests/fixtures/artifacts/product_receipts/signal_auto_validation_evidence_index.md` | Synthetic Signal receipt market-window evidence ref resolves to safe local metadata without live execution or capital scope | 2026-05-31: fixture example | Yes |
