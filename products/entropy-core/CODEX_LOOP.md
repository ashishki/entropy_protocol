# Entropy Core Codex Loop

This product is operated by an already-running Codex agent inside tmux window
`entropy-core`.

## Runtime Model

- Codex is started by `/srv/codex-entropy/scripts/start-codex-products.sh`.
- Normal development does not call `codex`.
- Normal development does not call `codex exec`.
- Do not spawn nested Codex or another AI coding process.
- Continue the loop from local files in this product workspace.

Expected runtime:

```bash
codex --sandbox danger-full-access --ask-for-approval never
```

This mode is allowed only because the VPS isolates each product by Unix user,
working copy, and log directory.

## Local Scope

- Product: `entropy-core`
- Product path: `/srv/codex-entropy/repos/product-1/entropy_protocol/products/entropy-core`
- Repository clone: `/srv/codex-entropy/repos/product-1/entropy_protocol`
- Linux user: `codex-entropy-1`
- Branch: `codex/entropy-core-work`

Do not read or modify other product workspaces. They are intentionally isolated
and inaccessible.

## Loop Inputs

At the start of each work segment, read:

1. `RUNBOOK.md`
2. `AGENT_NOTES.md`
3. `PHASE_HANDOFF.md`
4. `CODEX_LOOP.md`
5. `docs/CODEX_PROMPT.md`
6. `docs/tasks.md`

Then continue the product loop:

```text
Fix Queue -> Strategy -> Implement -> Light Review -> phase-boundary Deep Review
-> Archive -> Doc Update -> Phase Report -> checkpoint -> next task
```

## Stop Policy

The only unplanned stop condition is account/model limits until reset.

Planned pauses:

- Human gate: write checkpoint and ask the concrete question.
- Phase boundary: update `AGENT_NOTES.md` and `PHASE_HANDOFF.md`, record
  validation and git status, then optionally restart fresh context in the same
  tmux window.
- Project complete: write final report and stop.
- P0 unresolved after two attempts: checkpoint and wait for operator direction.

## Context Rollover

When context is too heavy or a phase ends:

1. Finish the current coherent change.
2. Update `AGENT_NOTES.md`.
3. Update `PHASE_HANDOFF.md`.
4. Record exact validation commands and git status.
5. Stop or ask operator to run:

```bash
/srv/codex-entropy/scripts/restart-product-codex.sh product-1
```

Fresh context resume instruction:

```text
Continue entropy-core from RUNBOOK.md, AGENT_NOTES.md, PHASE_HANDOFF.md,
CODEX_LOOP.md, docs/CODEX_PROMPT.md, and docs/tasks.md. Do not spawn nested
Codex. Continue the orchestration loop from the next pending task.
```
