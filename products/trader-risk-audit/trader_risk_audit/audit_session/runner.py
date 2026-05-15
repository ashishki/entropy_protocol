from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from trader_risk_audit.artifacts.manifest import build_audit_manifest, hash_file
from trader_risk_audit.evaluation.attribution import (
    attribute_pnl,
    ensure_reconciled,
    serialize_attribution,
)
from trader_risk_audit.evaluation.rules import (
    evaluate_loss_rules,
    evaluate_position_asset_rules,
)
from trader_risk_audit.evaluation.violations import serialize_violations
from trader_risk_audit.policy.review import build_review_packet
from trader_risk_audit.policy.schema import load_policy
from trader_risk_audit.policy.validation import ensure_policy_ready_for_evaluation
from trader_risk_audit.reporting.claim_guard import ensure_report_claims_valid
from trader_risk_audit.reporting.delivery import render_delivery_packet
from trader_risk_audit.reporting.markdown import render_markdown_report
from trader_risk_audit.reporting.model import build_report_model
from trader_risk_audit.trades.importers import normalize_csv, serialize_trade_records

RUNNABLE_INTAKE_STATUS = "ready_for_audit"
RUNNABLE_POLICY_STATUSES = frozenset(
    {
        "approved",
        "ready_for_audit",
        "ready_for_evaluation",
    }
)
STATUS_FILE_NAME = "run_status.json"
_SAFE_LABEL_CHARS = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._:-"
)
_SAFE_FILE_REF_CHARS = _SAFE_LABEL_CHARS | frozenset("-")


class AuditSessionRunnerError(RuntimeError):
    def __init__(self, reason_code: str) -> None:
        self.reason_code = reason_code
        super().__init__(reason_code)


@dataclass(frozen=True)
class AuditSessionRunResult:
    status: str
    reason_code: str | None
    status_path: Path
    artifacts: dict[str, str]


@dataclass(frozen=True)
class _AuditArtifacts:
    audit_id: str
    artifact_refs: dict[str, str]


def run_audit_session(
    *,
    session_path: str | Path,
    policy_path: str | Path,
    input_dir: str | Path,
    output_dir: str | Path,
    policy_status: str = "approved",
) -> AuditSessionRunResult:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    status_path = output_path / STATUS_FILE_NAME
    policy_file = Path(policy_path)

    try:
        session_payload = _load_session(session_path)
        source_ref = _source_export_ref(session_payload)
        trades_path = _resolve_input_path(input_dir, source_ref)
        intake_status = _safe_label(session_payload.get("status"), "unknown")
        normalized_policy_status = _safe_label(
            policy_status.strip().casefold(), "unknown"
        )

        base_status = {
            "intake_session_id": _safe_label(
                session_payload.get("session_id"),
                "unknown",
            ),
            "intake_status": intake_status,
            "policy_ref": _safe_file_ref(policy_file.name, "policy_file"),
            "policy_status": normalized_policy_status,
            "source_export_ref": _safe_file_ref(
                Path(source_ref).name,
                "source_export",
            ),
        }

        if intake_status != RUNNABLE_INTAKE_STATUS:
            return _write_status(
                status_path,
                {
                    **base_status,
                    "status": "blocked",
                    "reason_code": "intake_not_ready",
                    "artifacts": {},
                },
            )
        if normalized_policy_status not in RUNNABLE_POLICY_STATUSES:
            return _write_status(
                status_path,
                {
                    **base_status,
                    "status": "blocked",
                    "reason_code": "policy_not_ready",
                    "artifacts": {},
                },
            )

        artifacts = _run_deterministic_audit(
            trades_path=trades_path,
            policy_path=policy_file,
            output_dir=output_path,
        )
        return _write_status(
            status_path,
            {
                **base_status,
                "status": "complete",
                "reason_code": None,
                "audit_id": artifacts.audit_id,
                "artifacts": artifacts.artifact_refs,
            },
        )
    except AuditSessionRunnerError as error:
        _write_status(
            status_path,
            {
                "status": "failed",
                "reason_code": error.reason_code,
                "artifacts": {},
            },
        )
        raise
    except Exception as error:
        _write_status(
            status_path,
            {
                "status": "failed",
                "reason_code": "audit_generation_failed",
                "error_type": type(error).__name__,
                "artifacts": {},
            },
        )
        raise AuditSessionRunnerError("audit_generation_failed") from error


