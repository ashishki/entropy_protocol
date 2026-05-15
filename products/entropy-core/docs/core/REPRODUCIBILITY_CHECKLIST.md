# Reproducibility Checklist

Version: 1.0
Date: 2026-05-12
Status: PHASE_15_SHARED_CHECKLIST

This checklist defines how product agents rerun the same report inputs, compare
outputs, and document accepted nondeterminism. It is product-neutral guidance
for report artifacts adopting `docs/core/ARTIFACT_CONTRACT.md`.

## Rerun Steps

1. Confirm the artifact uses `artifact_contract_version:
   entropy-core-artifact/v1`.
2. Confirm `product`, `run_id`, `policy_config_hash`, `code_version_ref`, and
   `generated_artifact_refs` are present.
3. Recreate the product-local environment or reviewed source snapshot named by
   `code_version_ref`.
4. Load only the input refs allowed by the product-local scope note.
5. Verify input hashes or safe fingerprints where they are expected.
6. Regenerate the report artifact or source/evidence packet.
7. Compare expected stable output hashes.
8. Review accepted nondeterminism before treating any diff as a failure.
9. Record rerun result, reviewer, date, changed fields, and decision state.

## Output Hash Comparison

Products should compare hashes for stable artifacts such as:

- redacted input manifests;
- policy/config files;
- normalized violation or evidence tables;
- generated report Markdown/PDF/JSON where formatting is deterministic;
- delivery packets;
- error registers after review closure.

The comparison record should include:

- previous hash;
- rerun hash;
- hash method;
- paths or artifact refs compared;
- expected stable fields;
- accepted nondeterministic fields;
- reviewer decision: `match`, `accepted_nondeterminism`, `mismatch_blocked`,
  or `not_reproducible_by_design`.

## Accepted Nondeterminism

These fields may differ when documented before comparison:

- generation timestamp;
- local absolute paths;
- machine/user names;
- manual review timestamp;
- reviewer notes ordering when semantically identical;
- public-source availability, capture timestamp, or page content drift;
- generated PDF metadata that does not affect report findings;
- redaction tokens when they are stable within the reviewed packet but not
  across separate private input captures.

Accepted nondeterminism must not hide changed findings, changed source refs,
changed policy interpretation, changed claim language, privacy leaks, or
delivery approval drift.

## Failure Handling

Treat these as blockers for external pilot readiness:

- missing input refs or hashes where required;
- changed material findings without documented input or policy change;
- changed no-claim boundary;
- changed manual validation status without reviewer approval;
- changed external-delivery approval status;
- missing error register;
- source refs that no longer support a material finding.

## Trader Risk Audit Guidance

Trader reproducibility focuses on whether the same real audit inputs produce the
same material findings.

Required checks:

- same redacted trade export manifest or approved safe fingerprint;
- same policy/rule manifest and `policy_config_hash`;
- same code version or reviewed source snapshot;
- same violation ids, rule ids, source row ids, severities, observed values,
  thresholds, and attribution refs for material findings;
- same report no-claim labels;
- same delivery decision packet after manual validation.

Allowed differences:

- report generation timestamp;
- local source paths;
- reviewer note timestamp;
- formatting-only PDF metadata;
- redaction token text if the redaction map is product-local and reviewed.

Any changed violation truth, policy interpretation, severity, attribution, or
delivery approval must be recorded as a mismatch until manually reviewed.

## Signal Analytics Sandbox Guidance

Signal reproducibility depends on source availability and capture method. The
artifact must distinguish reproducible packet fields from public-source fields
that may drift.

Hash-reproducible fields should include:

- checked-in or redacted source capture pack;
- source/evidence table;
- ambiguity or unsupported-field register;
- synthesis/review configuration;
- report packet generated from the captured source pack;
- delivery decision packet.

Availability-dependent fields may include:

- live public page text;
- deleted or edited posts/pages;
- rate-limited source access;
- search-result ordering;
- source metadata added after capture.

Manual-review-dependent fields may include:

- ambiguity resolution;
- insufficient-evidence language;
- claim-safety edits;
- external pilot suitability.

Signal artifacts should say which findings reproduce from the checked-in source
pack and which would require a fresh public-source recapture.

## Review Output

Each reproducibility review should record:

- artifact refs rerun;
- hash comparison table;
- accepted nondeterminism;
- mismatches and severity;
- manual review decision;
- external pilot impact;
- next action.

## Core Boundary

Core does not run product report regeneration in this phase. Core provides the
checklist and vocabulary; product agents run product-local reproducibility steps
against their own report logic and source handling.
