from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

from trader_risk_audit.artifacts.manifest import (
    MissingArtifactError,
    build_audit_manifest,
    hash_file,
    validate_manifest,
)


def test_manifest_records_required_artifact_hashes(tmp_path: Path) -> None:
    artifacts = _artifact_paths(tmp_path)
    manifest = build_audit_manifest(
        **artifacts,
        delivery_packet=_write(tmp_path / "delivery.txt", "delivery"),
        command_arguments=("--trades", "source.csv"),
        generated_at="2026-05-07T12:00:00+00:00",
    )

    records = {artifact.name: artifact for artifact in manifest.artifacts}

    assert set(records) == {
        "source_export",
        "policy_file",
        "normalized_trades",
        "violations",
        "attribution_summary",
        "report_markdown",
        "delivery_packet",
    }
    assert records["source_export"].sha256 == _sha256("source")
    assert records["policy_file"].sha256 == hash_file(artifacts["policy_file"])
    assert manifest.package_version == "0.1.0"
    assert manifest.command_arguments == ("--trades", "source.csv")
    validate_manifest(manifest)


def test_content_hash_excludes_generation_timestamp(tmp_path: Path) -> None:
    artifacts = _artifact_paths(tmp_path)

    first = build_audit_manifest(
        **artifacts,
        generated_at="2026-05-07T12:00:00+00:00",
        package_version="0.1.0",
    )
    second = build_audit_manifest(
        **artifacts,
        generated_at="2026-05-07T12:05:00+00:00",
        package_version="0.1.0",
    )
    changed_version = build_audit_manifest(
        **artifacts,
        generated_at="2026-05-07T12:05:00+00:00",
        package_version="0.1.1",
    )

    assert first.generated_at != second.generated_at
    assert first.content_hash == second.content_hash
    assert first.content_hash != changed_version.content_hash


def test_manifest_validation_fails_for_missing_artifact(tmp_path: Path) -> None:
    artifacts = _artifact_paths(tmp_path)
    manifest = build_audit_manifest(**artifacts)
    missing_report = tmp_path / "missing_report.md"
    broken_manifest = replace(
        manifest,
        artifacts=tuple(
            replace(artifact, path=str(missing_report))
            if artifact.name == "report_markdown"
            else artifact
            for artifact in manifest.artifacts
        ),
    )

    with pytest.raises(MissingArtifactError, match="absent"):
        validate_manifest(broken_manifest)


def _artifact_paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "source_export": _write(tmp_path / "source.csv", "source"),
        "policy_file": _write(tmp_path / "policy.yaml", "policy"),
        "normalized_trades": _write(tmp_path / "normalized.json", "normalized"),
        "violations": _write(tmp_path / "violations.json", "violations"),
        "attribution_summary": _write(tmp_path / "attribution.json", "attribution"),
        "report_markdown": _write(tmp_path / "report.md", "report"),
    }


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path


def _sha256(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()
