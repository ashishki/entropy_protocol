# Entropy Protocol

Entropy Protocol is a product portfolio for governed trading research and trader
discipline workflows.

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
