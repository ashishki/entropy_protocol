from __future__ import annotations

import subprocess
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path

from signal_sandbox.cli import PLANNED_SUBCOMMANDS
from signal_sandbox.media import (
    MediaArtifact,
    MediaModality,
    RetentionState,
    build_media_manifest,
)

SCRIPT_PATH = Path(sys.executable).with_name("signal-sandbox")


def run_cli(
    *args: str,
    env: Mapping[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(SCRIPT_PATH), *args],
        capture_output=True,
        env=env,
        text=True,
        check=False,
    )


def test_help_lists_subcommands() -> None:
    result = run_cli("--help")

    assert result.returncode == 0
    for subcommand in PLANNED_SUBCOMMANDS:
        assert subcommand in result.stdout


def test_unimplemented_subcommands_exit_2() -> None:
    implemented = {
        "extract",
        "report",
        "review",
        "santiment-context",
        "snapshot",
        "status",
        "transcribe-media",
    }
    unimplemented = [
        command for command in PLANNED_SUBCOMMANDS if command not in implemented
    ]

    for command in unimplemented:
        result = run_cli(command)
        combined_output = result.stdout + result.stderr
        assert result.returncode == 2, command
        assert "not implemented" in combined_output


def test_status_exits_zero(tmp_path: Path) -> None:
    result = run_cli(
        "status",
        env={"SIGNAL_SANDBOX_WORKSPACE": str(tmp_path)},
    )

    assert result.returncode == 0
    assert "status: ok" in result.stdout


def test_transcribe_media_honors_gates_without_provider_call(tmp_path: Path) -> None:
    media_path = tmp_path / "voice.ogg"
    media_bytes = b"voice bytes"
    media_path.write_bytes(media_bytes)
    manifest_path = tmp_path / "manifest.json"
    manifest = build_media_manifest(
        [
            MediaArtifact(
                media_id="voice_1",
                source_id="bablos79",
                capture_id="bablos79-10476",
                source_document_id="bablos79:bablos79-10476",
                source_timestamp_utc=datetime(2026, 4, 30, 7, 34, tzinfo=UTC),
                modality=MediaModality.VOICE,
                original_url_or_file_id="https://t.me/bablos79/10476",
                local_path=str(media_path),
                media_sha256="00" * 32,
                mime_type="audio/ogg",
                duration_seconds=275,
                retention_state=RetentionState.TEMPORARY,
                created_at_utc=datetime(2026, 5, 14, 0, 0, tzinfo=UTC),
            )
        ]
    )
    manifest.write_json(manifest_path)

    result = run_cli(
        "transcribe-media",
        "--media-manifest",
        str(manifest_path),
        "--output-dir",
        str(tmp_path / "transcripts"),
    )

    assert result.returncode == 0
    assert "voice/audio rows: 1" in result.stdout
    assert "draft transcripts: 0" in result.stdout
    assert "voice_1: skipped:environment_disabled" in result.stdout
    assert "approval: missing --approve" in result.stderr


def test_santiment_context_honors_approval_gate_without_provider_call(
    tmp_path: Path,
) -> None:
    bundle_path = tmp_path / "bundle.json"
    bundle_path.write_text("{}", encoding="utf-8")

    result = run_cli(
        "santiment-context",
        "--bundle",
        str(bundle_path),
        "--output-dir",
        str(tmp_path / "santiment"),
    )

    assert result.returncode == 2
    assert "approval: missing --approve" in result.stderr
