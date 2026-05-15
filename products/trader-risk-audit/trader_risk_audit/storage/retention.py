from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from trader_risk_audit.artifacts.manifest import ArtifactRecord, AuditManifest


@dataclass(frozen=True)
class RetentionListItem:
    manifest_id: str
    artifact_count: int
    created_timestamp: str
    report_path: str


@dataclass(frozen=True)
class DeletionResult:
    referenced_paths: tuple[str, ...]
    removed_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    dry_run: bool


def load_manifest(path: str | Path) -> AuditManifest:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return AuditManifest(
        manifest_id=str(payload["manifest_id"]),
        package_version=str(payload["package_version"]),
        command=str(payload["command"]),
        command_arguments=tuple(str(item) for item in payload["command_arguments"]),
        generated_at=str(payload["generated_at"]),
        artifacts=tuple(
            ArtifactRecord(
                name=str(artifact["name"]),
                path=str(artifact["path"]),
                sha256=str(artifact["sha256"]),
            )
            for artifact in payload["artifacts"]
        ),
        content_hash=str(payload["content_hash"]),
    )


def retention_list_items(
    manifest_paths: tuple[str | Path, ...],
) -> tuple[RetentionListItem, ...]:
    return tuple(
        _retention_list_item(load_manifest(path))
        for path in sorted(manifest_paths, key=lambda item: str(item))
    )


def format_retention_list(manifest_paths: tuple[str | Path, ...]) -> str:
    lines = [
        "manifest_id\tartifact_count\tcreated_timestamp\treport_path",
        *(
            "\t".join(
                (
                    item.manifest_id,
                    str(item.artifact_count),
                    item.created_timestamp,
                    item.report_path,
                )
            )
            for item in retention_list_items(manifest_paths)
        ),
    ]
    return "\n".join(lines) + "\n"


def delete_manifest_artifacts(
    manifest_path: str | Path,
    *,
    dry_run: bool,
    confirm_delete: bool = False,
) -> DeletionResult:
    manifest = load_manifest(manifest_path)
    referenced_paths = tuple(artifact.path for artifact in manifest.artifacts)
    if dry_run:
        return DeletionResult(
            referenced_paths=referenced_paths,
            removed_paths=(),
            missing_paths=(),
            dry_run=True,
        )
    if not confirm_delete:
        raise ValueError("confirmed deletion requires confirm_delete=True")

    removed: list[str] = []
    missing: list[str] = []
    for raw_path in referenced_paths:
        path = Path(raw_path)
        if path.exists():
            path.unlink()
            removed.append(raw_path)
        else:
            missing.append(raw_path)
    return DeletionResult(
        referenced_paths=referenced_paths,
        removed_paths=tuple(removed),
        missing_paths=tuple(missing),
        dry_run=False,
    )


def _retention_list_item(manifest: AuditManifest) -> RetentionListItem:
    report_path = next(
        (
            artifact.path
            for artifact in manifest.artifacts
            if artifact.name == "report_markdown"
        ),
        "",
    )
    return RetentionListItem(
        manifest_id=manifest.manifest_id,
        artifact_count=len(manifest.artifacts),
        created_timestamp=manifest.generated_at,
        report_path=report_path,
    )
