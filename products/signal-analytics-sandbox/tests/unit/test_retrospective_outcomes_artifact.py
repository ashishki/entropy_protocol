from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_bablos79_outcomes_do_not_compute_without_approved_proxies() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.json").read_text(
            encoding="utf-8"
        )
    )
    summary = artifact["summary"]

    assert summary["total_claim_rows"] == len(artifact["outcomes"])
    assert summary["approved_proxy_rows"] == 0
    assert summary["market_data_snapshots_used"] == 0
    assert summary["computed_metric_rows"] == 0
    assert summary["confirmed_rows"] == 0
    assert summary["contradicted_rows"] == 0


def test_bablos79_outcomes_keep_unresolved_and_non_measurable_rows() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/bablos79_RETROSPECTIVE_OUTCOMES.json").read_text(
            encoding="utf-8"
        )
    )
    summary = artifact["summary"]
    outcomes = artifact["outcomes"]

    assert summary["unresolved_rows"] > 0
    assert summary["non_measurable_rows"] > 0
    assert summary["not_applicable_rows"] > 0
    assert summary["unsupported_media_rows"] == 4
    assert all(outcome["metric_computed"] is False for outcome in outcomes)
    assert all(outcome["market_data_snapshot_ref"] is None for outcome in outcomes)
