from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_three_channel_probe_records_public_boundary() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json").read_text(
            encoding="utf-8"
        )
    )

    boundary = artifact["source_boundary"]
    assert boundary["source_class"] == "telegram_public"
    assert boundary["public_s_pages_only"] is True
    assert boundary["private_sources_used"] is False
    assert boundary["login_walled_sources_used"] is False
    assert boundary["paywalled_sources_used"] is False
    assert boundary["market_data_fetched"] is False
    assert boundary["outcomes_computed"] is False
    assert boundary["external_claims_created"] is False


def test_three_channel_probe_has_comparable_candidate_counts() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json").read_text(
            encoding="utf-8"
        )
    )

    channels = {channel["source_id"]: channel for channel in artifact["channels"]}
    assert set(channels) == {"bablos79", "nemphiscrypts", "pifagortrade"}
    assert artifact["totals"]["text_rows"] >= 1_400
    assert artifact["totals"]["market_adjacent_candidates"] >= 800
    assert artifact["totals"]["market_data_fetch_allowed_now"] == 0
    assert artifact["totals"]["external_eligible_now"] == 0

    assert channels["bablos79"]["text_rows"] >= 500
    assert channels["nemphiscrypts"]["text_rows"] >= 500
    assert channels["pifagortrade"]["text_rows"] >= 450
    assert (
        channels["pifagortrade"]["explicit_setup_candidates"]
        > channels["nemphiscrypts"]["explicit_setup_candidates"]
        > channels["bablos79"]["explicit_setup_candidates"]
    )


def test_three_channel_review_samples_remain_operator_gated() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json").read_text(
            encoding="utf-8"
        )
    )

    for source_id, samples in artifact["review_samples"].items():
        assert source_id in {"bablos79", "nemphiscrypts", "pifagortrade"}
        assert samples
        assert all(sample["requires_operator_approval"] is True for sample in samples)
        assert all(
            sample["market_data_fetch_allowed_now"] is False for sample in samples
        )
        assert all(sample["external_eligible_now"] is False for sample in samples)
