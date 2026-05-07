from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from trader_risk_audit.workspace import create_audit_workspace

ALLOWED_DOCUMENT_SUFFIXES = frozenset({".csv", ".xlsx", ".yaml", ".yml", ".md", ".txt"})
_SAFE_FILE_NAME = re.compile(r"[^A-Za-z0-9_.-]+")


class TelegramUploadError(ValueError):
    pass


@dataclass(frozen=True)
class TelegramDocumentUpload:
    file_name: str
    content: bytes


@dataclass(frozen=True)
class StoredTelegramAudit:
    audit_id: str
    status: str
    workspace_root: Path
    stored_file: Path


class TelegramAuditStorage:
    def __init__(self, workspace_root: str | Path) -> None:
        self._workspace_root = Path(workspace_root)

    def store_upload(self, upload: TelegramDocumentUpload) -> StoredTelegramAudit:
        safe_name = _safe_upload_name(upload.file_name)
        if not upload.content:
            raise TelegramUploadError("uploaded file must not be empty")
        if _looks_like_credentials(upload.content):
            raise TelegramUploadError("uploaded file appears to contain credentials")

        audit_id = _audit_id(safe_name, upload.content)
        workspace = create_audit_workspace(
            self._workspace_root,
            audit_id,
            status="received",
            file_references={"telegram_upload": f"input/{safe_name}"},
        )
        stored_file = workspace.input_dir / safe_name
        stored_file.write_bytes(upload.content)
        return StoredTelegramAudit(
            audit_id=audit_id,
            status="received",
            workspace_root=workspace.root,
            stored_file=stored_file,
        )


def _safe_upload_name(file_name: str) -> str:
    name = Path(file_name).name.strip()
    if not name:
        raise TelegramUploadError("uploaded file name must not be blank")
    suffix = Path(name).suffix.casefold()
    if suffix not in ALLOWED_DOCUMENT_SUFFIXES:
        raise TelegramUploadError("uploaded file type is not allowed")
    return _SAFE_FILE_NAME.sub("_", name)


def _audit_id(file_name: str, content: bytes) -> str:
    digest = hashlib.sha256(file_name.encode("utf-8") + b"\0" + content).hexdigest()
    return f"audit_{digest[:16]}"


def _looks_like_credentials(content: bytes) -> bool:
    lowered = content[:4096].decode("utf-8", errors="ignore").casefold()
    credential_markers = (
        "api_key=",
        "api key:",
        "secret=",
        "password=",
        "bearer ",
        "seed phrase",
        "private key",
    )
    return any(marker in lowered for marker in credential_markers)
