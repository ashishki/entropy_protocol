from __future__ import annotations

import asyncio
import hashlib
from datetime import UTC, datetime
from pathlib import Path

import pytest
from pydantic import ValidationError

from signal_sandbox.media import MediaModality, RetentionState
from signal_sandbox.media.telegram_voice import (
    MediaAuthorization,
    TelegramVoiceAcquisitionRequest,
    TelegramVoiceDownloadError,
    UnauthorizedMediaError,
    acquire_telegram_voice_artifact,
)


def test_downloads_voice_with_injected_client(tmp_path: Path) -> None:
    media_bytes = b"voice bytes"
    client = FakeTelegramClient(media_bytes)
    request = _request()

    artifact = asyncio.run(
        acquire_telegram_voice_artifact(
            request,
            client=client,
            media_dir=tmp_path,
        )
    )

    expected_sha = hashlib.sha256(media_bytes).hexdigest()
    assert client.requested_file_id == "fixture_voice_ref"
    assert artifact.modality == MediaModality.VOICE
    assert artifact.retention_state == RetentionState.TEMPORARY
    assert artifact.capture_id == "bablos79-10442"
    assert artifact.source_document_id == "bablos79:bablos79-10442"
    assert artifact.original_url_or_file_id == "fixture_voice_ref"
    assert artifact.media_sha256 == expected_sha
    assert artifact.duration_seconds == 47
    assert artifact.mime_type == "audio/ogg"
    assert Path(artifact.local_path).read_bytes() == media_bytes
    assert not list(tmp_path.glob("*.part"))


def test_rejects_unauthorized_or_unlinked_voice(tmp_path: Path) -> None:
    client = FakeTelegramClient(b"voice bytes")

    with pytest.raises(UnauthorizedMediaError):
        asyncio.run(
            acquire_telegram_voice_artifact(
                _request(legal_media_authorized=False),
                client=client,
                media_dir=tmp_path,
            )
        )

    with pytest.raises(UnauthorizedMediaError):
        asyncio.run(
            acquire_telegram_voice_artifact(
                _request(authorization=MediaAuthorization.FORBIDDEN_PRIVATE),
                client=client,
                media_dir=tmp_path,
            )
        )

    with pytest.raises(ValidationError):
        _request(capture_id="")


def test_download_failure_has_no_partial_artifact(tmp_path: Path) -> None:
    client = FakeTelegramClient(b"voice bytes", fail=True)

    with pytest.raises(TelegramVoiceDownloadError):
        asyncio.run(
            acquire_telegram_voice_artifact(
                _request(),
                client=client,
                media_dir=tmp_path,
            )
        )

    assert not list(tmp_path.iterdir())


class FakeTelegramClient:
    def __init__(self, payload: bytes, *, fail: bool = False) -> None:
        self.payload = payload
        self.fail = fail
        self.requested_file_id: str | None = None

    async def get_file(self, file_id: str) -> FakeTelegramFile:
        self.requested_file_id = file_id
        return FakeTelegramFile(self.payload, fail=self.fail)


class FakeTelegramFile:
    def __init__(self, payload: bytes, *, fail: bool = False) -> None:
        self.payload = payload
        self.fail = fail

    async def download_to_drive(self, custom_path: str) -> None:
        if self.fail:
            Path(custom_path).write_bytes(b"partial")
            raise RuntimeError("download failed")
        Path(custom_path).write_bytes(self.payload)


def _request(
    *,
    authorization: MediaAuthorization = MediaAuthorization.PUBLIC_TELEGRAM,
    legal_media_authorized: bool = True,
    capture_id: str = "bablos79-10442",
) -> TelegramVoiceAcquisitionRequest:
    return TelegramVoiceAcquisitionRequest(
        file_id="fixture_voice_ref",
        source_id="bablos79",
        capture_id=capture_id,
        source_document_id="bablos79:bablos79-10442",
        source_timestamp_utc=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
        duration_seconds=47,
        authorization=authorization,
        legal_media_authorized=legal_media_authorized,
        created_at_utc=datetime(2026, 5, 9, 12, 0, tzinfo=UTC),
        metadata={"operator_attestation": "public channel"},
    )
