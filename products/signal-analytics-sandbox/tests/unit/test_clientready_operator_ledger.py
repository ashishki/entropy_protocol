from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LEDGER_JSON = PROJECT_ROOT / "docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.json"
LEDGER_MD = PROJECT_ROOT / "docs/pilot/clientready_OPERATOR_MEDIA_LEDGER.md"


def _ledger() -> dict:
    return json.loads(LEDGER_JSON.read_text(encoding="utf-8"))


def test_clientready_operator_ledger_records_every_model_candidate() -> None:
    ledger = _ledger()
    rows = ledger["rows"]
    report = LEDGER_MD.read_text(encoding="utf-8")

    assert ledger["summary"]["status"] == "clientready_operator_media_acceptance_ledger"
    assert ledger["summary"]["source_artifact"] == (
        "docs/pilot/preclient_MODEL_REVIEW_PACKET.json"
    )
    assert ledger["summary"]["candidate_count"] == 9
    assert len(rows) == 9
    assert ledger["summary"]["decision_counts"] == {
        "accepted": 0,
        "rejected": 0,
        "needs_context": 5,
        "post_factum_only": 4,
    }
    assert "Model review remains triage only." in report

    for row in rows:
        assert row["source_url"].startswith("https://t.me/")
        assert row["media_ref_id"].startswith("media_")
        assert row["model_decision"] == "arbiter_accepted_internal_candidate"
        assert row["operator_decision"] in {
            "accepted",
            "rejected",
            "needs_context",
            "post_factum_only",
        }
        assert row["operator_decision_reason"]


def test_clientready_operator_ledger_blocks_model_only_dashboard_promotion() -> None:
    ledger = _ledger()

    assert ledger["summary"]["operator_input_received"] is False
    assert ledger["summary"]["dashboard_safe_rows"] == 0
    assert ledger["summary"]["paid_report_safe_rows"] == 0
    assert ledger["summary"]["customer_facing_rows"] == 0
    assert ledger["policy"]["model_review_boundary"] == "model_review_is_triage_only"

    for row in ledger["rows"]:
        assert row["dashboard_safe"] is False
        assert row["paid_report_safe"] is False
        assert row["customer_facing_status"].startswith("blocked_")
        if row["operator_decision"] != "accepted":
            assert "operator" in " ".join(row["blockers"]) or (
                row["operator_decision"] == "post_factum_only"
            )


def test_clientready_operator_ledger_keeps_post_factum_out_of_predictive_metrics() -> (
    None
):
    ledger = _ledger()
    post_factum_rows = [
        row for row in ledger["rows"] if row["operator_decision"] == "post_factum_only"
    ]
    report = LEDGER_MD.read_text(encoding="utf-8")

    assert {row["post_id"] for row in post_factum_rows} == {3225, 3264, 3274, 3276}
    assert ledger["summary"]["predictive_call_metric_eligible_rows"] == 0
    assert (
        "Post-factum-only rows remain blocked from predictive-call metrics." in report
    )

    for row in post_factum_rows:
        assert row["predictive_call_metric_eligible"] is False
        assert row["customer_facing_status"] == "blocked_post_factum_only"
        assert "post_factum_not_predictive_call" in row["blockers"]
