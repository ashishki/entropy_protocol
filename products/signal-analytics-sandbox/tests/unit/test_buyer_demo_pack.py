from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_buyer_demo_pack_is_internal_only_unless_gate_approves() -> None:
    pack = (PROJECT_ROOT / "docs/pilot/three_channel_BUYER_DEMO_PACK.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Status: internal_only_not_customer_facing",
        "Gate: `approve_internal_only`",
        "must not be sent as a customer-facing report",
        "Decision: `approve_internal_only`",
        "rerun external-ready gate with explicit approval",
    ):
        assert required in pack


def test_buyer_demo_pack_contains_method_limitations_and_talk_track() -> None:
    pack = (PROJECT_ROOT / "docs/pilot/three_channel_BUYER_DEMO_PACK.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "## Included Artifacts",
        "## Methodology Summary",
        "## Buyer Discovery Talk Track",
        "## Open Limitations",
        "170 V2 evaluable text claims",
        "0 reviewed media claims included",
        "Unsupported provider/proxy rows are exclusions",
    ):
        assert required in pack
