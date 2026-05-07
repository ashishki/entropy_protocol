"""Reset baseline smoke tests."""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path

from typer.testing import CliRunner

from entropy import cli
from entropy.metrics import increment_counter, record_histogram


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src" / "entropy"


def _python_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.py") if path.is_file())


def test_shared_tracing_boundary() -> None:
    """Span-creating code uses the shared tracing module only."""
    offenders: list[str] = []

    for path in _python_files(SRC_ROOT):
        tree = ast.parse(path.read_text(), filename=str(path))
        imports_shared_tracer = False
        imports_otel_tracer_factory = False
        creates_span = False

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module == "entropy.tracing":
                    imports_shared_tracer = any(alias.name == "get_tracer" for alias in node.names)
                if node.module == "opentelemetry.trace":
                    imports_otel_tracer_factory = any(
                        alias.name == "get_tracer" for alias in node.names
                    )
            elif isinstance(node, ast.Call):
                function = node.func
                if isinstance(function, ast.Attribute) and function.attr in {
                    "start_as_current_span",
                    "start_span",
                }:
                    creates_span = True
                elif isinstance(function, ast.Name) and function.id == "get_tracer":
                    if path.name != "tracing.py" and not imports_shared_tracer:
                        offenders.append(str(path.relative_to(PROJECT_ROOT)))

        if imports_otel_tracer_factory and path.name != "tracing.py":
            offenders.append(str(path.relative_to(PROJECT_ROOT)))
        if creates_span and path.name != "tracing.py" and not imports_shared_tracer:
            offenders.append(str(path.relative_to(PROJECT_ROOT)))

    assert offenders == []


def test_metrics_stubs_are_callable() -> None:
    """Metrics stubs stay safe to call before metrics backend activation."""
    assert increment_counter("reset.smoke", attributes={"scope": "test"}) is None
    assert record_histogram("reset.smoke.duration", 1.0, attributes={"scope": "test"}) is None


def test_cli_health_smoke(monkeypatch) -> None:
    """The local health command returns machine-readable status."""
    monkeypatch.setattr(cli, "check_postgres", lambda: {"name": "postgres", "status": "ok"})
    monkeypatch.setattr(cli, "check_duckdb", lambda: {"name": "duckdb", "status": "ok"})

    result = CliRunner().invoke(cli.app, ["health"])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == {"status": "ok"}


def test_codex_prompt_records_reset_baseline() -> None:
    """The active loop state records the latest reset pytest baseline."""
    prompt_text = (PROJECT_ROOT / "docs" / "CODEX_PROMPT.md").read_text()

    assert re.search(r"Baseline: \d+ passing tests, 20 skipped", prompt_text)
    assert re.search(r"pytest -q tests/` reported `\d+ passed, 20 skipped`", prompt_text)


def test_legacy_context_is_scoped() -> None:
    """Active task instructions do not point at the old workflow archive."""
    tasks_text = (PROJECT_ROOT / "docs" / "tasks.md").read_text()

    assert "docs/legacy/old-workflow/2026-05-07" not in tasks_text
    assert "docs/legacy/" in tasks_text
    assert "Context-Refs:" in tasks_text
