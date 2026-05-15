from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.artifacts.manifest import build_audit_manifest
from trader_risk_audit.exchange.credentials import (
    ExchangeCredentials,
    build_exchange_import_safe_metadata,
    inspect_exchange_permissions,
)
from trader_risk_audit.pilot_queue import PilotQueue
from trader_risk_audit.workspace import build_workspace_metadata


def test_exchange_import_does_not_persist_secrets(tmp_path: Path) -> None:
    raw_values = (
        "fixture_api_key_123",
        "fixture_api_secret_456",
        "fixture_signature_789",
        "fixture_account_id_999",
    )
    credentials = ExchangeCredentials(
        exchange="bybit",
        api_key=raw_values[0],
        api_secret=raw_values[1],
        account_id=raw_values[3],
    )
    safe_metadata = build_exchange_import_safe_metadata(
        credentials=credentials,
        permission_review=inspect_exchange_permissions(
            exchange="bybit",
            read_only=True,
            permissions={},
        ),
    )

    workspace_metadata = build_workspace_metadata(
        audit_id="audit_exchange_safe",
        file_references={
            "exchange_credentials": json.dumps(safe_metadata, sort_keys=True),
            "exchange_signature": "<redacted>",
        },
    )
    queue_file = tmp_path / "queue.json"
    PilotQueue(queue_file).upsert_request(
        "audit_exchange_safe",
        file_references={
            "exchange_credentials": json.dumps(safe_metadata, sort_keys=True),
            "exchange_signature": "<redacted>",
        },
    )

    report = tmp_path / "report.md"
    report.write_text(
        "# Trader Risk Audit\n\nExchange import permission: approved_read_only\n",
        encoding="utf-8",
    )
    source_export = _write(tmp_path / "source.json", '{"rows": []}\n')
    policy_file = _write(tmp_path / "policy.yaml", "schema_version: 1\nrules: []\n")
    normalized_trades = _write(tmp_path / "normalized.csv", "timestamp,symbol\n")
    violations = _write(tmp_path / "violations.json", "[]\n")
    attribution = _write(tmp_path / "attribution.json", "{}\n")
    manifest = build_audit_manifest(
        source_export=source_export,
        policy_file=policy_file,
        normalized_trades=normalized_trades,
        violations=violations,
        attribution_summary=attribution,
        report_markdown=report,
        command="trader-risk-audit exchange-import bybit",
        command_arguments=(
            "--credential-profile",
            "local-env",
            "--signature",
            "<redacted>",
        ),
        generated_at="2026-05-09T00:00:00+00:00",
    )

    persisted = "\n".join(
        (
            workspace_metadata.to_json(),
            queue_file.read_text(encoding="utf-8"),
            manifest.to_json(),
            report.read_text(encoding="utf-8"),
        )
    )

    for raw_value in raw_values:
        assert raw_value not in persisted
    assert "approved_read_only" in persisted
    assert "api_key_fingerprint" in persisted


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path
