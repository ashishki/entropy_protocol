"""Regex-based extraction adapter."""

from __future__ import annotations

import re
from decimal import Decimal

from signal_sandbox.capture.loader import CapturedPost
from signal_sandbox.extraction.base import (
    ExtractionAdapter,
    ExtractionResult,
    ExtractionStatus,
)
from signal_sandbox.extraction.rule_templates import TEMPLATES, RuleTemplate
from signal_sandbox.ledger.record import Direction, SignalRecord


class RuleExtractionAdapter(ExtractionAdapter):
    def __init__(self, template: str) -> None:
        self.template_id = template
        self.template = _load_template(template)
        self._pattern = re.compile(self.template.pattern, flags=re.IGNORECASE)

    def extract(self, post: CapturedPost) -> ExtractionResult:
        match = self._pattern.search(post.raw_text)
        if match is None:
            return ExtractionResult(
                status=ExtractionStatus.DEFER_TO_HUMAN,
                post=post,
                reason=f"no match for template {self.template_id}",
            )

        record = SignalRecord(
            source_id=post.source_id,
            capture_id=post.capture_id,
            evidence_url=post.evidence_url,
            text_sha256=post.text_sha256,
            capture_timestamp_utc=post.capture_timestamp_utc,
            extracted_timestamp_utc=post.capture_timestamp_utc,
            asset_symbol=match.group("asset").upper(),
            direction=Direction(match.group("direction").lower()),
            entry=Decimal(match.group("entry")),
            stop=Decimal(match.group("stop")),
            target=Decimal(match.group("target")),
            extraction_metadata={
                "adapter_id": f"rule/{self.template_id}",
                "template_sha256": self.template.pattern_sha256,
            },
        )
        return ExtractionResult(
            status=ExtractionStatus.DRAFT_PENDING_REVIEW,
            post=post,
            record=record,
        )


def _load_template(template_id: str) -> RuleTemplate:
    try:
        return TEMPLATES[template_id]
    except KeyError as exc:
        raise ValueError(f"unknown rule template: {template_id}") from exc
