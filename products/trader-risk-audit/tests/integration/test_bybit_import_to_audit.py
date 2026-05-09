from __future__ import annotations

import csv
import json
from pathlib import Path

from trader_risk_audit.cli import main

BYBIT_FIXTURE = "tests/fixtures/exchange/bybit/executions.json"


def test_bybit_import_feeds_audit(tmp_path: Path) -> None:
    import_dir = tmp_path / "exchange_import"
    audit_dir = tmp_path / "audit"
    policy_path = _write_bybit_policy(tmp_path)

    import_result = _run_bybit_import(import_dir)
    audit_result = _run_audit(import_dir, audit_dir, policy_path)

    assert import_result == 0
    assert audit_result == 0
    assert (import_dir / "raw_snapshot.json").exists()
    assert (import_dir / "normalized_trades.csv").exists()
    assert (import_dir / "import_manifest.json").exists()
    assert (audit_dir / "report.md").exists()
    assert (audit_dir / "manifest.json").exists()


def test_bybit_import_to_audit_is_deterministic(tmp_path: Path) -> None:
    first_import = tmp_path / "first_import"
    second_import = tmp_path / "second_import"
    first_audit = tmp_path / "first_audit"
    second_audit = tmp_path / "second_audit"
    policy_path = _write_bybit_policy(tmp_path)

    assert _run_bybit_import(first_import) == 0
    assert _run_bybit_import(second_import) == 0
    assert _run_audit(first_import, first_audit, policy_path) == 0
    assert _run_audit(second_import, second_audit, policy_path) == 0

    first_import_manifest = _load_json(first_import / "import_manifest.json")
    second_import_manifest = _load_json(second_import / "import_manifest.json")
    first_audit_manifest = _load_json(first_audit / "manifest.json")
    second_audit_manifest = _load_json(second_audit / "manifest.json")

    assert (
        first_import_manifest["content_hash"] == second_import_manifest["content_hash"]
    )
    assert first_audit_manifest["content_hash"] == second_audit_manifest["content_hash"]
    assert (first_import / "normalized_trades.csv").read_text(encoding="utf-8") == (
        second_import / "normalized_trades.csv"
    ).read_text(encoding="utf-8")
    assert (first_audit / "report.md").read_text(encoding="utf-8") == (
        second_audit / "report.md"
    ).read_text(encoding="utf-8")


def test_bybit_audit_preserves_safe_traceability(tmp_path: Path) -> None:
    import_dir = tmp_path / "exchange_import"
    audit_dir = tmp_path / "audit"
    policy_path = _write_bybit_policy(tmp_path)

    assert _run_bybit_import(import_dir) == 0
    assert _run_audit(import_dir, audit_dir, policy_path) == 0

    normalized_rows = tuple(
        csv.DictReader((import_dir / "normalized_trades.csv").open(encoding="utf-8"))
    )
    report = (audit_dir / "report.md").read_text(encoding="utf-8")
    manifest = (audit_dir / "manifest.json").read_text(encoding="utf-8")

    assert [row["row_id"] for row in normalized_rows] == [
        "bybit_exec_synthetic_exec_bybit_001",
        "bybit_exec_synthetic_exec_bybit_002",
    ]
    assert "bybit_exec_synthetic_exec_bybit_001" in report
    assert "bybit_exec_synthetic_exec_bybit_002" in report
    for forbidden in ("api_key", "api_secret", "signature"):
        assert forbidden not in report
        assert forbidden not in manifest


def _run_bybit_import(output_dir: Path) -> int:
    return main(
        [
            "exchange-import",
            "fixture",
            "--snapshot",
            BYBIT_FIXTURE,
            "--output-dir",
            str(output_dir),
        ]
    )


def _run_audit(import_dir: Path, audit_dir: Path, policy_path: Path) -> int:
    return main(
        [
            "audit",
            "--trades",
            str(import_dir / "normalized_trades.csv"),
            "--policy",
            str(policy_path),
            "--output-dir",
            str(audit_dir),
        ]
    )


def _write_bybit_policy(tmp_path: Path) -> Path:
    policy_path = tmp_path / "bybit_policy.yaml"
    policy_path.write_text(
        "\n".join(
            (
                'schema_version: "1"',
                "account_scope:",
                "  - bybit_read_only_import",
                "timezone: UTC",
                "session:",
                '  start: "00:00"',
                '  end: "23:59"',
                "rules:",
                "  - rule_id: rule_forbidden_bybit_symbol",
                "    type: forbidden_assets",
                "    threshold: null",
                "    unit: symbol",
                "    params:",
                "      symbols:",
                "        - BTCUSDT",
                "",
            )
        ),
        encoding="utf-8",
    )
    return policy_path


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))
