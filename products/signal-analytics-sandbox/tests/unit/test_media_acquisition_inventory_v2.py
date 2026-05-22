from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_media_inventory_v2_records_refs_blockers_checksums_and_review_status() -> None:
    inventory = (
        PROJECT_ROOT / "docs/pilot/three_channel_V2_MEDIA_INVENTORY.md"
    ).read_text(encoding="utf-8")

    for required in (
        "## Inventory Rows",
        "SHA-256",
        "blocker",
        "review status",
        "`dc35f04c417d644b603c9336d96108d485682e467e88e1e476500b1add1e115c`",
        "`87ae688d3e55e4ab0eed95c2e4ec3d6ec3aa8a8022acc37a70703b255d6e8b00`",
        "not_acquired_no_checksum",
        "llm_reviewed_internal",
        "pending_operator_linkage",
        "not_acquired",
    ):
        assert required in inventory


def test_media_inventory_v2_covers_each_pilot_channel_and_blocks_customer_use() -> None:
    inventory = (
        PROJECT_ROOT / "docs/pilot/three_channel_V2_MEDIA_INVENTORY.md"
    ).read_text(encoding="utf-8")

    for channel in ("`bablos79`", "`nemphiscrypts`", "`pifagortrade`"):
        assert channel in inventory

    for required in (
        "Transcript human review",
        "Operator linkage needed",
        "Media acquisition needed",
        "No V2 media-backed claim is customer-facing eligible.",
        "Customer-facing media-backed claims require human/operator acceptance",
    ):
        assert required in inventory
