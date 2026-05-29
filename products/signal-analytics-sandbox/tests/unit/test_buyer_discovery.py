from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_buyer_discovery_lists_10_to_20_profiles_and_use_cases() -> None:
    plan = (PROJECT_ROOT / "docs/pilot/BUYER_DISCOVERY.md").read_text(encoding="utf-8")

    profile_ids = [f"B{number:02d}" for number in range(1, 16)]
    for profile_id in profile_ids:
        assert f"| {profile_id} |" in plan

    assert "| B16 |" not in plan
    assert "Likely pilot use case" in plan
    assert "Validation signal" in plan


def test_buyer_discovery_keeps_external_boundary_and_disqualifiers() -> None:
    plan = (PROJECT_ROOT / "docs/pilot/BUYER_DISCOVERY.md").read_text(encoding="utf-8")

    for required in (
        "Gate: `approve_internal_only`",
        "not a sales deck",
        "Buyer wants live trading alerts, copy trading, or advice.",
        "Buyer wants a public channel ordering without review/gate approval.",
        "Buyer cannot provide public/operator-authorized sources.",
    ):
        assert required in plan
