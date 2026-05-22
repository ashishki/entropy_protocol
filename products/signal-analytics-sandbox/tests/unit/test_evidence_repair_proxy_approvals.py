from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_bablos79_proxy_approvals_cover_position_candidates() -> None:
    approvals = (
        PROJECT_ROOT / "docs/pilot/bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md"
    ).read_text(encoding="utf-8")

    expected_capture_ids = {
        "bablos79-10008",
        "bablos79-10009",
        "bablos79-10122",
        "bablos79-10162",
        "bablos79-10219",
        "bablos79-10277",
        "bablos79-10339",
        "bablos79-10391",
        "bablos79-10526",
        "bablos79-10576",
    }

    for capture_id in expected_capture_ids:
        assert f"`{capture_id}`" in approvals

    assert approvals.count("approved_for_proxy_mapping") >= 9
    assert "| `bablos79-10576` |" in approvals
    assert "rejected_as_context" in approvals


def test_bablos79_proxy_approvals_define_provider_horizon_and_method() -> None:
    approvals = (
        PROJECT_ROOT / "docs/pilot/bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md"
    ).read_text(encoding="utf-8")

    assert "Primary horizon | `7d` directional return" in approvals
    assert "Timestamp basis | Public Telegram post timestamp" in approvals
    assert "MOEX ISS candles" in approvals
    assert "asset-level directional return" in approvals
    assert "Open/public provider windows only" in approvals


def test_bablos79_proxy_approvals_block_unapproved_fetches_and_external_use() -> None:
    approvals = (
        PROJECT_ROOT / "docs/pilot/bablos79_EVIDENCE_REPAIR_PROXY_APPROVALS.md"
    ).read_text(encoding="utf-8")

    assert "do_not_fetch" in approvals
    assert "External posture | Internal V1 research only" in approvals
    assert "External delivery still requires a V1 external-ready gate" in approvals
    assert "No human/operator external acceptance yet" in approvals
