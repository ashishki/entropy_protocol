from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTCOMES_JSON = PROJECT_ROOT / "docs/pilot/preclient_CANDIDATE_OUTCOMES.json"
OUTCOMES_MD = PROJECT_ROOT / "docs/pilot/preclient_CANDIDATE_OUTCOMES.md"


def test_preclient_candidate_outcomes_classify_every_reviewed_candidate() -> None:
    artifact = json.loads(OUTCOMES_JSON.read_text(encoding="utf-8"))
    rows = artifact["rows"]
    allowed_statuses = {
        "evaluated",
        "insufficient_fields",
        "provider_gap",
        "post_factum_only",
        "media_review_blocked",
    }

    assert artifact["summary"]["status"] == "internal_candidate_outcome_rr_recompute"
    assert artifact["summary"]["candidate_count"] == 9
    assert len(rows) == 9
    assert artifact["summary"]["by_candidate_status"] == {
        "insufficient_fields": 4,
        "post_factum_only": 4,
        "provider_gap": 1,
    }
    assert {row["candidate_status"] for row in rows}.issubset(allowed_statuses)
    assert artifact["summary"]["rr_recomputed_internal_count"] == 1
    assert artifact["summary"]["market_outcome_recomputed_count"] == 0


def test_preclient_candidate_outcomes_include_provider_refs_without_bulk_storage() -> (
    None
):
    artifact = json.loads(OUTCOMES_JSON.read_text(encoding="utf-8"))
    serialized = json.dumps(artifact, ensure_ascii=False)

    assert artifact["summary"]["bulk_market_history_storage_used"] is False
    assert "workspace/market_data" not in serialized
    for row in artifact["rows"]:
        assert row["source_url"].startswith("https://t.me/")
        assert row["source_timestamp_utc"]
        assert row["media_ref_id"].startswith("media_")
        assert row["provider_refs"]
        assert row["source_refs"]
        assert row["bulk_market_history_storage_used"] is False
        assert row["market_data_storage"] == "none_open_api_refs_only"
        assert row["customer_facing_status"] == "blocked_from_customer_metrics"


def test_preclient_candidate_outcomes_keep_post_factum_out_of_predictive_calls() -> (
    None
):
    rows = json.loads(OUTCOMES_JSON.read_text(encoding="utf-8"))["rows"]
    post_factum_rows = [
        row for row in rows if row["candidate_status"] == "post_factum_only"
    ]

    assert {row["post_id"] for row in post_factum_rows} == {3225, 3264, 3274, 3276}
    for row in post_factum_rows:
        assert row["predictive_call_policy"] == "post_factum_not_predictive_call"
        assert row["market_outcome"]["status"] == "market_outcome_not_recomputed"
        assert "post_factum_not_predictive_call" in row["blockers"]


def test_preclient_candidate_outcomes_record_rr_recompute_and_blockers() -> None:
    rows = json.loads(OUTCOMES_JSON.read_text(encoding="utf-8"))["rows"]
    by_post = {(row["source_id"], row["post_id"]): row for row in rows}
    report = OUTCOMES_MD.read_text(encoding="utf-8")

    bablos = by_post[("bablos79", 10450)]
    assert bablos["candidate_status"] == "provider_gap"
    assert bablos["rr_recompute"]["status"] == "rr_recomputed_internal"
    assert bablos["rr_recompute"]["computed_rr"] == "10.180000"
    assert "provider_gap=unapproved_contract_or_quote_scale" in bablos["provider_refs"]
    assert by_post[("pifagortrade", 3234)]["candidate_status"] == "insufficient_fields"
    assert "target_direction_conflict" in by_post[("pifagortrade", 3234)]["blockers"]
    assert "No bulk market-history storage is used." in report
    assert "Post-factum screenshots are not treated as predictive calls." in report
