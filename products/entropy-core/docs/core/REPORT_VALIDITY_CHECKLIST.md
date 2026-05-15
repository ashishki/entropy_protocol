# Report Validity Checklist

Version: 1.0
Date: 2026-05-12
Status: PHASE_15_SHARED_CHECKLIST

This checklist is the product-neutral review surface used before a Trader Risk
Audit or Signal Analytics Sandbox report moves from an internal artifact to a
controlled external pilot artifact. It is manual governance support only; it is
not automated approval, product certification, public release approval, or Core
platformization approval.

## Decision States

| State | Meaning | External use |
|---|---|---|
| `internal_draft` | Artifact exists but review is incomplete. | Not allowed. |
| `internal_demo_ready` | Operator can use the artifact internally to inspect format and findings. | Not allowed. |
| `external_pilot_blocked` | One or more stop-ship or unresolved validation items block delivery. | Not allowed. |
| `controlled_external_pilot_ready` | Manual validation, redaction, limitations, and delivery approval are complete. | Allowed only for the named pilot scope. |
| `rejected` | Artifact should not be used without regeneration or rewrite. | Not allowed. |

Internal demo readiness proves only that the report can be reviewed inside the
operator workspace. External pilot readiness additionally requires source/input
traceability, manual validation, redaction/privacy review, claim safety, and an
explicit delivery approval decision.

## Severity Model

| Severity | Meaning | Stop-ship rule |
|---|---|---|
| P0 | Critical false claim, private data leak, unsupported delivery approval, live/production/capital-ready implication, or materially wrong finding. | Blocks internal demo and external pilot until fixed and re-reviewed. |
| P1 | Material traceability, reproducibility, policy/config, or manual-validation gap. | Blocks external pilot; may allow internal demo only with visible limitation. |
| P2 | Non-material ambiguity, copy issue, incomplete explanatory note, or minor reproducibility caveat. | Does not block internal demo; blocks external pilot if unresolved and customer-visible. |
| P3 | Cosmetic formatting, typo, or optional clarity improvement. | Does not block unless it creates confusion about claims or evidence. |

Any P0 or delivery-approval mismatch is stop-ship. Three or more related P2
items in the same report section should be reviewed as a possible P1 pattern.

## Checklist

### 1. Input Provenance

- Product and `run_id` are recorded.
- Real input scope is named and bounded.
- Input refs point to product-local manifests, source packs, redacted exports,
  or public-source capture notes.
- Input hashes or safe fingerprints exist where deterministic hashing is safe.
- Private/customer data is not committed to Core docs, fixtures, or templates.
- Unsupported or omitted input fields are listed in a register.

### 2. Deterministic Processing

- `policy_config_hash` is recorded.
- `code_version_ref` is recorded.
- Generated artifact refs are stable and product-local.
- Deterministic transformations are identified separately from manual review.
- Known nondeterminism is listed before review, not after delivery.

### 3. Evidence And Source Traceability

- Every material finding points to a source row, source capture, policy rule, or
  public evidence ref.
- Ambiguous or insufficient-evidence findings are labeled as such.
- Source references are safe to show under the intended delivery scope.
- Evidence tables avoid raw secrets, credentials, private keys, or unnecessary
  customer-sensitive payloads.

### 4. Manual Validation

- Manual reviewer identity or role is recorded product-locally.
- Reviewer checked material findings against allowed source refs.
- Reviewer checked limitations and unsupported fields.
- Reviewer checked that the report does not imply unapproved Core, live,
  production, capital-ready, investment-advice, or future-performance claims.
- Manual validation status matches `docs/core/ARTIFACT_CONTRACT.md`.

### 5. Claim Safety

- No holdout read, holdout unlock, OOS/performance conclusion, live order
  placement, live broker/exchange execution, live capital action, production
  label, capital-ready label, public SDK claim, hosted Core service claim, or
  automated enforcement claim is present.
- Trader reports say they are not order blocking, live trading, broker/exchange
  execution, production, capital-ready, or investment advice.
- Signal reports say they are not trading advice, not future-performance
  prediction, not investment recommendation, not automated signal execution,
  not production, and not capital-ready.

### 6. Limitations

- Known data gaps are explicit.
- Manual judgment areas are explicit.
- Unsupported fields are explicit.
- External-source volatility is explicit for public web sources.
- Report wording does not hide limitations behind generic disclaimers.

### 7. Privacy And Redaction

- Raw customer/private data is excluded unless explicitly approved in the
  product-local scope note.
- Public-source captures avoid unnecessary personal data.
- Redacted examples preserve enough structure to validate findings.
- Delivery packet identifies which artifacts may be shown externally.

### 8. Reproducibility Notes

- Rerun procedure or checklist reference is present.
- Expected stable outputs are named.
- Accepted nondeterminism is named.
- Hash comparison expectations are recorded.

### 9. Delivery Approval

- Error register exists and is reviewed.
- P0/P1 items are closed or the artifact is blocked.
- External-delivery approval status is explicit.
- Approval is limited to the named artifact, audience, and pilot scope.
- Contract adoption alone is not treated as approval.

## Review Output

Each report review should produce a short product-local decision packet with:

- artifact refs reviewed;
- checklist decision state;
- open P0/P1/P2/P3 counts;
- stop-ship decision;
- manual validation status;
- redaction/privacy decision;
- external-delivery approval status;
- reviewer notes and date.

## Core Boundary

Core provides this checklist and the shared artifact vocabulary. Product
workspaces own report generation, data/source handling, validation evidence,
delivery approval, and customer/pilot feedback.
