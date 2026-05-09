from datetime import UTC, datetime

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.draft_parser import parse_draft


def test_parse_draft_returns_structured_review_draft() -> None:
    post = _post("#MAGN совет директоров. Мы шортили с текущих хаев.")

    draft = parse_draft(post, _profile())

    assert draft.capture_id == post.capture_id
    assert draft.suggested_status == "insufficient_fields"
    assert draft.candidate_fields["asset_candidates"] == ["MAGN"]
    assert draft.candidate_fields["direction_candidate"] == "short"
    assert draft.review_required is True
    assert "missing_entry" in draft.reason_codes


def test_parse_draft_preserves_evidence_fields() -> None:
    post = _post("#CHMF entry 100 stop 95 target 110 buy")

    draft = parse_draft(post, _complete_profile())

    assert draft.capture_id == post.capture_id
    assert draft.evidence_url == post.evidence_url
    assert draft.text_sha256 == post.text_sha256


def test_pseudo_label_fixtures_classify_deterministically() -> None:
    post = _post("По #AMD отбой. Пока не буду шортить его.")

    first = parse_draft(post, _profile())
    second = parse_draft(post, _profile())

    assert first == second
    assert first.suggested_status == "needs_review"
    assert "uncertainty_marker_detected" in first.reason_codes


def test_complete_candidate_requires_human_review() -> None:
    post = _post("#CHMF buy entry 100 stop 95 target 110")

    draft = parse_draft(post, _complete_profile())

    assert draft.suggested_status == "review_candidate"
    assert draft.review_required is True
    assert draft.suggested_status != "approved"


def _post(raw_text: str) -> CapturedPost:
    return CapturedPost(
        capture_id="bablos79-test",
        source_id="bablos79",
        evidence_url="https://t.me/bablos79/1",
        capture_timestamp_utc=datetime(2026, 5, 7, 18, 51, 32, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )


def _profile() -> dict[str, object]:
    return {
        "candidates": [
            {
                "term": "#MAGN",
                "category": "asset_alias",
                "profile_state": "accepted_for_draft",
            },
            {
                "term": "#AMD",
                "category": "asset_alias",
                "profile_state": "accepted_for_draft",
            },
            {
                "term": "шорт",
                "category": "direction_short",
                "profile_state": "accepted_for_draft",
            },
            {
                "term": "отбой",
                "category": "uncertainty",
                "profile_state": "accepted_for_draft",
            },
            {
                "term": "шортить",
                "category": "direction_short",
                "profile_state": "needs_review",
            },
        ]
    }


def _complete_profile() -> dict[str, object]:
    return {
        "candidates": [
            {
                "term": "#CHMF",
                "category": "asset_alias",
                "profile_state": "accepted_for_draft",
            },
            {
                "term": "buy",
                "category": "direction_long",
                "profile_state": "accepted_for_draft",
            },
        ]
    }
