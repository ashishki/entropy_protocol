from __future__ import annotations

import json
from pathlib import Path

import pytest

from signal_sandbox.capture.loader import (
    CaptureChecksumMismatch,
    PrivateSourceForbidden,
    compute_text_sha256,
    load_capture,
    load_captures,
)


def write_capture(
    path: Path,
    *,
    capture_id: str = "cap-001",
    source_id: str = "bablos79",
    evidence_url: str = "https://t.me/bablos79/1",
    timestamp: str = "2026-05-07T10:00:00Z",
    raw_text: str = "BTC long entry 100 target 110 stop 95",
    text_sha256: str | None = None,
) -> None:
    payload = {
        "capture_id": capture_id,
        "source_id": source_id,
        "evidence_url": evidence_url,
        "capture_timestamp_utc": timestamp,
        "raw_text": raw_text,
        "text_sha256": text_sha256 or compute_text_sha256(raw_text),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")


def test_checksum_mismatch_rejected(tmp_path: Path) -> None:
    capture_path = tmp_path / "capture.json"
    write_capture(capture_path, text_sha256="0" * 64)

    with pytest.raises(CaptureChecksumMismatch):
        load_capture(capture_path)


def test_private_source_rejected(tmp_path: Path) -> None:
    capture_path = tmp_path / "capture.json"
    write_capture(capture_path, evidence_url="https://t.me/+privateInvite")

    with pytest.raises(PrivateSourceForbidden):
        load_capture(capture_path)


def test_deterministic_order(tmp_path: Path) -> None:
    captures_dir = tmp_path / "captures" / "bablos79"
    write_capture(
        captures_dir / "b.json",
        capture_id="b",
        timestamp="2026-05-07T10:00:00Z",
    )
    write_capture(
        captures_dir / "a.json",
        capture_id="a",
        timestamp="2026-05-07T10:00:00Z",
    )
    write_capture(
        captures_dir / "c.json",
        capture_id="c",
        timestamp="2026-05-07T09:00:00Z",
    )

    posts = load_captures(tmp_path, "bablos79")

    assert [post.capture_id for post in posts] == ["c", "a", "b"]


def test_empty_directory(tmp_path: Path) -> None:
    captures_dir = tmp_path / "captures" / "bablos79"
    captures_dir.mkdir(parents=True)

    assert load_captures(tmp_path, "bablos79") == []
