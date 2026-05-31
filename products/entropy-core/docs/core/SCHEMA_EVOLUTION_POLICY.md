# Core V2 Schema Evolution Policy

Status: Active policy
Date: 2026-05-29
Scope: Entropy Core internal artifact schemas

This policy defines how Core V2 may evolve internal artifact schemas without
weakening deterministic validation, append-only records, evidence binding, or
restricted-surface guardrails.

## Version Taxonomy

Core schema versions use `name/vMAJOR.MINOR.PATCH` for newly evolved schemas.
Existing Core V1 schema identifiers such as `entropy-core-artifact/v1` remain
valid legacy-major identifiers and are interpreted as `MAJOR=1`, `MINOR=0`,
`PATCH=0` for compatibility review.

| Version part | Allowed when | Compatibility expectation |
|--------------|--------------|---------------------------|
| MAJOR | Required fields are removed, renamed, or retyped; semantics change in a way old validators cannot safely interpret. | Migration required; not backward-compatible by default. |
| MINOR | Optional fields, enum values, or stricter metadata are added while existing valid artifacts remain valid. | Backward-compatible if old required fields and meanings are preserved. |
| PATCH | Clarifications, examples, redaction wording, non-semantic metadata, or validator bug fixes that do not change accepted artifact meaning. | Compatible with the same major and minor version. |

## Compatibility Categories

Every future compatibility check must classify schema pairs into one of these
categories:

- `same_version`: source and target schema identifiers are identical.
- `backward_compatible`: the target can safely validate or interpret existing
  artifacts without changing their meaning.
- `migration_required`: deterministic migration is required before validation
  or interpretation.
- `unsupported_major`: the major version is unknown or intentionally blocked.
- `malformed_version`: the schema identifier cannot be parsed safely.

Compatibility status is not an approval state. It cannot approve external
delivery, production use, holdout access, live execution, or capital movement.

## Change Rules

Major changes require:

- a task contract naming the affected schemas;
- an ADR if runtime, storage, public API, service, language, or protocol
  boundary semantics change;
- deterministic migration design before migrated artifacts can be accepted;
- evidence rows that point to tests, fixtures, and review artifacts.

Minor changes require:

- tests proving existing valid fixtures remain valid;
- fixtures covering the new optional field or enum;
- no change to no-claim, holdout, live, capital, production, or compliance
  approval semantics.

Patch changes require:

- tests or manual evidence proving the change is non-semantic;
- no change to accepted artifact truth, governance state truth, evidence truth,
  or report claim status.

## Migration Record Requirements

Future migration records must be append-only and include:

- `migration_id`;
- `source_schema`;
- `target_schema`;
- `artifact_id`;
- `source_artifact_hash`;
- `target_artifact_hash`;
- `migration_policy_hash`;
- `migration_code_hash`;
- `actor`;
- `created_at`;
- `reason`;
- `compatibility_category`;
- `evidence_refs`;
- `approval_event_ref` when a human-gated boundary is involved.

Corrections are new migration records. Application code must not update or
delete prior migration records.

## Evidence Binding

Before a migrated or compatibility-classified artifact is treated as admissible
Core evidence, the evidence packet must bind:

- source and target schema identifiers;
- source and target artifact hashes;
- migration policy hash;
- migration or compatibility code hash;
- validation result;
- compatibility category;
- referenced tests, fixtures, or review artifacts.

If any required hash or evidence reference is missing, the artifact remains
`needs_manual_review` or `blocked` and must not be promoted as validated
internal evidence.

## Blocked Surfaces

Schema evolution never approves:

- holdout read or unlock;
- OOS/performance conclusions;
- live feeds by default;
- broker/exchange execution;
- order placement or order blocking;
- live capital;
- production credentials;
- production labels;
- capital-ready labels;
- investment advice;
- public SDK;
- hosted service or SaaS;
- auth, SSO, RBAC, or tenant isolation;
- external compliance certification;
- enterprise SLA claims;
- Rust, Go, Java, native extensions, FFI, or a second runtime service.

Any task that needs one of these surfaces must stop for explicit human approval
and any required ADR before implementation.
