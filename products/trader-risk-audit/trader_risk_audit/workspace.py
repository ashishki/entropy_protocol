from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from trader_risk_audit.policy.profiles import PolicyProfileSelection

WORKSPACE_DIR_NAMES = ("input", "output", "operator_notes", "artifacts")
DEFAULT_WORKSPACE_STATUS = "intake_received"
_AUDIT_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")


@dataclass(frozen=True)
class AuditWorkspace:
    audit_id: str
    root: Path
    input_dir: Path
    output_dir: Path
    operator_notes_dir: Path
    artifacts_dir: Path
    metadata_path: Path


@dataclass(frozen=True)
class WorkspaceMetadata:
    audit_id: str
    created_at: str
    status: str
    file_references: dict[str, str]
    policy_profile: dict[str, str] | None = None

    def to_json(self) -> str:
        payload = asdict(self)
        if not self.policy_profile:
            payload.pop("policy_profile")
        return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def create_audit_workspace(
    base_dir: str | Path,
    audit_id: str,
    *,
    created_at: datetime | None = None,
    status: str = DEFAULT_WORKSPACE_STATUS,
    file_references: dict[str, str | Path] | None = None,
    policy_profile: PolicyProfileSelection | None = None,
) -> AuditWorkspace:
    _validate_audit_id(audit_id)
    workspace_root = Path(base_dir) / audit_id
    workspace_root.mkdir(parents=True, exist_ok=True)

    directories = {name: workspace_root / name for name in WORKSPACE_DIR_NAMES}
    for directory in directories.values():
        directory.mkdir(parents=True, exist_ok=True)

    workspace = AuditWorkspace(
        audit_id=audit_id,
        root=workspace_root,
        input_dir=directories["input"],
        output_dir=directories["output"],
        operator_notes_dir=directories["operator_notes"],
        artifacts_dir=directories["artifacts"],
        metadata_path=workspace_root / "metadata.json",
    )
    metadata = build_workspace_metadata(
        audit_id=audit_id,
        created_at=created_at,
        status=status,
        file_references=file_references or {},
        policy_profile=policy_profile,
    )
    workspace.metadata_path.write_text(metadata.to_json(), encoding="utf-8")
    return workspace


def build_workspace_metadata(
    *,
    audit_id: str,
    created_at: datetime | None = None,
    status: str = DEFAULT_WORKSPACE_STATUS,
    file_references: dict[str, str | Path] | None = None,
    policy_profile: PolicyProfileSelection | None = None,
) -> WorkspaceMetadata:
    _validate_audit_id(audit_id)
    timestamp = (created_at or datetime.now(UTC)).astimezone(UTC).isoformat()
    return WorkspaceMetadata(
        audit_id=audit_id,
        created_at=timestamp,
        status=_safe_text(status, field="status"),
        file_references={
            _safe_text(label, field="file reference label"): _safe_file_reference(path)
            for label, path in sorted((file_references or {}).items())
        },
        policy_profile=_safe_policy_profile(policy_profile),
    )


def _validate_audit_id(audit_id: str) -> None:
    if _AUDIT_ID_PATTERN.fullmatch(audit_id) is None:
        raise ValueError(
            "audit_id must use only letters, numbers, dot, underscore, or hyphen"
        )


def _safe_text(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must not be blank")
    if "\n" in text or "\r" in text:
        raise ValueError(f"{field} must be a single line")
    return text


def _safe_file_reference(value: str | Path) -> str:
    text = _safe_text(str(value), field="file reference")
    if Path(text).is_absolute():
        return Path(text).name
    return text


def _safe_policy_profile(
    selection: PolicyProfileSelection | None,
) -> dict[str, str] | None:
    if selection is None:
        return None
    return {
        _safe_text(label, field="policy profile metadata label"): _safe_text(
            value,
            field="policy profile metadata value",
        )
        for label, value in selection.to_metadata().items()
    }
