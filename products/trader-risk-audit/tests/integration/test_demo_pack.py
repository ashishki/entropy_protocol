from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.artifacts.manifest import REQUIRED_ARTIFACT_NAMES, hash_file
from trader_risk_audit.cli import main

DEMO_ROOT = Path("demo/risk_audit_case_001")
DEMO_TRADES = DEMO_ROOT / "trades.csv"
DEMO_POLICY = DEMO_ROOT / "policy.yaml"
DEMO_OUTPUT = DEMO_ROOT / "output"
DEMO_REPORT = DEMO_OUTPUT / "report.md"
DEMO_PACKET = DEMO_OUTPUT / "telegram_packet.txt"
DEMO_MANIFEST = DEMO_OUTPUT / "manifest.json"
DEMO_CASE_RU = Path("docs/DEMO_CASE_RU.md")


def test_demo_pack_contains_required_artifacts() -> None:
    for path in (
        DEMO_TRADES,
        DEMO_POLICY,
        DEMO_REPORT,
        DEMO_PACKET,
        DEMO_MANIFEST,
    ):
        assert path.exists()

    manifest = json.loads(DEMO_MANIFEST.read_text(encoding="utf-8"))
    artifact_names = {artifact["name"] for artifact in manifest["artifacts"]}
    assert artifact_names == {*REQUIRED_ARTIFACT_NAMES, "delivery_packet"}
    assert manifest["content_hash"]
    assert all(artifact["sha256"] for artifact in manifest["artifacts"])
    assert "Trader Risk Audit Summary" in DEMO_PACKET.read_text(encoding="utf-8")


def test_demo_pack_regenerates_deterministically(tmp_path: Path) -> None:
    output_dir = tmp_path / "demo_regenerated"

    result = main(
        [
            "audit",
            "--trades",
            str(DEMO_TRADES),
            "--policy",
            str(DEMO_POLICY),
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    assert (output_dir / "report.md").read_text(
        encoding="utf-8"
    ) == DEMO_REPORT.read_text(encoding="utf-8")
    assert (output_dir / "attribution_summary.json").read_text(encoding="utf-8") == (
        DEMO_OUTPUT / "attribution_summary.json"
    ).read_text(encoding="utf-8")

    regenerated_manifest = json.loads(
        (output_dir / "manifest.json").read_text(encoding="utf-8")
    )
    committed_manifest = json.loads(DEMO_MANIFEST.read_text(encoding="utf-8"))
    regenerated_hashes = {
        artifact["name"]: artifact["sha256"]
        for artifact in regenerated_manifest["artifacts"]
    }
    committed_hashes = {
        artifact["name"]: artifact["sha256"]
        for artifact in committed_manifest["artifacts"]
    }
    for artifact_name in REQUIRED_ARTIFACT_NAMES:
        assert regenerated_hashes[artifact_name] == committed_hashes[artifact_name]
    assert hash_file(output_dir / "report.md") == committed_hashes["report_markdown"]


def test_demo_case_contains_synthetic_data_and_claim_boundaries() -> None:
    text = DEMO_CASE_RU.read_text(encoding="utf-8").casefold()

    required_phrases = (
        "синтетическими",
        "не является инвестиционной рекомендацией",
        "не доказывает качество торговой стратегии",
        "не подключается к broker/exchange api",
        "не управляет live orders",
        "не блокирует сделки",
        "не является market validation",
    )
    for phrase in required_phrases:
        assert phrase in text
