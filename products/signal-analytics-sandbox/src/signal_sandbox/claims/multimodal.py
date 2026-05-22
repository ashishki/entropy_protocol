"""Reviewed multimodal evidence to structured claim drafts."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from signal_sandbox.claims.extractor import StructuredClaim, extract_structured_claims
from signal_sandbox.corpus import SourceDocument


class MediaClaimStatus(StrEnum):
    EXTRACTED = "extracted"
    EXCLUDED_UNREVIEWED = "excluded_unreviewed"
    NO_MEDIA_REFS = "no_media_refs"


class MultimodalClaimDraft(BaseModel):
    model_config = ConfigDict(strict=True)

    status: MediaClaimStatus
    source_document_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    media_refs: list[str] = Field(default_factory=list)
    claim: StructuredClaim | None = None
    customer_metric_eligible: bool = False
    exclusion_reason: str | None = None


def extract_reviewed_multimodal_claims(
    document: SourceDocument,
    *,
    accepted_media_refs: set[str],
) -> list[MultimodalClaimDraft]:
    """Extract claims only from media refs accepted by human/operator review."""

    refs = [*document.transcript_refs, *document.ocr_refs]
    if not refs:
        return [
            MultimodalClaimDraft(
                status=MediaClaimStatus.NO_MEDIA_REFS,
                source_document_id=document.document_id,
                evidence_url=document.evidence_url,
                exclusion_reason="source_document_has_no_transcript_or_ocr_refs",
            )
        ]

    reviewed_refs = [ref for ref in refs if ref in accepted_media_refs]
    unreviewed_refs = [ref for ref in refs if ref not in accepted_media_refs]
    drafts: list[MultimodalClaimDraft] = []
    for claim in extract_structured_claims(document):
        if reviewed_refs:
            drafts.append(
                MultimodalClaimDraft(
                    status=MediaClaimStatus.EXTRACTED,
                    source_document_id=document.document_id,
                    evidence_url=document.evidence_url,
                    media_refs=reviewed_refs,
                    claim=claim,
                    customer_metric_eligible=True,
                )
            )
    if unreviewed_refs:
        drafts.append(
            MultimodalClaimDraft(
                status=MediaClaimStatus.EXCLUDED_UNREVIEWED,
                source_document_id=document.document_id,
                evidence_url=document.evidence_url,
                media_refs=unreviewed_refs,
                customer_metric_eligible=False,
                exclusion_reason="media_ref_not_human_operator_reviewed",
            )
        )
    return drafts
