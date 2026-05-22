from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_known_v2_channel_aggregate_metrics_do_not_drift() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_V2_METRIC_RESULTS.json").read_text(
            encoding="utf-8"
        )
    )
    summaries = {row["source_id"]: row for row in artifact["channel_summaries"]}

    assert artifact["totals"] == {
        "public_text_rows": 1534,
        "v2_evaluable_claims": 170,
        "confirmed_hits": 93,
        "contradicted_misses": 77,
        "primary_hit_rate": "54.705882",
        "reviewed_media_claims_included": 0,
        "unreviewed_media_claims_excluded": 2,
        "blocked_or_unacquired_media_rows": 6,
        "delta_from_v1_evaluable_claims": 0,
        "delta_from_v1_confirmed_hits": 0,
        "delta_from_v1_contradicted_misses": 0,
    }
    assert summaries["bablos79"]["v2_evaluable_claims"] == 14
    assert summaries["nemphiscrypts"]["confirmed_hits"] == 28
    assert summaries["pifagortrade"]["contradicted_misses"] == 51


def test_known_v1_claim_examples_do_not_drift() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_V1_METRIC_RESULTS.json").read_text(
            encoding="utf-8"
        )
    )
    kept = artifact["kept_claim_ids_by_channel"]

    assert "claim_f6041f3dfd9af816" in kept["bablos79"]
    assert "claim_7997845104759b60" in kept["nemphiscrypts"]
    assert "claim_413df3d46a002e05" in kept["pifagortrade"]
    assert len(kept["bablos79"]) == 15
    assert len(kept["nemphiscrypts"]) == 49
    assert len(kept["pifagortrade"]) == 108
