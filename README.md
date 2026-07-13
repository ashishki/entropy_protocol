# Entropy Protocol

Entropy Protocol is a research monorepo with three separately owned workspaces:

1. **Entropy Core** - governed evidence and audit primitives.
2. **Trader Risk Audit** - a deterministic post-trade policy-audit case.
3. **Signal Analytics Sandbox** - bounded public-source research experiments.

The repository is not a single product, shared runtime, open-source SDK, or
release unit. Product claims and verification remain scoped to their owning
directories. Trader Risk Audit is being prepared for a history-preserving
standalone publication boundary; this monorepo remains its source lineage until
that separate repository can be created and verified.

See `docs/PROJECT_PLAN.md` for the current roadmap.

The repository still contains product workspaces for governed trading research
and trader discipline workflows.

Current structure:

- `products/entropy-core/` - original governed protocol core, including code,
  tests, migrations, audits, and archives.
- `products/trader-risk-audit/` - deterministic applied policy-audit workspace.
- `products/signal-analytics-sandbox/` - separate signal analytics sandbox.
- `docs/` - global product direction only.

There is no shared root playbook, prompt pool, template pool, hooks directory,
workflow CI template, or Claude settings. Each product workspace owns its own
development materials.

## Repository CI and maintainer intake

GitHub executes only workflows under the repository-root `.github/workflows/`
directory. Root workflows now cover Entropy Core, Signal Analytics Sandbox, and
Trader Risk Audit independently; nested product workflow files remain local
templates and are not claimed as GitHub checks.

Use the [root-CI defect form](https://github.com/ashishki/entropy_protocol/issues/new?template=root-ci-defect.yml)
only for a reproducible failure in one of those root workflows. Read
[contribution routing](docs/CONTRIBUTION_ROUTING.md) before proposing a
product-scoped pull request. Product-behavior issue intake is not currently
offered; blank issues and generic feature/portfolio requests are disabled.
Suspected vulnerabilities follow [SECURITY.md](SECURITY.md), not a public
issue.

This public repository currently has no root open-source license. An issue or
pull request does not grant permission to reuse code across product boundaries.

Start here:

1. `docs/README.md`
2. `docs/PRODUCT_PORTFOLIO.md`
3. `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`
4. `docs/ENTROPY_CORE_AND_GENSYN_REFERENCES.md`
5. `docs/ENTROPY_CORE_PROOF_LAYER_STRATEGY.md`
6. `docs/VPS_COGNITION_VAULT.md` for the VPS-local Obsidian vault pointer.
7. `docs/CONTRIBUTION_ROUTING.md` for root-CI and product ownership boundaries.
