from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from trader_risk_audit import __version__


REQUIRED_ARTIFACT_NAMES = (
    "source_export",
    "policy_file",
    "normalized_trades",
    "violations",
    "attribution_summary",
    "report_markdown",
)


@dataclass(frozen=True)
class ArtifactRecord:
    name: str
    path: str
    sha256: str


@dataclass(frozen=True)
class AuditManifest:
    manifest_id: str
    package_version: str
    command: str
    command_arguments: tuple[str, ...]
    generated_at: str
    artifacts: tuple[ArtifactRecord, ...]
    content_hash: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


class ManifestValidationError(ValueError):
    pass


class MissingArtifactError(ManifestValidationError):
    pass


def build_audit_manifest(
    *,
    source_export: Path | str,
    policy_file: Path | str,
    normalized_trades: Path | str,
    violations: Path | str,
    attribution_summary: Path | str,
    report_markdown: Path | str,
    delivery_packet: Path | str | None = None,
    command: str = "trader-risk-audit audit",
    command_arguments: tuple[str, ...] = (),
    generated_at: str | None = None,
    package_version: str = __version__,
) -> AuditManifest:
    artifact_paths = {
        "source_export": source_export,
        "policy_file": policy_file,
        "normalized_trades": normalized_trades,
        "violations": violations,
        "attribution_summary": attribution_summary,
        "report_markdown": report_markdown,
    }
    if delivery_packet is not None:
        artifact_paths["delivery_packet"] = delivery_packet

    artifacts = tuple(
        ArtifactRecord(
            name=name,
            path=str(Path(path)),
            sha256=hash_file(path),
        )
        for name, path in artifact_paths.items()
    )
    content_hash = compute_content_hash(
        package_version=package_version,
        artifacts=artifacts,
    )
    return AuditManifest(
        manifest_id=content_hash[:16],
        package_version=package_version,
        command=command,
        command_arguments=tuple(command_arguments),
        generated_at=generated_at or datetime.now(UTC).isoformat(),
        artifacts=artifacts,
        content_hash=content_hash,
    )


def compute_content_hash(
    *,
    package_version: str,
    artifacts: tuple[ArtifactRecord, ...],
) -> str:
    stable_payload = {
        "artifacts": [
            {"name": artifact.name, "sha256": artifact.sha256}
            for artifact in sorted(artifacts, key=lambda item: item.name)
        ],
        "package_version": package_version,
    }
    payload = json.dumps(stable_payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_manifest(manifest: AuditManifest) -> None:
    records_by_name = {artifact.name: artifact for artifact in manifest.artifacts}
    missing_names = [
        name for name in REQUIRED_ARTIFACT_NAMES if name not in records_by_name
    ]
    if missing_names:
        raise MissingArtifactError(
            f"Manifest is missing artifact record: {', '.join(missing_names)}"
        )

    for artifact in manifest.artifacts:
        path = Path(artifact.path)
        if not path.exists():
            raise MissingArtifactError(f"Manifest artifact is absent: {artifact.path}")
        actual_hash = hash_file(path)
        if actual_hash != artifact.sha256:
            raise ManifestValidationError(
                f"Manifest artifact hash drift: {artifact.name}"
            )

    expected_content_hash = compute_content_hash(
        package_version=manifest.package_version,
        artifacts=manifest.artifacts,
    )
    if expected_content_hash != manifest.content_hash:
        raise ManifestValidationError("Manifest content hash drift")


def hash_file(path: Path | str) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as artifact_file:
        for chunk in iter(lambda: artifact_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
