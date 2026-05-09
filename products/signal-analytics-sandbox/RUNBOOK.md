# RUNBOOK

Stack:
- Documentation and product-planning workspace.
- No implementation package manager was detected.

Detected files:
- README.md: yes
- pyproject.toml: no
- requirements.txt: no
- package.json: no
- docker-compose.yml: no
- Makefile: no
- .env.example: yes

Test commands:
- `cd products/signal-analytics-sandbox && .venv/bin/python -m unittest discover -s tests -v`

Build commands:
- No explicit build command is defined by project files.

Dev server or CLI:
- No dev server or CLI command is defined by project files.

Environment:
- Product-local `.venv` exists and uses Python 3.12.
- No dependencies are installed automatically because this product does not
  currently define `pyproject.toml`, `requirements.txt`, or another dependency
  manifest.

Manual check required:
- Engineering Phase 1 remains blocked until `docs/CODEX_PROMPT.md §Phase 0 Gate Status` marks SAS-001 and SAS-002 as `acknowledged`.
- Keep work inside this product directory unless a root-level portfolio document explicitly needs an update.
