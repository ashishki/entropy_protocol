# Entropy Core V1 Operator Runbook

Status: Internal operator guide
Date: 2026-05-14

Run commands from `products/entropy-core/`.

## Environment

Use local scratch directories for registry and reproducibility state:

```bash
export ENTROPY_REGISTRY_DIR=/tmp/entropy-core-registry
export ENTROPY_REPRODUCIBILITY_MANIFEST_DIR=/tmp/entropy-core-reproducibility/manifests
```

## Generic Artifact

Validate a synthetic generic artifact:

```bash
.venv/bin/entropy artifact validate tests/fixtures/artifacts/valid_artifact.json
```

Register it in the local append-only registry:

```bash
.venv/bin/entropy artifact register tests/fixtures/artifacts/valid_artifact.json
.venv/bin/entropy artifact list
```

Inspect registry history after registration:

```bash
.venv/bin/entropy artifact history artifact-bf2e9ce008e7c16d
```

## Research-Shaped Artifact

Convert the synthetic research fixture to the base artifact contract, then
validate it:

```bash
.venv/bin/python - <<'PY'
import json
from pathlib import Path
from entropy.artifacts import ResearchArtifact

source = Path("tests/fixtures/artifacts/research/valid_research_artifact.json")
target = Path("/tmp/entropy-core-research-artifact.json")
artifact = ResearchArtifact.model_validate(json.loads(source.read_text()))
target.write_text(artifact.to_artifact_contract().model_dump_json(indent=2), encoding="utf-8")
print(target)
PY
.venv/bin/entropy artifact validate /tmp/entropy-core-research-artifact.json
```

## Product-Shaped Artifacts

Validate synthetic product-shaped fixtures through Core bridge profiles:

```bash
.venv/bin/entropy artifact validate \
  tests/fixtures/artifacts/profiles/trader_valid.json \
  --profile trader-risk-audit

.venv/bin/entropy artifact validate \
  tests/fixtures/artifacts/profiles/signal_valid.json \
  --profile signal-analytics-sandbox
```

Profile validation remains Core-only. It does not run product report logic and
does not edit product workspaces.

## CAF-Shaped Artifact

Convert the synthetic CAF allocation decision fixture to the base artifact
contract, then validate it:

```bash
.venv/bin/python - <<'PY'
import json
from pathlib import Path
from entropy.artifacts import AllocationDecisionArtifact

source = Path("tests/fixtures/artifacts/caf/valid_allocation_decision.json")
target = Path("/tmp/entropy-core-caf-artifact.json")
artifact = AllocationDecisionArtifact.model_validate(json.loads(source.read_text()))
target.write_text(artifact.to_artifact_contract().model_dump_json(indent=2), encoding="utf-8")
print(target)
PY
.venv/bin/entropy artifact validate /tmp/entropy-core-caf-artifact.json
```

## Evidence And Governance

Build an evidence packet for a registered artifact:

```bash
.venv/bin/entropy evidence build artifact-bf2e9ce008e7c16d
```

Inspect a generated evidence packet:

```bash
.venv/bin/entropy evidence inspect docs/audit/generated/evidence/artifact-bf2e9ce008e7c16d.json
```

Record a local governance transition:

```bash
.venv/bin/entropy governance transition artifact-bf2e9ce008e7c16d validated_internal --reason "synthetic internal validation"
.venv/bin/entropy governance history artifact-bf2e9ce008e7c16d
```

## Failure Handling

Invalid artifacts exit non-zero and emit redacted validation errors:

```bash
.venv/bin/entropy artifact validate tests/fixtures/artifacts/invalid_artifact.json
```

Unsafe research, product-profile, and CAF fixtures are expected to fail:

```bash
.venv/bin/entropy artifact validate tests/fixtures/artifacts/profiles/trader_unsafe_claim.json --profile trader-risk-audit
```

Do not override failed validation by editing registry state. Fix the artifact or
record a new corrected artifact.

## Blocked Surfaces

The runbook does not approve:

- holdout read or unlock;
- live feeds by default;
- broker/exchange execution;
- order placement or order blocking;
- live capital;
- production credentials;
- investment advice;
- OOS/performance conclusions;
- public SDK;
- hosted service;
- external compliance certification.
