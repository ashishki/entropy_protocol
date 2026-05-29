from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_ocr_chart_policy_requires_source_links_and_review_fields() -> None:
    policy = (PROJECT_ROOT / "docs/specs/OCR_CHART_SOURCE_LINK_POLICY.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "`source_ref`",
        "`source_document_id`",
        "`media_id`",
        "`source_media_sha256`",
        "`ocr_artifact_ref`",
        "`ocr_text_sha256`",
        "`reviewer_id`",
        "`reason`",
        "`accepted_claim_boundary`",
        "`external_claim_ready`",
    ):
        assert required in policy


def test_ocr_chart_policy_blocks_machine_only_chart_claims() -> None:
    policy = (PROJECT_ROOT / "docs/specs/OCR_CHART_SOURCE_LINK_POLICY.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "Machine-only chart interpretation is forbidden for customer-facing metrics.",
        "support or resistance levels",
        "entry, stop, target, or invalidation levels",
        "`ocr_draft_pending_review`",
        "`chart_context_only`",
        "`human_claim_accepted`",
        "Machine-only chart interpretation remains blocked.",
    ):
        assert required in policy
