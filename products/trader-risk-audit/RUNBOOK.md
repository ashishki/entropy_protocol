# RUNBOOK

Stack:
- Python 3.12 local CLI package.
- Dependency management uses pip requirements files plus editable install.

Prerequisite:
- Product-local `.venv` exists and uses Python 3.12.

Detected files:
- README.md: yes
- pyproject.toml: yes
- requirements.txt: yes
- requirements-dev.txt: yes
- package.json: no
- docker-compose.yml: no
- Makefile: no
- .env.example: yes

Setup commands:
- `.venv/bin/python --version`
- `uv pip install -r requirements-dev.txt -e . --python .venv/bin/python`

Test commands:
- `.venv/bin/python -m pytest tests -q --tb=short`

Lint and format commands:
- `.venv/bin/python -m ruff check trader_risk_audit tests`
- `.venv/bin/python -m ruff format --check trader_risk_audit tests`

Build commands:
- No explicit build command is defined by project files.

Dev server or CLI:
- `.venv/bin/python -m trader_risk_audit --help`
- `.venv/bin/python -m trader_risk_audit --version`

Manual check required:
- Keep work inside this product directory unless a root-level portfolio document explicitly needs an update.
