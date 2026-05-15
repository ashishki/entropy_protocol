"""Extraction adapter interface and result envelope."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, model_validator

from signal_sandbox.capture.loader import CapturedPost
from signal_sandbox.ledger.record import SignalRecord


class ExtractionStatus(StrEnum):
    DRAFT_PENDING_REVIEW = "draft_pending_review"
    DEFER_TO_HUMAN = "defer_to_human"


class ExtractionResult(BaseModel):
    model_config = ConfigDict(strict=True)

    status: ExtractionStatus
    post: CapturedPost
    record: SignalRecord | None = None
    reason: str = ""

    @model_validator(mode="after")
    def _validate_status_contract(self) -> ExtractionResult:
        if self.status == ExtractionStatus.DRAFT_PENDING_REVIEW:
            if self.record is None:
                raise ValueError("draft_pending_review requires record")
            if self.reason:
                raise ValueError("draft_pending_review must not include reason")
            self._validate_evidence_preserved()
        if self.status == ExtractionStatus.DEFER_TO_HUMAN:
            if self.record is not None:
                raise ValueError("defer_to_human must not include record")
            if not self.reason:
                raise ValueError("defer_to_human requires reason")
        return self

    def _validate_evidence_preserved(self) -> None:
        if self.record is None:
            return
        if self.record.evidence_url != self.post.evidence_url:
            raise ValueError("record evidence_url must match captured post")
        if self.record.text_sha256 != self.post.text_sha256:
            raise ValueError("record text_sha256 must match captured post")


class ExtractionAdapter(ABC):
    @abstractmethod
    def extract(self, post: CapturedPost) -> ExtractionResult:
        """Return a draft signal record or a deterministic defer reason."""
