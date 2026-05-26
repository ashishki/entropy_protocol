# Cognition Manifest - Entropy Protocol

---
artifact_kind: retrieval_manifest
project: entropy-protocol
source_repo: Entropy_Protocol
status: active
canonical: false
generated: false
tags: [portfolio, cognition, ai-workflow-playbook]
---

Version: 1.0
Last updated: 2026-05-25

## Purpose

This file maps cross-product operational memory for the Entropy Protocol portfolio. The product workspaces remain authoritative; this root manifest is a retrieval surface for portfolio-level orientation.

## Authority Rules

- Product repos/directories remain source of truth.
- Obsidian, generated indexes, and context packets are optional navigation layers.
- Cross-product pattern notes must cite product-local artifacts before influencing implementation.

## Project Identity

| Field | Value |
|-------|-------|
| Primary shape | Portfolio of governed product workspaces |
| Governance level | Mixed by product |
| Runtime tier | Mixed by product |
| Active profiles | Product-specific; root has no runtime profile |

## Canonical Truth

| Surface | Path | Notes |
|---------|------|-------|
| Portfolio overview | `docs/PRODUCT_PORTFOLIO.md` | Root product map |
| Development operating model | `docs/AI_DEVELOPMENT_OPERATING_MODEL.md` | Cross-product workflow stance |
| Entropy core | `products/entropy-core/` | Governed protocol core |
| Trader risk audit | `products/trader-risk-audit/` | Commercial MVP workspace |
| Signal analytics sandbox | `products/signal-analytics-sandbox/` | Signal/evidence sandbox |

## Retrieval Scopes

| Scope | Start here | Include next |
|-------|------------|--------------|
| Portfolio strategy | `docs/PRODUCT_PORTFOLIO.md` | product readmes, operating model |
| Product implementation | product-local `docs/ARCHITECTURE.md` or `README.md` | product tasks, evals, ADRs, audits |
| Cross-product evidence | product-local evidence/eval docs | demos, audit reports, product ADRs |
| Pattern reuse | product-local ADR/eval pairs | cross-project pattern notes only after citation |

## Local/VPS Agent Context Workflow

Agents do not automatically discover the cognition vault. The operator or orchestrator must pass a repo-local manifest, vault project map, or generated context packet path into the agent task.

Expected sibling layout on any machine that runs agents:

```text
ai-stack/
|-- projects/<repo>/
`-- engineering-cognition-vault/
```

Local project work:

```bash
cd ai-stack/engineering-cognition-vault
./scripts/sync_from_projects.sh --no-pull --commit --push
```

VPS project work:

1. Commit and push code, docs, evals, ADRs, findings, or postmortems in this repo.
2. Refresh the vault on the machine that owns vault sync:

```bash
cd ai-stack/engineering-cognition-vault
git pull --ff-only
./scripts/sync_from_projects.sh --commit --push
```

If an agent runs on the VPS, clone the vault next to `projects/` and pass packet paths explicitly:

```text
../engineering-cognition-vault/10-projects/<project>.md
../engineering-cognition-vault/90-context-packets/<role>-<project>-<scope>.md
```

Do not write canonical decisions, eval results, or findings directly into the vault. Write them into this repo first, then regenerate the vault.

---

## Known Gaps

| Gap | Impact | Migration step |
|-----|--------|----------------|
| No root canonical playbook or task state | Root should not be treated as an implementation workspace | Keep root manifest as portfolio map only |
| Product-level cognition manifests are not standardized | Cross-product retrieval requires manual path knowledge | Add product-local manifests when each product has active work |
| Cross-product pattern notes do not exist yet | Reuse lessons stay buried in product docs | Create vault pattern notes after linking at least two product artifacts |

## Generated Artifacts

| Artifact | Path | Policy |
|----------|------|--------|
| Root cognition index | `generated/cognition/index.json` | Optional generated manifest |
| Product context packets | product-local `docs/context-packets/` | Commit only for major reviews or regressions |

