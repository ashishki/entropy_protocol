from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMO_JSON = PROJECT_ROOT / "docs/pilot/clientready_REDACTED_BUYER_DEMO.json"
DEMO_MD = PROJECT_ROOT / "docs/pilot/clientready_REDACTED_BUYER_DEMO.md"


def _demo() -> dict:
    return json.loads(DEMO_JSON.read_text(encoding="utf-8"))


def test_clientready_redacted_demo_uses_compact_fields_and_source_links() -> None:
    demo = _demo()
    summary = demo["summary"]
    cards = demo["channel_cards"]
    report = DEMO_MD.read_text(encoding="utf-8")

    assert summary["status"] == "clientready_redacted_buyer_demo_subset"
    assert summary["channels_included"] == 3
    assert summary["source_linked_examples"] == 3
    assert summary["full_appendix_exposed"] is False
    assert [card["source_id"] for card in cards] == [
        "bablos79",
        "nemphiscrypts",
        "pifagortrade",
    ]
    assert "docs/pilot/preclient_EVIDENCE_APPENDIX" not in report

    for card in cards:
        assert set(card) == {
            "source_id",
            "source_type",
            "evaluated_window",
            "compact_text_claim_counts",
            "media_ref_count",
            "model_reviewed_candidate_count",
            "accepted_rows",
            "recomputed_rows",
            "gate_status",
            "visible_caveats",
            "source_linked_examples",
        }
        assert card["source_linked_examples"][0]["source_url"].startswith(
            "https://t.me/"
        )
        assert card["visible_caveats"]


def test_clientready_redacted_demo_avoids_forbidden_language() -> None:
    combined = (
        DEMO_JSON.read_text(encoding="utf-8")
        + "\n"
        + DEMO_MD.read_text(encoding="utf-8")
    ).lower()

    for forbidden in (
        "advice",
        "future-profit",
        "future profit",
        "ranking",
        "marketplace",
        "payment",
        "private-source",
        "private source",
        "guaranteed",
    ):
        assert forbidden not in combined


def test_clientready_redacted_demo_declares_blocked_showability() -> None:
    demo = _demo()
    summary = demo["summary"]
    report = DEMO_MD.read_text(encoding="utf-8")

    assert summary["showable_now"] is False
    assert summary["gate_decision"] == "blocked_internal_only"
    assert summary["accepted_rows"] == 0
    assert summary["recomputed_rows"] == 0
    assert summary["buyer_demo_safe_rows"] == 0
    assert "Showable now: `false`" in report
    assert "0 buyer-demo-safe rows" in report
