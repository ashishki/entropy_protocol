from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_bablos79_claim_ledger_keeps_blocked_and_non_market_rows() -> None:
    ledger_path = PROJECT_ROOT / "docs/pilot/bablos79_CLAIM_LEDGER.json"

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    summary = ledger["summary"]
    claims = ledger["claims"]

    assert summary["total_rows"] == len(claims)
    assert summary["text_capture_rows"] == 60
    assert summary["llm_reviewed_transcript_claims"] == 3
    assert summary["unsupported_media_blocker_rows"] == 4
    assert summary["insufficient_corpus_decision"] is True
    assert summary["deterministic_outcome_ready_rows"] == 0
    assert summary["customer_report_eligible_rows"] == 0
    assert summary["category_counts"]["non_market_commentary"] > 0
    assert summary["category_counts"]["unsupported_media_claim"] == 4


def test_bablos79_claim_ledger_rows_have_required_review_fields() -> None:
    ledger_path = PROJECT_ROOT / "docs/pilot/bablos79_CLAIM_LEDGER.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))

    for claim in ledger["claims"]:
        assert claim["claim_id"]
        assert claim["category"]
        assert claim["review_state"]
        assert claim["measurability_status"]
        assert claim["deterministic_outcome_ready"] is False
        assert claim["customer_report_eligible"] is False
        assert claim["outcome_blockers"]
