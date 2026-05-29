# Entropy Protocol

Entropy Protocol is now organized around two related lines:

1. **Entropy Core** - a verification and responsibility kernel for AI actions,
   decisions, evidence chains, and referee verdicts.
2. **Telegram Trader Intelligence** - an applied product line for analyzing
   Telegram trader channels, claims, narratives, source behavior, and risk
   signals.

See `docs/PROJECT_PLAN.md` for the current roadmap.

The repository still contains product workspaces for governed trading research
and trader discipline workflows.

Current structure:

- `products/entropy-core/` - original governed protocol core, including code,
  tests, migrations, audits, and archives.
- `products/trader-risk-audit/` - primary commercial MVP.
- `products/signal-analytics-sandbox/` - separate signal analytics sandbox.
- `docs/` - global product direction only.

There is no shared root playbook, prompt pool, template pool, hooks directory,
workflow CI template, or Claude settings. Each product workspace owns its own
development materials.

Start here:

1. `docs/README.md`
2. `docs/PRODUCT_PORTFOLIO.md`
3. `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`
4. `docs/ENTROPY_CORE_AND_GENSYN_REFERENCES.md`
5. `docs/VPS_COGNITION_VAULT.md` for the VPS-local Obsidian vault pointer.
