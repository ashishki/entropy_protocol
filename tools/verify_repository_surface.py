"""Verify root CI routing and bounded maintainer intake."""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    readme = _read("README.md")
    security = _read("SECURITY.md")
    routing = _read("docs/CONTRIBUTION_ROUTING.md")
    readme_normalized = " ".join(readme.split())
    routing_normalized = " ".join(routing.split())
    form_path = ROOT / ".github/ISSUE_TEMPLATE/root-ci-defect.yml"
    config_path = ROOT / ".github/ISSUE_TEMPLATE/config.yml"
    workflow = _read(".github/workflows/trader-risk-audit-ci.yml")
    form = yaml.safe_load(form_path.read_text(encoding="utf-8"))
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    field_ids = [item["id"] for item in form["body"] if "id" in item]
    expected_ids = {
        "confirmations",
        "expected",
        "minimal_fix",
        "observed",
        "owning_path",
        "reproduction",
        "revision",
        "run",
        "workflow",
    }
    if set(field_ids) != expected_ids or len(field_ids) != len(set(field_ids)):
        raise SystemExit("root-CI issue form fields are incomplete or duplicated")
    if config.get("blank_issues_enabled") is not False:
        raise SystemExit("blank issues must remain disabled")

    required_routes = {
        ".github/workflows/ci.yml": "products/entropy-core/",
        ".github/workflows/signal-analytics-sandbox-ci.yml": (
            "products/signal-analytics-sandbox/"
        ),
        ".github/workflows/trader-risk-audit-ci.yml": "products/trader-risk-audit/",
    }
    for active_workflow, product_path in required_routes.items():
        if active_workflow not in routing or product_path not in routing:
            raise SystemExit(
                f"missing routing contract: {active_workflow} -> {product_path}"
            )
        if not (ROOT / active_workflow).is_file() or not (ROOT / product_path).is_dir():
            raise SystemExit(
                f"missing routed surface: {active_workflow} -> {product_path}"
            )

    for marker in (
        "not a single product",
        "no root open-source license",
        "nested product workflow files remain local templates",
    ):
        if marker not in readme_normalized:
            raise SystemExit(f"README boundary missing: {marker}")
    for marker in (
        "not active GitHub Actions checks",
        "generic features",
        "no root open-source license",
    ):
        if marker.casefold() not in routing_normalized.casefold():
            raise SystemExit(f"routing boundary missing: {marker}")
    if "cannot promise a response or remediation deadline" not in security:
        raise SystemExit("security response boundary is missing")

    for action_sha in (
        "actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1",
    ):
        if action_sha not in workflow:
            raise SystemExit(f"workflow action pin missing: {action_sha}")
    for command in (
        "python -m pip check",
        "python tools/verify_repository_surface.py",
        "ruff check products/trader-risk-audit/trader_risk_audit",
        "ruff format --check products/trader-risk-audit/trader_risk_audit",
        "python -m pytest tests -q --tb=short",
    ):
        if command not in workflow:
            raise SystemExit(f"workflow gate missing: {command}")

    print("repository-maintainer-surface: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
