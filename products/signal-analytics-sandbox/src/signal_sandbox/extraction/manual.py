"""Manual extraction adapter using an injected editor command."""

from __future__ import annotations

import json
from collections.abc import Callable
from decimal import Decimal
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from signal_sandbox.capture.loader import CapturedPost
from signal_sandbox.extraction.base import (
    ExtractionAdapter,
    ExtractionResult,
    ExtractionStatus,
)
from signal_sandbox.ledger.record import SignalRecord

EditorCommand = Callable[[Path], None]

REQUIRED_OPERATOR_FIELDS = [
    "extracted_timestamp_utc",
    "asset_symbol",
    "direction",
    "entry",
    "stop",
    "target",
]


class ManualExtractionAdapter(ExtractionAdapter):
    def __init__(self, drafts_dir: Path, editor: EditorCommand) -> None:
        self.drafts_dir = drafts_dir
        self.editor = editor

    def extract(self, post: CapturedPost) -> ExtractionResult:
        template_path = self._template_path(post)
        self._write_template(post, template_path)
        self.editor(template_path)
        payload = json.loads(template_path.read_text(encoding="utf-8"))

        missing = _missing_required_operator_fields(payload)
        if missing:
            return ExtractionResult(
                status=ExtractionStatus.DEFER_TO_HUMAN,
                post=post,
                reason=f"missing required fields: {', '.join(missing)}",
            )

        try:
            record = SignalRecord.model_validate(_record_payload(post, payload))
        except (ValidationError, ValueError) as exc:
            return ExtractionResult(
                status=ExtractionStatus.DEFER_TO_HUMAN,
                post=post,
                reason=f"invalid manual extraction: {exc}",
            )

        return ExtractionResult(
            status=ExtractionStatus.DRAFT_PENDING_REVIEW,
            post=post,
            record=record,
        )

    def _template_path(self, post: CapturedPost) -> Path:
        return self.drafts_dir / f"{post.source_id}-{post.capture_id}.json"

    def _write_template(self, post: CapturedPost, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(_template_payload(post), ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )


def _template_payload(post: CapturedPost) -> dict[str, Any]:
    return {
        "source_id": post.source_id,
        "capture_id": post.capture_id,
        "evidence_url": post.evidence_url,
        "text_sha256": post.text_sha256,
        "capture_timestamp_utc": post.capture_timestamp_utc.isoformat(),
        "extracted_timestamp_utc": "",
        "asset_symbol": "",
        "direction": "",
        "entry": "",
        "stop": "",
        "target": "",
        "confidence_flags": [],
        "ambiguity_flags": [],
        "reviewer_id": "",
        "extraction_metadata": {"adapter_id": "manual"},
    }


def _missing_required_operator_fields(payload: dict[str, Any]) -> list[str]:
    return [
        field
        for field in REQUIRED_OPERATOR_FIELDS
        if field not in payload or payload[field] in {None, ""}
    ]


def _record_payload(post: CapturedPost, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "source_id": post.source_id,
        "capture_id": post.capture_id,
        "evidence_url": post.evidence_url,
        "text_sha256": post.text_sha256,
        "capture_timestamp_utc": post.capture_timestamp_utc,
        "extracted_timestamp_utc": payload["extracted_timestamp_utc"],
        "asset_symbol": payload["asset_symbol"],
        "direction": payload["direction"],
        "entry": _decimal_or_none(payload["entry"]),
        "stop": _decimal_or_none(payload["stop"]),
        "target": _decimal_or_none(payload["target"]),
        "confidence_flags": payload.get("confidence_flags", []),
        "ambiguity_flags": payload.get("ambiguity_flags", []),
        "reviewer_id": payload.get("reviewer_id") or None,
        "extraction_metadata": payload.get("extraction_metadata", {}),
    }


def _decimal_or_none(value: Any) -> Decimal | None:
    if value is None or value == "":
        return None
    return Decimal(str(value))
