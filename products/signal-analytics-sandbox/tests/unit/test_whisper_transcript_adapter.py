from __future__ import annotations

import hashlib
import sys
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

from signal_sandbox.media import MediaArtifact, MediaModality, RetentionState
from signal_sandbox.media.transcription import (
    DraftTranscriptStatus,
    OpenAIWhisperTranscriptionClient,
    TranscriptionRunStatus,
    WhisperTranscriptionClientError,
    run_whisper_transcription,
)


def test_double_gate_required(tmp_path: Path) -> None:
    media = _media_artifact(tmp_path)
    client = FakeTranscriptionClient("BTC long setup")

    disabled = run_whisper_transcription(
        media,
        client=client,
        output_dir=tmp_path / "transcripts",
        env={"SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION": "0"},
        per_run_approved=True,
    )
    not_approved = run_whisper_transcription(
        media,
        client=client,
        output_dir=tmp_path / "transcripts",
        env={"SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION": "1"},
        per_run_approved=False,
    )

    assert disabled.status == TranscriptionRunStatus.SKIPPED
    assert not_approved.status == TranscriptionRunStatus.SKIPPED
    assert client.calls == []
    assert not (tmp_path / "transcripts").exists()


def test_transcript_preserves_media_provenance(tmp_path: Path) -> None:
    media = _media_artifact(tmp_path)
    transcript_text = "BTC long setup"
    client = FakeTranscriptionClient(transcript_text)

    result = run_whisper_transcription(
        media,
        client=client,
        output_dir=tmp_path / "transcripts",
        env={"SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION": "1"},
        per_run_approved=True,
        provider="fake-whisper",
        model="whisper-test",
        delete_raw_on_success=False,
    )

    transcript = result.transcript
    assert result.status == TranscriptionRunStatus.DRAFT_PENDING_REVIEW
    assert transcript is not None
    assert transcript.media_id == media.media_id
    assert transcript.provider == "fake-whisper"
    assert transcript.model == "whisper-test"
    assert (
        transcript.transcript_sha256
        == hashlib.sha256(transcript_text.encode("utf-8")).hexdigest()
    )
    assert transcript.source_media_sha256 == media.media_sha256
    assert transcript.status == DraftTranscriptStatus.DRAFT_PENDING_REVIEW
    assert transcript.reviewer_id == "pending"
    assert transcript.review_required is True
    assert transcript.artifact_path is not None
    assert Path(transcript.artifact_path).exists()
    assert media.media_id in Path(transcript.artifact_path).read_text(encoding="utf-8")


def test_provider_failure_is_not_truth(tmp_path: Path) -> None:
    media = _media_artifact(tmp_path)
    client = FakeTranscriptionClient("ignored", fail=True)

    result = run_whisper_transcription(
        media,
        client=client,
        output_dir=tmp_path / "transcripts",
        env={"SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION": "1"},
        per_run_approved=True,
    )

    assert result.status == TranscriptionRunStatus.PROVIDER_FAILED
    assert result.transcript is None
    assert result.error_type == "WhisperTranscriptionClientError"
    assert media.local_path and Path(media.local_path).exists()
    assert not list((tmp_path / "transcripts").glob("*.json"))


def test_openai_whisper_client_calls_managed_transcription(
    tmp_path: Path,
    monkeypatch,
) -> None:
    media_path = tmp_path / "voice.ogg"
    media_path.write_bytes(b"voice bytes")
    calls: list[tuple[str, str, bytes]] = []

    class FakeTranscriptions:
        @staticmethod
        def create(*, model: str, file) -> SimpleNamespace:
            calls.append((model, file.name, file.read()))
            return SimpleNamespace(text="  расшифровка голосового  ")

    class FakeOpenAI:
        def __init__(self, *, api_key: str) -> None:
            assert api_key == "test-key"
            self.audio = SimpleNamespace(
                transcriptions=FakeTranscriptions(),
            )

    monkeypatch.setitem(sys.modules, "openai", SimpleNamespace(OpenAI=FakeOpenAI))

    client = OpenAIWhisperTranscriptionClient(api_key="test-key")

    assert (
        client.transcribe(media_path, model="whisper-test") == "расшифровка голосового"
    )
    assert calls == [("whisper-test", str(media_path), b"voice bytes")]


def test_openai_whisper_client_requires_api_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    client = OpenAIWhisperTranscriptionClient()

    try:
        client.transcribe(Path("voice.ogg"), model="whisper-test")
    except WhisperTranscriptionClientError as exc:
        assert "OPENAI_API_KEY" in str(exc)
    else:
        raise AssertionError("expected missing-key failure")


def test_success_follows_retention_and_logging_policy(
    tmp_path: Path,
    caplog,
) -> None:
    media = _media_artifact(tmp_path)
    raw_transcript = "secret market text should not be logged"
    client = FakeTranscriptionClient(raw_transcript)

    result = run_whisper_transcription(
        media,
        client=client,
        output_dir=tmp_path / "transcripts",
        env={"SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION": "1"},
        per_run_approved=True,
        delete_raw_on_success=True,
    )

    assert result.status == TranscriptionRunStatus.DRAFT_PENDING_REVIEW
    assert result.transcript is not None
    assert result.transcript.raw_media_retention_action == "deleted_after_transcription"
    assert not Path(media.local_path).exists()
    assert raw_transcript not in caplog.text


class FakeTranscriptionClient:
    def __init__(self, transcript: str, *, fail: bool = False) -> None:
        self.transcript = transcript
        self.fail = fail
        self.calls: list[tuple[Path, str]] = []

    def transcribe(self, media_path: Path, *, model: str) -> str:
        self.calls.append((media_path, model))
        if self.fail:
            raise WhisperTranscriptionClientError("provider unavailable")
        return self.transcript


def _media_artifact(tmp_path: Path) -> MediaArtifact:
    media_path = tmp_path / "voice.ogg"
    media_bytes = b"voice bytes"
    media_path.write_bytes(media_bytes)
    return MediaArtifact(
        media_id="telegram_voice_bablos79_10442",
        source_id="bablos79",
        capture_id="bablos79-10442",
        source_document_id="bablos79:bablos79-10442",
        source_timestamp_utc=datetime(2026, 5, 9, 10, 0, tzinfo=UTC),
        modality=MediaModality.VOICE,
        original_url_or_file_id="fixture_voice_ref",
        local_path=str(media_path),
        media_sha256=hashlib.sha256(media_bytes).hexdigest(),
        mime_type="audio/ogg",
        duration_seconds=47,
        retention_state=RetentionState.TEMPORARY,
        created_at_utc=datetime(2026, 5, 9, 12, 0, tzinfo=UTC),
    )
