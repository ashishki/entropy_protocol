Read `docs/prompts/ORCHESTRATOR.md` in full, then execute it exactly as written, starting from Step 0.

Before starting Step 0, replace the literal string `{{PROJECT_ROOT}}` in your working context with the absolute path of the current working directory (run `pwd` to get it).

Project-specific note: this project has a Phase 0 gate (SAS-001 + SAS-002). Before dispatching any T01–T20 task, the orchestrator must verify both rows in `docs/CODEX_PROMPT.md §Phase 0 Gate Status` are marked `acknowledged`. If either row is `pending`, stop and report the blocker; do not run any engineering task.
