from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EVAL_JSON = PROJECT_ROOT / "docs/pilot/clientready_AUTO_VALIDATION_EVAL.json"
EVAL_MD = PROJECT_ROOT / "docs/pilot/clientready_AUTO_VALIDATION_EVAL.md"


def _artifact() -> dict:
    return json.loads(EVAL_JSON.read_text(encoding="utf-8"))


def test_auto_validation_eval_records_decision_counts_for_all_candidates() -> None:
    artifact = _artifact()
    summary = artifact["summary"]
    rows = artifact["rows"]

    assert summary["status"] == "clientready_auto_validation_eval"
    assert summary["candidate_count"] == 9
    assert len(rows) == 9
    assert summary["decision_counts"] == {
        "auto_accepted": 0,
        "auto_rejected": 4,
        "excluded_provider_gap": 0,
        "needs_human": 5,
        "blocked_customer_facing": 0,
    }
    assert sum(summary["decision_counts"].values()) == 9
    assert EVAL_MD.read_text(encoding="utf-8").count("| clientready-") == 9


def test_auto_validation_eval_cites_audit_refs_and_blockers_for_every_row() -> None:
    for row in _artifact()["rows"]:
        assert row["validator_audit_ref"].startswith("auto-val-audit:")
        assert row["policy_audit_ref"].startswith("customer-policy:")
        assert row["validator_result_refs"]
        assert row["blocker_reasons"]
        assert row["source_url"].startswith("https://t.me/")


def test_auto_validation_eval_keeps_customer_facing_promotion_blocked() -> None:
    artifact = _artifact()

    assert artifact["summary"]["customer_facing_policy_passed_rows"] == 0
    assert artifact["summary"]["customer_facing_rows"] == 0
    assert artifact["summary"]["promotion_blocked"] is True
    for row in artifact["rows"]:
        assert row["policy_gate_status"] == "blocked_customer_facing"
        assert row["customer_facing_allowed"] is False
        assert row["auto_decision"] != "auto_accepted"


def test_auto_validation_eval_preserves_post_factum_as_rejections_not_outcomes() -> (
    None
):
    rows = _artifact()["rows"]
    rejected = [row for row in rows if row["auto_decision"] == "auto_rejected"]

    assert {row["post_id"] for row in rejected} == {3225, 3264, 3274, 3276}
    assert all(
        "auto_rejected_for_predictive_metrics" in row["blocker_reasons"]
        for row in rejected
    )
    assert "wins" not in json.dumps(rejected)
    assert "losses" not in json.dumps(rejected)
