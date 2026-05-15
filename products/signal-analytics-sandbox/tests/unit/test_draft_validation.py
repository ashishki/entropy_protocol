from datetime import UTC, datetime

import pytest

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.draft_validation import (
    PseudoLabelValidationError,
    validate_pseudo_label,
)


def test_validate_pseudo_label_rejects_unsupported_fields() -> None:
    post = _post("По #AMD отбой. Пока не буду шортить его.")
    pseudo_label = {
        "capture_id": post.capture_id,
        "candidate_fields": {
            "asset_candidates": ["NVDA"],
            "direction_candidate": "unknown",
            "entry_candidate": None,
            "stop_candidate": None,
            "target_candidate": None,
        },
        "evidence_spans": [{"field": "asset_candidates", "text": "#NVDA"}],
    }

    with pytest.raises(PseudoLabelValidationError):
        validate_pseudo_label(post, pseudo_label)


def test_validate_pseudo_label_accepts_supported_spans() -> None:
    post = _post("По #AMD отбой. Пока не буду шортить его.")
    pseudo_label = {
        "capture_id": post.capture_id,
        "candidate_fields": {
            "asset_candidates": ["AMD"],
            "direction_candidate": "short",
            "entry_candidate": None,
            "stop_candidate": None,
            "target_candidate": None,
        },
        "evidence_spans": [
            {"field": "asset_candidates", "text": "#AMD"},
            {"field": "direction_candidate", "text": "шортить"},
        ],
    }

    assert validate_pseudo_label(post, pseudo_label) == pseudo_label


def _post(raw_text: str) -> CapturedPost:
    return CapturedPost(
        capture_id="bablos79-test",
        source_id="bablos79",
        evidence_url="https://t.me/bablos79/1",
        capture_timestamp_utc=datetime(2026, 5, 7, 18, 51, 32, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )
