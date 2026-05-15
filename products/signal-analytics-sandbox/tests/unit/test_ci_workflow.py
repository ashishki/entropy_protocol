from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = PROJECT_ROOT.parents[1]


def test_workflow_triggers_and_python_version() -> None:
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "ci.yml").read_text()

    assert "push:" in workflow
    assert "pull_request:" in workflow
    assert 'branches: ["master", "main"]' in workflow
    assert 'python-version: "3.12"' in workflow
    assert 'cache: "pip"' in workflow


def test_workflow_step_order() -> None:
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "ci.yml").read_text()
    expected_steps = [
        "run: ruff check src/ tests/",
        "run: ruff format --check src/ tests/",
        "run: pyright",
        "run: python -m pytest tests/ -q --tb=short",
    ]

    positions = [workflow.index(step) for step in expected_steps]

    assert positions == sorted(positions)


def test_dev_deps_listed() -> None:
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "ci.yml").read_text()
    requirements_dev = (PROJECT_ROOT / "requirements-dev.txt").read_text()

    assert "pip install -r requirements-dev.txt -e ." in workflow
    for dependency in ("ruff", "pyright", "pytest", "pytest-cov"):
        assert dependency in requirements_dev


def test_repo_root_workflow_delegates_to_product() -> None:
    workflow = (
        REPO_ROOT / ".github" / "workflows" / "signal-analytics-sandbox-ci.yml"
    ).read_text()

    assert "working-directory: products/signal-analytics-sandbox" in workflow
    assert "pip install -r requirements-dev.txt -e ." in workflow
    assert "ruff check src/ tests/" in workflow
    assert "ruff format --check src/ tests/" in workflow
    assert "pyright" in workflow
    assert "python -m pytest tests/ -q --tb=short" in workflow
