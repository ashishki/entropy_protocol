from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_REQUIRED_FIELDS = ("timestamp", "symbol", "side", "quantity", "price")
_SENSITIVE_TEXT_PARTS = (
    "api_key",
    "apikey",
    "secret",
    "token",
    "password",
    "credential",
    "telegram",
    "handle",
)
_SECRET_PATTERN = re.compile(
    r"(sk-[A-Za-z0-9_-]{8,}|lin_api_[A-Za-z0-9_-]+|AKIA[0-9A-Z]{12,}|"
    r"Bearer\s+[A-Za-z0-9._-]+|@[A-Za-z0-9_]{4,})",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class IntakeReport:
    status: str
    reasons: tuple[str, ...]
    accepted_fields: tuple[str, ...]
    unsupported_checks: tuple[str, ...]
    next_action: str
    markdown: str


def build_intake_report(
    *,
    session_payload: dict[str, Any],
    profile_payload: dict[str, Any],
) -> IntakeReport:
    status, reasons = _classify_intake(session_payload, profile_payload)
    accepted_fields = tuple(
        field
        for field in _REQUIRED_FIELDS
        if field in _canonical_field_map(profile_payload)
    )
    unsupported_checks = _unsupported_checks(profile_payload)
    next_action = _next_action(status)
    markdown = _render_markdown(
        session_payload=session_payload,
        profile_payload=profile_payload,
        status=status,
        reasons=reasons,
        accepted_fields=accepted_fields,
        unsupported_checks=unsupported_checks,
        next_action=next_action,
    )
    return IntakeReport(
        status=status,
        reasons=reasons,
        accepted_fields=accepted_fields,
        unsupported_checks=unsupported_checks,
        next_action=next_action,
        markdown=markdown,
    )


def write_intake_report(report: IntakeReport, output_dir: str | Path) -> Path:
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / "intake_report.md"
    output_path.write_text(report.markdown, encoding="utf-8")
    return output_path


def _classify_intake(
    session_payload: dict[str, Any],
    profile_payload: dict[str, Any],
) -> tuple[str, tuple[str, ...]]:
    session_status = str(session_payload.get("status", "")).strip()
    source_type = str(session_payload.get("source_type", "")).strip()
    missing = tuple(
        str(item) for item in profile_payload.get("missing_required_fields", ())
    )
    duplicate_risk = bool(profile_payload.get("duplicate_row_id_risk", False))
    timezone_coverage = str(profile_payload.get("timestamp_timezone", "not_mapped"))

    if session_status in {"blocked_needs_fix", "rejected"}:
        return "rejected", ("intake session is blocked before profiling",)
    if source_type != "csv_export":
        return (
            "needs-operator-review",
            (f"source type {source_type or 'unknown'} is not an automated CSV path",),
        )
    if missing:
        return (
            "needs-user-fix",
            ("missing required fields: " + ", ".join(missing),),
        )
    review_reasons: list[str] = []
    if duplicate_risk:
        review_reasons.append("duplicate or blank row id values need review")
    if timezone_coverage in {"timezone_missing", "mixed", "not_mapped"}:
        review_reasons.append(f"timestamp timezone coverage is {timezone_coverage}")
    if review_reasons:
        return "needs-operator-review", tuple(review_reasons)
    return "runnable", ("required fields are mapped and timestamps include timezone",)


def _unsupported_checks(profile_payload: dict[str, Any]) -> tuple[str, ...]:
    checks: list[str] = []
    if not bool(profile_payload.get("fee_available", False)):
        checks.append("fees")
    if not bool(profile_payload.get("pnl_available", False)):
        checks.append("P&L")
        checks.append("drawdown")
    if not bool(profile_payload.get("leverage_available", False)):
        checks.append("leverage")
    if not bool(profile_payload.get("account_balance_available", False)):
        checks.append("account balance")
    return tuple(checks)


def _next_action(status: str) -> str:
    return {
        "runnable": "Proceed to structured rule builder or operator review.",
        "needs-user-fix": "Ask the prospect for a corrected CSV export.",
        "needs-operator-review": "Operator should review assumptions before audit.",
        "rejected": "Stop intake until the blocked session is replaced.",
    }[status]


def _render_markdown(
    *,
    session_payload: dict[str, Any],
    profile_payload: dict[str, Any],
    status: str,
    reasons: tuple[str, ...],
    accepted_fields: tuple[str, ...],
    unsupported_checks: tuple[str, ...],
    next_action: str,
) -> str:
    canonical_map = _canonical_field_map(profile_payload)
    unsupported_columns = tuple(
        str(column) for column in profile_payload.get("unsupported_columns", ())
    )
    session_id = _safe_markdown_value(session_payload.get("session_id", "unknown"))
    prospect_label = _safe_markdown_value(
        session_payload.get("prospect_label", "unknown")
    )
    source_file = _safe_markdown_value(profile_payload.get("source_file", "unknown"))
    lines = [
        "# Intake Report",
        "",
        f"Session: {session_id}",
        f"Prospect label: {prospect_label}",
        f"Source file: {source_file}",
        f"Status: {status}",
        "",
        "## Reasons",
        *_bullet_lines(reasons),
        "",
        "## Accepted Fields",
        *_field_lines(accepted_fields, canonical_map),
        "",
        "## Blockers",
        *_blocker_lines(status, reasons),
        "",
        "## Unsupported Checks",
        *_bullet_lines(unsupported_checks or ("none",)),
        "",
        "## Unsupported Columns",
        *_bullet_lines(unsupported_columns or ("none",)),
        "",
        "## Next Action",
        next_action,
        "",
        "Privacy: this report contains schema metadata only, not raw trade rows.",
        "",
    ]
    return "\n".join(lines)


def _canonical_field_map(profile_payload: dict[str, Any]) -> dict[str, str]:
    raw_map = profile_payload.get("canonical_field_map", {})
    if not isinstance(raw_map, dict):
        return {}
    return {str(key): str(value) for key, value in raw_map.items()}


def _field_lines(
    accepted_fields: tuple[str, ...],
    canonical_map: dict[str, str],
) -> list[str]:
    if not accepted_fields:
        return ["- none"]
    return [
        f"- {_safe_markdown_value(field)}: {_safe_markdown_value(canonical_map[field])}"
        for field in accepted_fields
    ]


def _blocker_lines(status: str, reasons: tuple[str, ...]) -> list[str]:
    if status in {"runnable", "needs-operator-review"}:
        return ["- none"]
    return _bullet_lines(reasons)


def _bullet_lines(values: tuple[str, ...]) -> list[str]:
    return [f"- {_safe_markdown_value(value)}" for value in values]


def _safe_markdown_value(value: object) -> str:
    text = str(value).strip().replace("\r", " ").replace("\n", " ")
    normalized = text.casefold().replace("-", "_").replace(" ", "_")
    if _SECRET_PATTERN.search(text) or any(
        part in normalized for part in _SENSITIVE_TEXT_PARTS
    ):
        return "redacted"
    return text or "unknown"
