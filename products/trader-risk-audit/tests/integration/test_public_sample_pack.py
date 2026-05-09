from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main
from trader_risk_audit.reporting.claim_guard import ensure_report_claims_valid

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "demo" / "public_sample_001"
OUTPUT = PACK / "output"


def test_public_sample_pack_contains_required_inputs_outputs_and_manifest(
    tmp_path: Path,
) -> None:
    expected_files = {
        PACK / "source.md",
        PACK / "trades.csv",
        PACK / "policy.yaml",
        OUTPUT / "normalized_trades.json",
        OUTPUT / "violations.json",
        OUTPUT / "attribution_summary.json",
        OUTPUT / "report.md",
        OUTPUT / "telegram_packet.txt",
        OUTPUT / "manifest.json",
    }
    for path in expected_files:
        assert path.exists(), path

    tmp_output = tmp_path / "public_sample"
    assert (
        main(
            [
                "audit",
                "--trades",
                str(PACK / "trades.csv"),
                "--policy",
                str(PACK / "policy.yaml"),
                "--output-dir",
                str(tmp_output),
            ]
        )
        == 0
    )

    committed_manifest = _load_json(OUTPUT / "manifest.json")
    regenerated_manifest = _load_json(tmp_output / "manifest.json")
    assert committed_manifest["content_hash"] == regenerated_manifest["content_hash"]
    assert _artifact_hashes(committed_manifest) == _artifact_hashes(
        regenerated_manifest
    )


def test_public_sample_report_is_explainable_and_claim_guard_safe() -> None:
    report = (OUTPUT / "report.md").read_text(encoding="utf-8")
    violations = json.loads((OUTPUT / "violations.json").read_text(encoding="utf-8"))

    ensure_report_claims_valid(report)
    assert len({violation["rule_type"] for violation in violations}) >= 3
    assert len(violations) >= 5

    required_report_phrases = (
        "public_sample_hard_max_daily_loss",
        "public_sample_hard_max_drawdown",
        "public_sample_hard_cooldown_after_loss",
        "public_sample_hard_max_position_size",
        "public_sample_hard_forbidden_assets",
        "Source Row IDs",
        "This audit is not investment advice",
    )
    for phrase in required_report_phrases:
        assert phrase in report


def test_public_sample_pack_is_not_marked_as_market_validation() -> None:
    source = _normalized_text(PACK / "source.md")
    evidence = _normalized_text(ROOT / "docs" / "PUBLIC_SAMPLE_EVIDENCE_RU.md")

    for text in (source, evidence):
        assert "internal validation" in text
        assert "demo artifact" in text or "demo artifacts" in text
        assert "qualified prospect call" in text
        assert "paid pilot report" in text
        assert "repeat commitment" in text
        assert "referral" in text
        assert "pmf evidence" in text
        assert "proof that traders will pay" in text

    source_metadata = _metadata((PACK / "source.md").read_text(encoding="utf-8"))
    assert source_metadata["intended_use"] == "internal_validation; demo_only"
    assert "market validation" not in source_metadata["intended_use"]


def test_public_sample_pack_records_starter_profile_context() -> None:
    source = (PACK / "source.md").read_text(encoding="utf-8").casefold()
    evidence = (
        (ROOT / "docs" / "PUBLIC_SAMPLE_EVIDENCE_RU.md")
        .read_text(encoding="utf-8")
        .casefold()
    )
    policy = (PACK / "policy.yaml").read_text(encoding="utf-8").casefold()

    for profile in ("soft", "medium", "hard"):
        assert profile in source
        assert profile in evidence
    assert "starter_profile: hard" in policy
    assert "not investment advice" in source
    assert "not strategy recommendations" in evidence
    assert "not replacements for trader custom rules" in evidence
    assert "objectively best" in evidence


def test_public_sample_pack_keeps_telegram_demo_inside_adr_boundary() -> None:
    packet = (OUTPUT / "telegram_packet.txt").read_text(encoding="utf-8").casefold()
    evidence = _normalized_text(ROOT / "docs" / "PUBLIC_SAMPLE_EVIDENCE_RU.md")

    assert "operator-approved report delivery" in evidence
    assert "adr-001" in evidence
    assert "this audit is not investment advice" in packet
    forbidden_scope = (
        "broker api",
        "signal parsing",
        "order blocking",
        "auto-advice",
        "live trading behavior",
        "credentials",
        "unapproved report delivery",
    )
    for phrase in forbidden_scope:
        assert phrase in evidence


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _normalized_text(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())


def _artifact_hashes(manifest: dict[str, object]) -> dict[str, str]:
    return {
        str(artifact["name"]): str(artifact["sha256"])
        for artifact in manifest["artifacts"]
    }


def _metadata(text: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in text.splitlines():
        key, separator, value = line.partition(":")
        if separator:
            metadata[key.strip()] = value.strip()
    return metadata