def _load_session(session_path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(session_path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise AuditSessionRunnerError("invalid_intake_session")
    return payload


def _source_export_ref(session_payload: dict[str, Any]) -> str:
    file_references = session_payload.get("file_references")
    if not isinstance(file_references, dict):
        raise AuditSessionRunnerError("missing_file_references")
    source_ref = file_references.get("source_export")
    if not isinstance(source_ref, str) or not source_ref.strip():
        raise AuditSessionRunnerError("missing_source_export")
    return source_ref


def _resolve_input_path(input_dir: str | Path, source_ref: str) -> Path:
    source_path = Path(source_ref)
    if source_path.is_absolute():
        raise AuditSessionRunnerError("unsafe_source_export_ref")

    root = Path(input_dir)
    candidates = (
        root / source_path,
        root / source_path.name,
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise AuditSessionRunnerError("missing_source_export_file")


def _run_deterministic_audit(
    *,
    trades_path: Path,
    policy_path: Path,
    output_dir: Path,
) -> _AuditArtifacts:
    trades = normalize_csv(trades_path)
    policy = load_policy(policy_path)
    ensure_policy_ready_for_evaluation(policy, build_review_packet(policy))

    position_asset_result = evaluate_position_asset_rules(trades, policy)
    loss_result = evaluate_loss_rules(trades, policy)
    violations = tuple(
        sorted(
            position_asset_result.violations + loss_result.violations,
            key=lambda item: (item.timestamp, item.rule_id, item.source_row_ids),
        )
    )
    warnings = tuple(
        sorted(
            position_asset_result.warnings + loss_result.warnings,
            key=lambda item: (item.rule_id, item.message_code),
        )
    )
    attribution = ensure_reconciled(attribute_pnl(trades, violations))
    report_model = build_report_model(
        trades=trades,
        policy=policy,
        violations=violations,
        warnings=warnings,
        attribution=attribution,
    )
    report = render_markdown_report(report_model)
    ensure_report_claims_valid(report)

    normalized_path = output_dir / "normalized_trades.json"
    violations_path = output_dir / "violations.json"
    attribution_path = output_dir / "attribution_summary.json"
    report_path = output_dir / "report.md"
    delivery_packet_path = output_dir / "telegram_packet.txt"
    manifest_path = output_dir / "manifest.json"

    audit_id = _audit_id(trades_path, policy_path)
    normalized_path.write_text(serialize_trade_records(trades), encoding="utf-8")
    violations_path.write_text(
        serialize_violations(audit_id, violations),
        encoding="utf-8",
    )
    attribution_path.write_text(
        serialize_attribution(attribution),
        encoding="utf-8",
    )
    report_path.write_text(report, encoding="utf-8")
    delivery_packet_path.write_text(
        render_delivery_packet(
            model=report_model,
            report_text=report,
            report_path=report_path.name,
        ),
        encoding="utf-8",
    )

    manifest = build_audit_manifest(
        source_export=trades_path,
        policy_file=policy_path,
        normalized_trades=normalized_path,
        violations=violations_path,
        attribution_summary=attribution_path,
        report_markdown=report_path,
        delivery_packet=delivery_packet_path,
        command="trader-risk-audit audit-session run",
        command_arguments=(
            "--session",
            "<intake_session>",
            "--policy",
            policy_path.name,
            "--input-dir",
            "<input_dir>",
            "--output-dir",
            "<output_dir>",
        ),
    )
    manifest_path.write_text(manifest.to_json(), encoding="utf-8")

    return _AuditArtifacts(
        audit_id=audit_id,
        artifact_refs={
            "normalized_trades": normalized_path.name,
            "violations": violations_path.name,
            "attribution_summary": attribution_path.name,
            "report_markdown": report_path.name,
            "delivery_packet": delivery_packet_path.name,
            "manifest": manifest_path.name,
        },
    )


def _write_status(
    status_path: Path,
    payload: dict[str, Any],
) -> AuditSessionRunResult:
    status_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return AuditSessionRunResult(
        status=str(payload["status"]),
        reason_code=(
            str(payload["reason_code"])
            if payload.get("reason_code") is not None
            else None
        ),
        status_path=status_path,
        artifacts={
            str(key): str(value)
            for key, value in dict(payload.get("artifacts", {})).items()
        },
    )


def _audit_id(trades_path: Path, policy_path: Path) -> str:
    return f"audit_{hash_file(trades_path)[:8]}{hash_file(policy_path)[:8]}"


def _safe_label(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        normalized = value.strip()
        if len(normalized) <= 128 and all(
            character in _SAFE_LABEL_CHARS for character in normalized
        ):
            return normalized
    return fallback


def _safe_file_ref(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        normalized = value.strip()
        if len(normalized) <= 128 and all(
            character in _SAFE_FILE_REF_CHARS for character in normalized
        ):
            return normalized
    return fallback
