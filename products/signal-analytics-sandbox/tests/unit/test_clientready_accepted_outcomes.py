from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTCOMES_JSON = PROJECT_ROOT / "docs/pilot/clientready_ACCEPTED_OUTCOMES.json"
OUTCOMES_MD = PROJECT_ROOT / "docs/pilot/clientready_ACCEPTED_OUTCOMES.md"


def _artifact() -> dict:
    return json.loads(OUTCOMES_JSON.read_text(encoding="utf-8"))


def test_clientready_accepted_outcomes_report_recompute_counts() -> None:
    artifact = _artifact()
    summary = artifact["summary"]
    rows = artifact["rows"]
    report = OUTCOMES_MD.read_text(encoding="utf-8")

    assert summary["status"] == "clientready_accepted_outcome_recompute"
    assert summary["source_ledger"] == (
        "docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.json"
    )
    assert summary["candidate_count"] == 9
    assert summary["operator_accepted_rows"] == 0
    assert summary["recomputed_rows"] == 0
    assert summary["excluded_rows"] == 9
    assert summary["buyer_demo_safe_rows"] == 0
    assert summary["wins"] == 0
    assert summary["losses"] == 0
    assert len(rows) == 9
    assert "The current operator ledger has 0 accepted rows." in report


def test_clientready_accepted_outcomes_cite_provider_without_bulk_storage() -> None:
    artifact = _artifact()

    assert artifact["summary"]["bulk_market_history_storage_used"] is False
    for row in artifact["rows"]:
        assert row["source_url"].startswith("https://t.me/")
        assert row["source_timestamp_utc"]
        assert row["media_ref_id"].startswith("media_")
        assert row["provider_proxy_provenance"]
        assert row["bulk_market_history_storage_used"] is False
        if row["recompute_status"] == "recomputed":
            assert row["accepted_for_recompute"] is True


def test_clientready_accepted_outcomes_keep_exclusions_out_of_wins_losses() -> None:
    rows = _artifact()["rows"]
    excluded_rows = [
        row for row in rows if row["recompute_status"].startswith("excluded_")
    ]

    assert len(excluded_rows) == 9
    assert {row["outcome_classification"] for row in excluded_rows} == {
        "excluded_not_win_loss"
    }
    for row in excluded_rows:
        assert row["market_outcome"] == {
            "status": "market_outcome_not_recomputed",
            "win_loss": None,
        }
        assert row["buyer_demo_safe"] is False
        assert row["rr_recomputed"] is False


def test_clientready_accepted_outcomes_preserve_post_factum_exclusions() -> None:
    artifact = _artifact()
    post_factum_rows = [
        row
        for row in artifact["rows"]
        if row["recompute_status"] == "excluded_post_factum_only"
    ]
    report = OUTCOMES_MD.read_text(encoding="utf-8")

    assert artifact["summary"]["counts_by_exclusion_status"] == {
        "excluded_operator_not_accepted": 5,
        "excluded_post_factum_only": 4,
    }
    assert {row["post_id"] for row in post_factum_rows} == {3225, 3264, 3274, 3276}
    assert "post_factum_not_predictive_call" in {
        reason for row in post_factum_rows for reason in row["exclusion_reasons"]
    }
    assert "post-factum status remain exclusions, not" in report
