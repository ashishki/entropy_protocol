from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

REQUIRED_CASE_FILES = {
    "source_note": Path("source.md"),
    "policy": Path("policy.yaml"),
    "input_fixture": Path("trades.csv"),
    "report": Path("output/report.md"),
    "reviewed_report": Path("output/report_reviewed.md"),
    "manifest": Path("output/manifest.json"),
    "violations": Path("output/violations.json"),
    "attribution": Path("output/attribution_summary.json"),
    "reproducibility_status": Path("output/reproducibility_status.json"),
}

REQUIRED_MANIFEST_ARTIFACTS = {
    "source_export",
    "policy_file",
    "normalized_trades",
    "violations",
    "attribution_summary",
    "report_markdown",
}

SECRET_PATTERNS = (
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]+"),
    re.compile(r"\blin_api_[A-Za-z0-9_-]+"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]+", re.IGNORECASE),
    re.compile(
        r"\b(api[_-]?key|secret|password|passphrase)\s*[:=]\s*\S+",
        re.IGNORECASE,
    ),
    re.compile(r"\b(signature)\s*[:=]\s*\S+", re.IGNORECASE),
)

PRIVATE_MARKER_PATTERNS = (
    re.compile(r"/home/[^/\s]+/(customers?|clients?|private)/", re.IGNORECASE),
    re.compile(r"/Users/[^/\s]+/(customers?|clients?|private)/", re.IGNORECASE),
    re.compile(
        r"\b[A-Z]:\\Users\\[^\\\s]+\\(customers?|clients?|private)\\",
        re.IGNORECASE,
    ),
    re.compile(r"\btelegram[_ -]?handle\s*[:=]\s*@?[A-Za-z0-9_]{4,}", re.IGNORECASE),
    re.compile(
        r"\b(private|customer|client)[_-]?(account|acct)[_-]?id\s*[:=]\s*\S+",
        re.IGNORECASE,
    ),
    re.compile(r"\bunreviewed[_ -]?(customer|private)\b", re.IGNORECASE),
)

TEXT_SUFFIXES = {".csv", ".json", ".md", ".txt", ".yaml", ".yml"}


@dataclass(frozen=True)
class CasePackIssue:
    code: str
    path: str
    message: str


@dataclass(frozen=True)
class CasePackValidationResult:
    case_id: str
    status: str
    issues: tuple[CasePackIssue, ...]

    @property
    def ok(self) -> bool:
        return self.status == "passed"


def validate_open_source_case_pack(case_dir: str | Path) -> CasePackValidationResult:
    root = Path(case_dir)
    issues: list[CasePackIssue] = []

    if not root.exists() or not root.is_dir():
        return CasePackValidationResult(
            case_id=root.name,
            status="failed",
            issues=(
                CasePackIssue(
                    code="missing_case_dir",
                    path=str(root),
                    message="case directory does not exist",
                ),
            ),
        )

    for label, relative_path in REQUIRED_CASE_FILES.items():
        path = root / relative_path
        if not path.is_file():
            issues.append(
                CasePackIssue(
                    code=f"missing_{label}",
                    path=str(relative_path),
                    message=f"required case-pack file is missing: {relative_path}",
                )
            )

    manifest_path = root / REQUIRED_CASE_FILES["manifest"]
    if manifest_path.is_file():
        issues.extend(_validate_manifest(root, manifest_path))

    reproducibility_path = root / REQUIRED_CASE_FILES["reproducibility_status"]
    if reproducibility_path.is_file():
        issues.extend(_validate_reproducibility_status(reproducibility_path))

    issues.extend(_scan_for_sensitive_markers(root))

    return CasePackValidationResult(
        case_id=root.name,
        status="passed" if not issues else "failed",
        issues=tuple(issues),
    )


def _validate_manifest(root: Path, manifest_path: Path) -> tuple[CasePackIssue, ...]:
    issues: list[CasePackIssue] = []
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return (
            CasePackIssue(
                code="invalid_manifest_json",
                path=str(manifest_path.relative_to(root)),
                message=f"manifest must be valid JSON: {error}",
            ),
        )

    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list):
        return (
            CasePackIssue(
                code="invalid_manifest_artifacts",
                path=str(manifest_path.relative_to(root)),
                message="manifest must contain an artifacts list",
            ),
        )

    artifact_names = {
        str(artifact.get("name"))
        for artifact in artifacts
        if isinstance(artifact, dict) and artifact.get("name")
    }
    missing = sorted(REQUIRED_MANIFEST_ARTIFACTS - artifact_names)
    for name in missing:
        issues.append(
            CasePackIssue(
                code="missing_manifest_artifact",
                path=str(manifest_path.relative_to(root)),
                message=f"manifest missing artifact entry: {name}",
            )
        )

    for artifact in artifacts:
        if not isinstance(artifact, dict):
            continue
        artifact_path = artifact.get("path")
        if not isinstance(artifact_path, str) or not artifact_path.strip():
            issues.append(
                CasePackIssue(
                    code="invalid_manifest_artifact_path",
                    path=str(manifest_path.relative_to(root)),
                    message="manifest artifact path must be a non-empty string",
                )
            )
            continue
        resolved = _resolve_manifest_artifact(root, artifact_path)
        if resolved is not None and not resolved.is_file():
            issues.append(
                CasePackIssue(
                    code="missing_manifest_artifact_file",
                    path=artifact_path,
                    message="manifest artifact path does not exist",
                )
            )

    return tuple(issues)


def _resolve_manifest_artifact(root: Path, artifact_path: str) -> Path | None:
    path = Path(artifact_path)
    if path.is_absolute():
        return None
    parts = path.parts
    if root.name in parts:
        index = parts.index(root.name)
        return root.joinpath(*parts[index + 1 :])
    return root / path


def _validate_reproducibility_status(path: Path) -> tuple[CasePackIssue, ...]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return (
            CasePackIssue(
                code="invalid_reproducibility_json",
                path=str(path),
                message=f"reproducibility status must be valid JSON: {error}",
            ),
        )

    required = ("status", "baseline_content_hash", "rerun_content_hash")
    issues = []
    for field in required:
        if not str(payload.get(field, "")).strip():
            issues.append(
                CasePackIssue(
                    code="invalid_reproducibility_status",
                    path=str(path),
                    message=f"reproducibility status missing field: {field}",
                )
            )
    if payload.get("status") != "passed":
        issues.append(
            CasePackIssue(
                code="reproducibility_not_passed",
                path=str(path),
                message="reproducibility status must be passed for reference packs",
            )
        )
    if payload.get("baseline_content_hash") != payload.get("rerun_content_hash"):
        issues.append(
            CasePackIssue(
                code="reproducibility_hash_mismatch",
                path=str(path),
                message="baseline and rerun content hashes differ",
            )
        )
    return tuple(issues)


def _scan_for_sensitive_markers(root: Path) -> tuple[CasePackIssue, ...]:
    issues: list[CasePackIssue] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = str(path.relative_to(root))
        for pattern in SECRET_PATTERNS:
            if pattern.search(text):
                issues.append(
                    CasePackIssue(
                        code="secret_marker",
                        path=relative,
                        message="file contains a secret-looking field or token",
                    )
                )
                break
        for pattern in PRIVATE_MARKER_PATTERNS:
            if pattern.search(text):
                issues.append(
                    CasePackIssue(
                        code="private_marker",
                        path=relative,
                        message="file contains a private/customer marker",
                    )
                )
                break
    return tuple(issues)
