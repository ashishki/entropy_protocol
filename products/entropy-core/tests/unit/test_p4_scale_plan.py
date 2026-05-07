"""Unit tests for P4 scaled collection planning."""

from __future__ import annotations

from entropy.evidence.crypto_universe import (
    get_default_phase0_crypto_universe,
    get_default_phase0_p4_crypto_universe,
)
from entropy.evidence.p4_scale_plan import (
    P4_REVISED_SCALE_PLAN_ID,
    P4_SCALE_PLAN_ID,
    batch_items,
    build_p4_scale_plan,
    first_batch,
    pending_count,
    plan_manifest_payload,
    render_p4_scale_plan,
)


def test_p4_scale_plan_builds_36_month_by_20_asset_matrix() -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe())

    assert plan.plan_id == P4_SCALE_PLAN_ID
    assert plan.asset_count == 20
    assert plan.month_count == 36
    assert plan.download_count == 720
    assert plan.gate_claim_allowed is False
    assert plan.download_items[0].symbol == "BTCUSDT"
    assert plan.download_items[0].year == 2023
    assert plan.download_items[0].month == 1
    assert plan.download_items[-1].symbol == "ALGOUSDT"
    assert plan.download_items[-1].year == 2025
    assert plan.download_items[-1].month == 12
    assert len(plan.plan_hash) == 64


def test_revised_p4_scale_plan_builds_72_month_matrix() -> None:
    plan = build_p4_scale_plan(
        universe=get_default_phase0_p4_crypto_universe(),
        plan_id=P4_REVISED_SCALE_PLAN_ID,
        start_year=2020,
        start_month=1,
        end_year=2025,
        end_month=12,
        artifact_root="artifacts/evidence/p4_binance_scale/revised_v2",
    )

    assert plan.plan_id == P4_REVISED_SCALE_PLAN_ID
    assert plan.universe_id == "PHASE0-CRYPTO-P4-20-v2"
    assert plan.asset_count == 20
    assert plan.month_count == 72
    assert plan.download_count == 1440
    assert plan.download_items[0].symbol == "BTCUSDT"
    assert plan.download_items[0].year == 2020
    assert plan.download_items[0].month == 1
    assert plan.download_items[-1].symbol == "XTZUSDT"
    assert plan.download_items[-1].year == 2025
    assert plan.download_items[-1].month == 12


def test_p4_scale_plan_first_batch_and_pending_count() -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe(), batch_size=7)

    batch = first_batch(plan)

    assert len(batch) == 7
    assert pending_count(batch) == 7
    assert tuple(item.sequence for item in batch) == tuple(range(1, 8))


def test_p4_scale_plan_batch_items_returns_one_based_resumable_slice() -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe(), batch_size=7)

    batch = batch_items(plan, batch_index=2)

    assert len(batch) == 7
    assert tuple(item.sequence for item in batch) == tuple(range(8, 15))


def test_p4_scale_plan_batch_items_rejects_non_positive_index() -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe(), batch_size=7)

    try:
        batch_items(plan, batch_index=0)
    except ValueError as exc:
        assert str(exc) == "batch_index must be positive"
    else:
        raise AssertionError("batch_items should reject non-positive batch_index")


def test_p4_scale_plan_manifest_and_rendered_boundary() -> None:
    plan = build_p4_scale_plan(universe=get_default_phase0_crypto_universe())

    payload = plan_manifest_payload(plan)
    rendered = render_p4_scale_plan(plan)

    assert payload["plan_hash"] == plan.plan_hash
    assert payload["download_count"] == 720
    assert payload["gate_claim_allowed"] is False
    assert "Gate claim allowed | false" in rendered
    assert "At least 15 assets" in rendered
    assert "BTCUSDT-1d-2023-01.zip" in rendered
