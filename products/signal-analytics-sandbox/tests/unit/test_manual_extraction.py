from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from signal_sandbox.capture.loader import CapturedPost, compute_text_sha256
from signal_sandbox.extraction.base import ExtractionStatus
from signal_sandbox.extraction.manual import ManualExtractionAdapter
from signal_sandbox.ledger.record import Direction


def post() -> CapturedPost:
    raw_text = "BTC long entry 100 target 110 stop 90"
    return CapturedPost(
        capture_id="cap-001",
        source_id="pilot",
        evidence_url="https://t.me/bablos79/1",
        capture_timestamp_utc=datetime(2026, 5, 7, 10, tzinfo=UTC),
        raw_text=raw_text,
        text_sha256=compute_text_sha256(raw_text),
    )


def test_template_prefilled(tmp_path: Path) -> None:
    seen_payload: dict[str, object] = {}

    def editor(path: Path) -> None:
        payload = json.loads(path.read_text())
        seen_payload.update(payload)
        payload.update(valid_operator_fields())
        path.write_text(json.dumps(payload, sort_keys=True))

    result = ManualExtractionAdapter(tmp_path, editor).extract(post())

    assert seen_payload["source_id"] == "pilot"
    assert seen_payload["capture_id"] == "cap-001"
    assert seen_payload["evidence_url"] == "https://t.me/bablos79/1"
    assert seen_payload["text_sha256"] == post().text_sha256
    for field in [
        "extracted_timestamp_utc",
        "asset_symbol",
        "direction",
        "entry",
        "stop",
        "target",
        "confidence_flags",
        "ambiguity_flags",
        "reviewer_id",
        "extraction_metadata",
    ]:
        assert field in seen_payload
    assert result.status == ExtractionStatus.DRAFT_PENDING_REVIEW


def test_status_branches(tmp_path: Path) -> None:
    def complete_editor(path: Path) -> None:
        payload = json.loads(path.read_text())
        payload.update(valid_operator_fields())
        path.write_text(json.dumps(payload, sort_keys=True))

    complete = ManualExtractionAdapter(tmp_path / "complete", complete_editor).extract(
        post()
    )

    assert complete.status == ExtractionStatus.DRAFT_PENDING_REVIEW
    assert complete.record is not None
    assert complete.record.asset_symbol == "BTC"
    assert complete.record.direction == Direction.LONG
    assert complete.record.entry == Decimal("100")
    assert complete.record.evidence_url == post().evidence_url
    assert complete.record.text_sha256 == post().text_sha256

    def blank_editor(path: Path) -> None:
        payload = json.loads(path.read_text())
        payload["asset_symbol"] = "BTC"
        path.write_text(json.dumps(payload, sort_keys=True))

    deferred = ManualExtractionAdapter(tmp_path / "blank", blank_editor).extract(post())

    assert deferred.status == ExtractionStatus.DEFER_TO_HUMAN
    assert deferred.record is None
    assert "missing required fields" in deferred.reason
    assert "direction" in deferred.reason
    assert "target" in deferred.reason


def valid_operator_fields() -> dict[str, object]:
    return {
        "extracted_timestamp_utc": "2026-05-07T10:05:00+00:00",
        "asset_symbol": "BTC",
        "direction": "long",
        "entry": "100",
        "stop": "90",
        "target": "110",
    }
