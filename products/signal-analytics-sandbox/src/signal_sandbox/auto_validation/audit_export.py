"""Persist auto-validation audit logs with Core-compatible proof receipts."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from signal_sandbox.auto_validation.core_receipt import (
    SignalAutoValidationProofReceipt,
    build_signal_auto_validation_receipt,
)
from signal_sandbox.auto_validation.evidence import AutoValidationEvidenceBundle
from signal_sandbox.auto_validation.results import ValidationAuditLog


@dataclass(frozen=True)
class ValidationAuditExport:
    audit_log_path: Path
    receipt_path: Path
    audit_sha256: str
    receipt_sha256: str


def export_validation_audit_with_receipt(
    *,
    bundle: AutoValidationEvidenceBundle,
    audit: ValidationAuditLog,
    output_dir: Path,
    stem: str | None = None,
    generated_at_utc: datetime | None = None,
) -> ValidationAuditExport:
    """Write an audit log and its proof receipt as sibling JSON artifacts."""

    artifact_stem = _artifact_stem(stem or audit.audit_id)
    receipt = build_signal_auto_validation_receipt(
        bundle=bundle,
        audit=audit,
        generated_at_utc=generated_at_utc,
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    audit_log_path = output_dir / f"{artifact_stem}.audit.json"
    receipt_path = output_dir / f"{artifact_stem}.receipt.json"
    audit_log_path.write_text(audit.canonical_json() + "\n", encoding="utf-8")
    receipt_path.write_text(receipt.canonical_json() + "\n", encoding="utf-8")

    return ValidationAuditExport(
        audit_log_path=audit_log_path,
        receipt_path=receipt_path,
        audit_sha256=audit.audit_sha256(),
        receipt_sha256=receipt.receipt_sha256(),
    )


def load_signal_auto_validation_receipt(path: Path) -> SignalAutoValidationProofReceipt:
    """Load a persisted proof receipt from its JSON artifact."""

    return SignalAutoValidationProofReceipt.model_validate(
        json.loads(path.read_text(encoding="utf-8"))
    )


def _artifact_stem(value: str) -> str:
    if not value or Path(value).name != value or value in {".", ".."}:
        raise ValueError("artifact stem must be a single file-name component")
    return value
