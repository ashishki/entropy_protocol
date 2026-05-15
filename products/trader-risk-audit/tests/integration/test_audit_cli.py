from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main


def test_audit_cli_writes_expected_artifacts(tmp_path: Path) -> None:
    output_dir = tmp_path / "audit"

    result = main(
        [
            "audit",
            "--trades",
            "tests/fixtures/trades/attribution_overlap.csv",
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    expected_files = {
        "normalized_trades.json",
        "violations.json",
        "attribution_summary.json",
        "report.md",
        "telegram_packet.txt",
        "manifest.json",
    }
    assert {path.name for path in output_dir.iterdir()} == expected_files

    manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))
    records = {artifact["name"]: artifact for artifact in manifest["artifacts"]}
    assert set(records) == {
        "source_export",
        "policy_file",
        "normalized_trades",
        "violations",
        "attribution_summary",
        "report_markdown",
        "delivery_packet",
    }
    assert records["report_markdown"]["sha256"]
    assert records["delivery_packet"]["sha256"]
    assert "This audit is not investment advice" in (
        output_dir / "report.md"
    ).read_text(encoding="utf-8")
    assert "Trader Risk Audit Summary" in (
        output_dir / "telegram_packet.txt"
    ).read_text(encoding="utf-8")


def test_audit_cli_blocks_unresolved_policy_review_items(tmp_path: Path) -> None:
    output_dir = tmp_path / "blocked"

    result = main(
        [
            "audit",
            "--trades",
            "tests/fixtures/trades/loss_rule_scenarios.csv",
            "--policy",
            "tests/fixtures/policies/ambiguous_policy.yaml",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result != 0
    assert not (output_dir / "report.md").exists()
    assert not (output_dir / "manifest.json").exists()


def test_audit_cli_repeated_run_has_same_content_hashes(tmp_path: Path) -> None:
    first_output = tmp_path / "first"
    second_output = tmp_path / "second"

    first = _run_audit(first_output)
    second = _run_audit(second_output)

    first_manifest = json.loads(
        (first_output / "manifest.json").read_text(encoding="utf-8")
    )
    second_manifest = json.loads(
        (second_output / "manifest.json").read_text(encoding="utf-8")
    )

    assert first == 0
    assert second == 0
    assert first_manifest["content_hash"] == second_manifest["content_hash"]
    assert _artifact_hashes(first_manifest) == _artifact_hashes(second_manifest)


def _run_audit(output_dir: Path) -> int:
    return main(
        [
            "audit",
            "--trades",
            "tests/fixtures/trades/attribution_overlap.csv",
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--output-dir",
            str(output_dir),
        ]
    )


def _artifact_hashes(manifest: dict[str, object]) -> dict[str, str]:
    return {
        str(artifact["name"]): str(artifact["sha256"])
        for artifact in manifest["artifacts"]
    }
