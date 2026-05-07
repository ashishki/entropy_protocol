# RUNBOOK

Stack:
- Python package under `src/entropy`.
- `pyproject.toml` declares Python `>=3.12`.
- Runtime and dev dependencies are declared in `pyproject.toml`.

Environment:
- Product-local `.venv` should use Python 3.12.
- Setup uses `uv` when system `python3.12` is unavailable.
- If `.venv/bin/python` already exists, do not recreate it during routine work.

Setup commands if `.venv` is missing:

```bash
uv venv --python 3.12 .venv
uv pip install -e ".[dev]" --python .venv/bin/python
```

Validation commands:

```bash
.venv/bin/python -m pytest -q tests/
.venv/bin/python -m ruff check src/entropy tests
.venv/bin/python -m pyright src/entropy
.venv/bin/entropy --help
```

Development loop:
- Read `CODEX_LOOP.md` before using older playbook/orchestrator instructions.
- Do not use `codex exec` for the normal loop.
- Do not spawn nested Codex.
- Do not touch other products.
