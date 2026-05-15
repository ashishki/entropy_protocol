from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from trader_risk_audit.artifacts.manifest import ArtifactRecord, compute_content_hash
from trader_risk_audit.audit_session.runner import (
    AuditSessionRunnerError,
    run_audit_session,
)

REPRODUCIBILITY_STATUS_FILE = "reproducibility_status.json"


class ReproducibilityGateError(ValueError):
    pass


@dataclass(frozen=True)
class ReproducibilityGateResult:
    status: str
    preview_status: str
    reason_code: str | None
    baseline_content_hash: str
    rerun_content_hash: str
    mismatched_artifacts: tuple[str, ...]
    artifact_refs: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        return {
            "artifact_refs": dict(self.artifact_refs),
            "baseline_content_hash": self.baseline_content_hash,
            "mismatched_artifacts": list(self.mismatched_artifacts),
            "preview_status": self.preview_status,
            "reason_code": self.reason_code,
            "rerun_content_hash": self.rerun_content_hash,
            "status": self.status,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def run_reproducibility_gate(
    *,
    session_path: str | Path,
    policy_path: str | Path,
    input_dir: str | Path,
    baseline_run_dir: str | Path,
    rerun_dir: str | Path,
    policy_status: str = "approved",
) -> ReproducibilityGateResult:
    baseline_root = Path(baseline_run_dir)
    rerun_root = Path(rerun_dir)
    baseline_manifest_path = baseline_root / "manifest.json"
    status_path = baseline_root / REPRODUCIBILITY_STATUS_FILE
    baseline_manifest = _load_manifest_payload(baseline_manifest_path)

    try:
        rerun = run_audit_session(
            session_path=session_path,
            policy_path=policy_path,
            input_dir=input_dir,
            output_dir=rerun_root,
            policy_status=policy_status,
        )
    except AuditSessionRunnerError as error:
        result = ReproducibilityGateResult(
            status="blocked",
            preview_status="blocked_reproducibility",
            reason_code=error.reason_code,
            baseline_content_hash=stable_manifest_content_hash(baseline_manifest),
            rerun_content_hash="",
            mismatched_artifacts=(),
            artifact_refs={
                "baseline_manifest": "manifest.json",
                "rerun_status": _safe_run_ref(rerun_root, "run_status.json"),
            },
        )
        _write_status(status_path, result)
        return result

    if rerun.status != "complete":
        result = ReproducibilityGateResult(
            status="blocked",
            preview_status="blocked_reproducibility",
            reason_code=rerun.reason_code or "rerun_not_complete",
            baseline_content_hash=stable_manifest_content_hash(baseline_manifest),
            rerun_content_hash="",
            mismatched_artifacts=(),
            artifact_refs={
                "baseline_manifest": "manifest.json",
                "rerun_status": _safe_run_ref(rerun_root, "run_status.json"),
            },
        )
        _write_status(status_path, result)
        return result

    rerun_manifest_path = rerun_root / "manifest.json"
    rerun_manifest = _load_manifest_payload(rerun_manifest_path)
    result = compare_manifest_payloads(
        baseline_manifest,
        rerun_manifest,
        baseline_manifest_ref="manifest.json",
        rerun_manifest_ref=_safe_run_ref(rerun_root, "manifest.json"),
    )
    _write_status(status_path, result)
    return result


def compare_manifest_payloads(
    baseline_manifest: dict[str, Any],
    rerun_manifest: dict[str, Any],
    *,
    baseline_manifest_ref: str = "baseline/manifest.json",
    rerun_manifest_ref: str = "rerun/manifest.json",
) -> ReproducibilityGateResult:
    baseline_hash = stable_manifest_content_hash(baseline_manifest)
    rerun_hash = stable_manifest_content_hash(rerun_manifest)
    mismatched_artifacts = _mismatched_artifacts(baseline_manifest, rerun_manifest)
    matched = baseline_hash == rerun_hash
    return ReproducibilityGateResult(
        status="passed" if matched else "blocked",
        preview_status="ready_for_preview" if matched else "blocked_reproducibility",
        reason_code=None if matched else "content_hash_mismatch",
        baseline_content_hash=baseline_hash,
        rerun_content_hash=rerun_hash,
        mismatched_artifacts=mismatched_artifacts,
        artifact_refs={
            "baseline_manifest": _safe_ref(baseline_manifest_ref),
            "rerun_manifest": _safe_ref(rerun_manifest_ref),
        },
    )


def stable_manifest_content_hash(manifest_payload: dict[str, Any]) -> str:
    package_version = str(manifest_payload.get("package_version", "unknown"))
    artifacts = tuple(
        ArtifactRecord(
            name=str(artifact["name"]),
            path="",
            sha256=str(artifact["sha256"]),
        )
        for artifact in _manifest_artifacts(manifest_payload)
    )
    return compute_content_hash(
        package_version=package_version,
        artifacts=artifacts,
    )


def _load_manifest_payload(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ReproducibilityGateError("manifest must contain a JSON object")
    return payload


def _manifest_artifacts(manifest_payload: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    artifacts = manifest_payload.get("artifacts")
    if not isinstance(artifacts, list) or not all(
        isinstance(artifact, dict) for artifact in artifacts
    ):
        raise ReproducibilityGateError("manifest artifacts must be JSON objects")
    return tuple(artifacts)


def _mismatched_artifacts(
    baseline_manifest: dict[str, Any],
    rerun_manifest: dict[str, Any],
) -> tuple[str, ...]:
    baseline = {
        str(artifact["name"]): str(artifact["sha256"])
        for artifact in _manifest_artifacts(baseline_manifest)
    }
    rerun = {
        str(artifact["name"]): str(artifact["sha256"])
        for artifact in _manifest_artifacts(rerun_manifest)
    }
    names = sorted(set(baseline) | set(rerun))
    return tuple(name for name in names if baseline.get(name) != rerun.get(name))


def _write_status(path: Path, result: ReproducibilityGateResult) -> None:
    path.write_text(result.to_json(), encoding="utf-8")


def _safe_run_ref(root: Path, filename: str) -> str:
    return _safe_ref(f"{root.name}/{filename}")


def _safe_ref(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("/") or ".." in Path(normalized).parts:
        raise ReproducibilityGateError("unsafe reproducibility artifact ref")
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-"
    if not normalized or len(normalized) > 160:
        raise ReproducibilityGateError("unsafe reproducibility artifact ref")
    if any(character not in allowed for character in normalized):
        raise ReproducibilityGateError("unsafe reproducibility artifact ref")
    return normalized
