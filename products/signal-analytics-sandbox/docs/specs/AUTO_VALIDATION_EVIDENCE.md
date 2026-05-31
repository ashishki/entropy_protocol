# Auto-Validation Evidence Contract

Date: 2026-05-31
Status: Phase 40 implementation in progress

## Purpose

The auto-validation system exists to automate media/chart candidate acceptance
without trusting a model review as final truth. It accepts only rows with
auditable evidence and strict validator agreement. Ambiguous rows remain
`needs_human`.

## Required Evidence Bundle

Every candidate entering auto-validation must provide:

- stable candidate id;
- source id and public source URL;
- source timestamp in UTC;
- source document id or capture id;
- text hash and/or media hash;
- media ref id, OCR ref id, transcript ref id, or chart-region refs;
- extracted candidate fields: asset, direction, entry, stop, targets, horizon;
- evidence refs for every extracted field;
- model extraction metadata, if any;
- candidate provenance version;
- allowed source class.

Missing source timestamp, missing checksum, missing evidence ref, unsupported
source class, or private-source risk invalidates the bundle.

Implemented schemas/validators: `src/signal_sandbox/auto_validation/evidence.py`,
`src/signal_sandbox/auto_validation/results.py`,
`src/signal_sandbox/auto_validation/timing.py`,
`src/signal_sandbox/auto_validation/setup_consistency.py`,
`src/signal_sandbox/auto_validation/provider_eligibility.py`,
`src/signal_sandbox/auto_validation/post_factum.py`,
`src/signal_sandbox/auto_validation/decision.py`.

## Validator Result States

Each validator returns one of:

- `passed`
- `failed`
- `uncertain_needs_human`
- `excluded_provider_gap`
- `blocked_customer_facing`

Each result must record:

- validator id and version;
- deterministic input hash;
- evidence refs used;
- confidence score or confidence label;
- blocker reasons;
- human-readable rationale;
- created date.

Blank validator version or missing evidence refs make the result invalid.

## Required Validators

### Pre-Outcome Timing

Proves the post timestamp occurred before target/stop or relevant market move.
If market data is missing or the move already happened, the row cannot pass.

### OCR Level And Setup Consistency

Requires evidence refs for entry, stop, target, and direction. Long setups must
have `stop < entry < target`. Short setups must have `target < entry < stop`.
Mixed trades, ambiguous levels, and low confidence route to `needs_human`.

### Asset Proxy And Provider Eligibility

Maps aliases to approved instruments or explicit exclusions. Ambiguous aliases,
unsupported markets, unapproved quote scales, or missing provider coverage do
not become wins or losses.

### Post-Factum And Closed-Position Detection

Flags PnL screenshots, closed-position UI, take-profit-hit language,
already-managed-position language, and retrospective claims. High-confidence
post-factum rows are rejected for predictive metrics.

### Customer-Facing Policy Gate

Requires public source refs, accepted validation audit refs, recompute
provenance, visible caveats, and no forbidden wording. It is separate from
model confidence and cannot be bypassed by model output.

## Final Decision Rules

`auto_accepted` requires all required validators to pass and the customer-facing
policy gate to pass for report/demo use.

`auto_rejected` applies when evidence proves the row is invalid, post-factum, or
not a predictive claim.

`excluded_provider_gap` applies when source evidence may be useful but no
approved provider/proxy path exists.

`needs_human` applies to uncertainty, missing fields, conflicting evidence,
low-confidence OCR, ambiguous setup math, or mixed validator outcomes.

`blocked_customer_facing` applies when internal validation may be useful but
customer-facing policy is not satisfied.

## Evaluation Requirement

Before any auto-accepted row can affect client-ready metrics, the full stack
must run against the 9 Phase 38 candidates and produce
`docs/pilot/clientready_AUTO_VALIDATION_EVAL.md/json`.

The evaluation must report counts for `auto_accepted`, `auto_rejected`,
`excluded_provider_gap`, `needs_human`, and `blocked_customer_facing`, with
validator audit refs and blocker reasons for every row.
