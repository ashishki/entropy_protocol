# VPS Cognition Vault Pointer

Status: active VPS-local pointer
Date: 2026-05-26

## Canonical VPS Location

On this VPS, the Obsidian cognition vault is cloned here:

```text
/srv/codex-entropy/repos/product-3/engineering-cognition-vault
```

The Entropy Protocol monorepo is here:

```text
/srv/codex-entropy/repos/product-3/entropy_protocol
```

The vault should stay outside product repositories. Product repositories remain
the source of truth; the vault is a navigation, retrieval, and context-packet
layer.

## Compatibility Layout

Vault sync scripts expect this stack layout:

```text
<stack-root>/
|-- engineering-cognition-vault/
`-- projects/Entropy_Protocol/
```

This VPS uses a local compatibility symlink:

```text
/srv/codex-entropy/repos/product-3/projects/Entropy_Protocol
  -> ../entropy_protocol
```

Do not commit this symlink into the Entropy Protocol repository. It is local VPS
infrastructure.

## Agent Pointer

When starting or resuming a product agent, pass these paths explicitly if
cross-product context is needed:

```text
/srv/codex-entropy/repos/product-3/engineering-cognition-vault/10-projects/entropy-protocol.md
/srv/codex-entropy/repos/product-3/engineering-cognition-vault/90-context-packets/
```

Use vault notes only as supporting context. If a vault note conflicts with a
repo artifact, the repo artifact wins.

## Freshness Check

Before using vault context for Entropy Protocol work:

```bash
cd /srv/codex-entropy/repos/product-3/engineering-cognition-vault
git pull --ff-only
./scripts/ensure_fresh_for_project.sh entropy-protocol --no-pull --no-packets
```

To refresh and publish generated vault context after committing product changes:

```bash
cd /srv/codex-entropy/repos/product-3/engineering-cognition-vault
./scripts/sync_from_projects.sh --project entropy-protocol --no-pull --commit --push
```

## Authority Rule

Write canonical decisions, eval results, findings, implementation journals, and
task state into product repositories first. Regenerate or update the vault
afterward.
