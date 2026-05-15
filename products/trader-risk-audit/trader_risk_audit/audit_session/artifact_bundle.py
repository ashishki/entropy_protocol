from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from trader_risk_audit.artifacts.manifest import hash_file

BUNDLE_FILE_NAME = "bundle_index.json"
BUNDLE_SCHEMA_VERSION = "1"
REQUIRED_COMPLETE_ARTIFACTS = (
    "run_status",
    "manifest",
    "normalized_trades",
    "violations",
    "attribution_summary",
    "report_markdown",
    "delivery_packet",
)
_SAFE_REF_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-"
)
_SAFE_LABEL_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-"
)


class ArtifactBundleError(ValueError):
    pass


class BundleValidationError(ArtifactBundleError):
    pass


class MissingBundleArtifactError(BundleValidationError):
    pass


@dataclass(frozen=True)
class BundleArtifactRecord:
    name: str
    ref: str
    sha256: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class ArtifactBundleIndex:
    schema_version: str
    bundle_id: str
    status: str
    reason_code: str | None
    input_refs: dict[str, str]
    preview_state: dict[str, str | None]
    artifacts: tuple[BundleArtifactRecord, ...]
    limitation_registers: tuple[BundleArtifactRecord, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "artifacts": [artifact.to_dict() for artifact in self.artifacts],
            "bundle_id": self.bundle_id,
            "input_refs": dict(self.input_refs),
            "limitation_registers": [
                artifact.to_dict() for artifact in self.limitation_registers
            ],
            "preview_state": dict(self.preview_state),
            "reason_code": self.reason_code,
            "schema_version": self.schema_version,
            "status": self.status,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def build_artifact_bundle_index(
    *,
    run_dir: str | Path,
    preview_status: str = "not_generated",
    preview_ref: str | None = None,
    limitation_registers: tuple[str | Path, ...] = (),
) -> ArtifactBundleIndex:
    root = Path(run_dir)
    run_status_path = root / "run_status.json"
    run_status = _load_json_object(run_status_path)
    status = _safe_label(run_status.get("status"), "unknown")
    reason_code = _optional_safe_label(run_status.get("reason_code"))
    artifact_refs = _artifact_refs_from_status(run_status)

    artifacts = [
        _record_artifact("run_status", run_status_path, root),
    ]
    manifest_ref = artifact_refs.get("manifest")
    if manifest_ref is not None:
        artifacts.append(_record_artifact("manifest", root / manifest_ref, root))
    for name in (
        "normalized_trades",
        "violations",
        "attribution_summary",
        "report_markdown",
        "delivery_packet",
    ):
        ref = artifact_refs.get(name)
        if ref is not None:
            artifacts.append(_record_artifact(name, root / ref, root))

    limitation_records = tuple(
        _record_artifact(Path(path).stem, Path(path), root)
        for path in limitation_registers
    )
    bundle_without_id = ArtifactBundleIndex(
        schema_version=BUNDLE_SCHEMA_VERSION,
        bundle_id="",
        status=status,
        reason_code=reason_code,
        input_refs={
            "policy": _safe_file_ref(run_status.get("policy_ref"), "policy_file"),
            "source_export": _safe_file_ref(
                run_status.get("source_export_ref"),
                "source_export",
            ),
        },
        preview_state={
            "status": _safe_label(preview_status, "not_generated"),
            "ref": _safe_ref(preview_ref) if preview_ref else None,
        },
        artifacts=tuple(artifacts),
        limitation_registers=limitation_records,
    )
    bundle_id = _bundle_id(bundle_without_id)
    return ArtifactBundleIndex(
        **{
            **bundle_without_id.to_dict(),
            "artifacts": bundle_without_id.artifacts,
            "limitation_registers": bundle_without_id.limitation_registers,
            "bundle_id": bundle_id,
        }
    )


def write_artifact_bundle_index(
    bundle: ArtifactBundleIndex,
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(bundle.to_json(), encoding="utf-8")
    return path


def load_artifact_bundle_index(path: str | Path) -> ArtifactBundleIndex:
    payload = _load_json_object(Path(path))
    artifacts = tuple(
        _record_from_payload(record, field="artifacts")
        for record in payload.get("artifacts", ())
    )
    limitation_registers = tuple(
        _record_from_payload(record, field="limitation_registers")
        for record in payload.get("limitation_registers", ())
    )
    return ArtifactBundleIndex(
        schema_version=_safe_label(payload.get("schema_version"), "unknown"),
        bundle_id=_safe_label(payload.get("bundle_id"), "unknown"),
        status=_safe_label(payload.get("status"), "unknown"),
        reason_code=_optional_safe_label(payload.get("reason_code")),
        input_refs={
            "policy": _safe_file_ref(
                dict(payload.get("input_refs", {})).get("policy"),
                "policy_file",
            ),
            "source_export": _safe_file_ref(
                dict(payload.get("input_refs", {})).get("source_export"),
                "source_export",
            ),
        },
        preview_state=_preview_state_from_payload(payload.get("preview_state", {})),
        artifacts=artifacts,
        limitation_registers=limitation_registers,
    )


def validate_artifact_bundle_index(
    bundle_path: str | Path,
) -> ArtifactBundleIndex:
    path = Path(bundle_path)
    bundle = load_artifact_bundle_index(path)
    root = path.parent
    artifacts_by_name = {artifact.name: artifact for artifact in bundle.artifacts}
    if bundle.status == "complete":
        missing = [
            name
            for name in REQUIRED_COMPLETE_ARTIFACTS
            if name not in artifacts_by_name
        ]
        if missing:
            raise MissingBundleArtifactError(
                f"bundle missing required artifacts: {', '.join(missing)}"
            )

    for artifact in bundle.artifacts + bundle.limitation_registers:
        artifact_path = _resolve_bundle_ref(root, artifact.ref)
        if not artifact_path.exists():
            raise MissingBundleArtifactError(
                f"bundle artifact is absent: {artifact.name}"
            )
        actual_hash = hash_file(artifact_path)
        if actual_hash != artifact.sha256:
            raise BundleValidationError(f"bundle artifact hash drift: {artifact.name}")
    return bundle


def format_bundle_summary(bundle: ArtifactBundleIndex, bundle_path: str | Path) -> str:
    return "\n".join(
        (
            f"Bundle ID: {bundle.bundle_id}",
            f"Status: {bundle.status}",
            f"Bundle index: {Path(bundle_path).name}",
            f"Artifacts: {len(bundle.artifacts)}",
            f"Limitation registers: {len(bundle.limitation_registers)}",
            f"Preview state: {bundle.preview_state['status']}",
        )
    )


def _load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ArtifactBundleError("bundle input must contain a JSON object")
    return payload


def _artifact_refs_from_status(run_status: dict[str, Any]) -> dict[str, str]:
    raw_artifacts = run_status.get("artifacts")
    if not isinstance(raw_artifacts, dict):
        return {}
    return {
        str(name): _safe_ref(ref)
        for name, ref in raw_artifacts.items()
        if isinstance(name, str) and isinstance(ref, str)
    }


def _record_artifact(name: str, path: Path, root: Path) -> BundleArtifactRecord:
    return BundleArtifactRecord(
        name=_safe_label(name, "artifact"),
        ref=_relative_ref(path, root),
        sha256=hash_file(path),
    )


def _record_from_payload(payload: object, *, field: str) -> BundleArtifactRecord:
    if not isinstance(payload, dict):
        raise ArtifactBundleError(f"{field} entries must be JSON objects")
    return BundleArtifactRecord(
        name=_safe_label(payload.get("name"), "artifact"),
        ref=_safe_ref(payload.get("ref")),
        sha256=_safe_hash(payload.get("sha256")),
    )


def _preview_state_from_payload(payload: object) -> dict[str, str | None]:
    if not isinstance(payload, dict):
        return {"status": "not_generated", "ref": None}
    ref = payload.get("ref")
    return {
        "status": _safe_label(payload.get("status"), "not_generated"),
        "ref": _safe_ref(ref) if ref else None,
    }


def _relative_ref(path: Path, root: Path) -> str:
    try:
        ref = path.relative_to(root).as_posix()
    except ValueError as error:
        raise ArtifactBundleError(
            "bundle artifact must be inside run directory"
        ) from error
    return _safe_ref(ref)


def _resolve_bundle_ref(root: Path, ref: str) -> Path:
    safe_ref = _safe_ref(ref)
    ref_path = Path(safe_ref)
    if ref_path.is_absolute() or ".." in ref_path.parts:
        raise BundleValidationError("unsafe bundle artifact ref")
    return root / ref_path


def _bundle_id(bundle: ArtifactBundleIndex) -> str:
    payload = bundle.to_dict()
    payload.pop("bundle_id", None)
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]


def _safe_ref(value: object) -> str:
    if isinstance(value, str) and value.strip():
        normalized = value.strip().replace("\\", "/")
        if (
            len(normalized) <= 160
            and not normalized.startswith("/")
            and ".." not in Path(normalized).parts
            and all(character in _SAFE_REF_CHARS for character in normalized)
        ):
            return normalized
    raise ArtifactBundleError("unsafe artifact ref")


def _safe_file_ref(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        try:
            return Path(_safe_ref(Path(value).name)).name
        except ArtifactBundleError:
            pass
    return fallback


def _safe_label(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        normalized = value.strip()
        if len(normalized) <= 128 and all(
            character in _SAFE_LABEL_CHARS for character in normalized
        ):
            return normalized
    return fallback


def _optional_safe_label(value: object) -> str | None:
    if value is None:
        return None
    return _safe_label(value, "unknown")


def _safe_hash(value: object) -> str:
    if isinstance(value, str) and len(value) == 64:
        normalized = value.lower()
        if all(character in "0123456789abcdef" for character in normalized):
            return normalized
    raise ArtifactBundleError("unsafe artifact hash")
