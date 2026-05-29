# Product Workspaces

This directory separates product workspaces from the root Entropy Protocol
portfolio documents.

| Workspace | Path | Role |
|---|---|---|
| Entropy Core | `products/entropy-core/` | Protocol-safe core primitives and bridges |
| Trader Risk Audit | `products/trader-risk-audit/` | Primary commercial MVP |
| Signal Analytics Sandbox | `products/signal-analytics-sandbox/` | Separate validation sandbox |

Current active focus as of 2026-05-15:

- Trader Risk Audit: `docs/OPEN_SOURCE_AUDIT_VALIDATION_ROADMAP.md`
- Signal Analytics Sandbox: `docs/DEEP_CHANNEL_RETROSPECTIVE_ROADMAP.md`
- Entropy Core: paused after Core V1 checkpoint pending human-approved Core V2

Read first:

1. `docs/PRODUCT_PORTFOLIO.md`
2. `docs/ARTIFACT_FIRST_VALIDATION_ROADMAP.md`
3. `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`
4. The target workspace `README.md`
5. The target workspace `docs/CODEX_PROMPT.md`
6. The target workspace artifact roadmap when present
7. The target workspace `docs/tasks.md`

Product workspace docs are subordinate to Entropy Core canonical protocol
documents where core protocol behavior is involved.

Workspace code, tests, migrations, local env templates, and product docs should
stay inside the owning product directory. The repository root is reserved for
global direction and repo-level orchestration.

Each product workspace also owns its local AI workflow pool:

- `PLAYBOOK.md`
- `prompts/`
- `templates/`
- `hooks/`
- `ci/ci.yml`
- `.claude/settings.json`
- `.claude/commands/bootstrap-new.md`
