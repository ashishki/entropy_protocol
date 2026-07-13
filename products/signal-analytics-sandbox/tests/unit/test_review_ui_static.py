from __future__ import annotations

from pathlib import Path

from signal_sandbox.review import load_review_queue
from signal_sandbox.review.ui import render_static_review_ui

PROJECT_ROOT = Path(__file__).resolve().parents[2]
UI_PATH = PROJECT_ROOT / "docs/pilot/review_ui/three_channel_review_ui.html"
CONTRACT_FIXTURE = (
    PROJECT_ROOT / "tests/fixtures/review/synthetic_full_review_queue.json"
)


def test_static_review_ui_artifact_contains_required_filters_and_data() -> None:
    html = UI_PATH.read_text(encoding="utf-8")

    for required in (
        'id="channel"',
        'id="claimType"',
        'id="asset"',
        'id="providerStatus"',
        'id="reviewStatus"',
        'id="queue-data"',
        "frq-source-nemphiscrypts-3344",
        "external delivery blocked",
    ):
        assert required in html


def test_static_review_ui_supports_local_decision_artifact_generation() -> None:
    html = UI_PATH.read_text(encoding="utf-8")

    for required in (
        "buildDecisionArtifact",
        "buildMarkdown",
        "review_ui_decisions",
        "decision_id",
        "evidence_span",
        "reviewed_at_utc",
    ):
        assert required in html


def test_static_review_ui_renderer_preserves_source_text_and_normalized_fields() -> (
    None
):
    queue = load_review_queue(CONTRACT_FIXTURE)
    html = render_static_review_ui(queue)

    assert "source_url" in html
    assert "evidence_snippet" in html
    assert "suggested_claim_type" in html
    assert "provider_symbol" in html
    assert "Synthetic evidence snippet for the review contract." in html
    assert "TEST-USD" in html
