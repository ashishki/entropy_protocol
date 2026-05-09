"""Join media-derived draft evidence refs into SourceDocument copies."""

from __future__ import annotations

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.media.artifact import MediaArtifact
from signal_sandbox.media.ocr import DraftOCRArtifact
from signal_sandbox.media.transcription import DraftTranscriptArtifact


class MediaJoinMismatchError(ValueError):
    """Raised when media or draft artifact provenance does not match a document."""


def join_multimodal_source_document(
    document: SourceDocument,
    *,
    media_artifacts: list[MediaArtifact],
    transcript_artifacts: list[DraftTranscriptArtifact],
    ocr_artifacts: list[DraftOCRArtifact],
) -> SourceDocument:
    media_by_id = _validate_media(document, media_artifacts)
    transcript_refs = [
        _validated_transcript_ref(transcript, media_by_id)
        for transcript in transcript_artifacts
    ]
    ocr_refs = [_validated_ocr_ref(ocr, media_by_id) for ocr in ocr_artifacts]
    media_refs = [media.local_path for media in media_artifacts]

    return document.model_copy(
        update={
            "media_refs": _unique([*document.media_refs, *media_refs]),
            "transcript_refs": _unique(
                [*document.transcript_refs, *transcript_refs]
            ),
            "ocr_refs": _unique([*document.ocr_refs, *ocr_refs]),
        }
    )


def _validate_media(
    document: SourceDocument,
    media_artifacts: list[MediaArtifact],
) -> dict[str, MediaArtifact]:
    media_by_id: dict[str, MediaArtifact] = {}
    for media in media_artifacts:
        if media.source_document_id != document.document_id:
            raise MediaJoinMismatchError("media source_document_id mismatch")
        if media.capture_id != document.capture_id:
            raise MediaJoinMismatchError("media capture_id mismatch")
        if media.source_id != document.source_id:
            raise MediaJoinMismatchError("media source_id mismatch")
        media_by_id[media.media_id] = media
    return media_by_id


def _validated_transcript_ref(
    transcript: DraftTranscriptArtifact,
    media_by_id: dict[str, MediaArtifact],
) -> str:
    media = _media_for_ref(transcript.media_id, media_by_id)
    if transcript.source_media_sha256 != media.media_sha256:
        raise MediaJoinMismatchError("transcript source media checksum mismatch")
    if transcript.artifact_path is None:
        raise MediaJoinMismatchError("transcript artifact_path is required")
    return transcript.artifact_path


def _validated_ocr_ref(
    ocr: DraftOCRArtifact,
    media_by_id: dict[str, MediaArtifact],
) -> str:
    media = _media_for_ref(ocr.media_id, media_by_id)
    if ocr.source_media_sha256 != media.media_sha256:
        raise MediaJoinMismatchError("ocr source media checksum mismatch")
    if ocr.artifact_path is None:
        raise MediaJoinMismatchError("ocr artifact_path is required")
    return ocr.artifact_path


def _media_for_ref(
    media_id: str,
    media_by_id: dict[str, MediaArtifact],
) -> MediaArtifact:
    media = media_by_id.get(media_id)
    if media is None:
        raise MediaJoinMismatchError("draft artifact references unknown media_id")
    return media


def _unique(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))
