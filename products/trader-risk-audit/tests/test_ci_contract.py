def _read_workflow() -> str:
    with open(".github/workflows/ci.yml", encoding="utf-8") as workflow:
        return workflow.read()


WORKFLOW_TEXT = _read_workflow()


def test_ci_uses_python_312_and_editable_install() -> None:
    assert 'python-version: "3.12"' in WORKFLOW_TEXT
    assert "pip install -r requirements-dev.txt -e ." in WORKFLOW_TEXT


def test_ci_has_lint_format_and_pytest_steps() -> None:
    assert "ruff check trader_risk_audit tests" in WORKFLOW_TEXT
    assert "ruff format --check trader_risk_audit tests" in WORKFLOW_TEXT
    assert "python -m pytest tests -q --tb=short" in WORKFLOW_TEXT


def test_ci_has_no_runtime_external_credentials() -> None:
    forbidden_credential_names = {
        "API_KEY",
        "BROKER_TOKEN",
        "BROKER_SECRET",
        "EXCHANGE_TOKEN",
        "EXCHANGE_SECRET",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
    }

    for credential_name in forbidden_credential_names:
        assert credential_name not in WORKFLOW_TEXT
