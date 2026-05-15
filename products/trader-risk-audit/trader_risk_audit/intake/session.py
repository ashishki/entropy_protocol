from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

INTAKE_SOURCE_TYPES = frozenset(
    {
        "csv_export",
        "xlsx_candidate",
        "bybit_read_only_api",
        "binance_read_only_api",
    }
)
INTAKE_SESSION_STATUSES = frozenset(
    {
        "created",
        "ready_for_schema_profile",
        "blocked_needs_fix",
        "schema_profiled",
        "ready_for_rules",
        "ready_for_audit",
    }
)
INTAKE_STATUS_TRANSITIONS = {
    "created": frozenset({"ready_for_schema_profile", "blocked_needs_fix"}),
    "ready_for_schema_profile": frozenset({"schema_profiled", "blocked_needs_fix"}),
    "blocked_needs_fix": frozenset({"ready_for_schema_profile"}),
    "schema_profiled": frozenset({"ready_for_rules", "blocked_needs_fix"}),
    "ready_for_rules": frozenset({"ready_for_audit", "blocked_needs_fix"}),
    "ready_for_audit": frozenset({"blocked_needs_fix"}),
}
_SESSION_ID_PATTERN = re.compile(r"^intake_[a-f0-9]{16}$")
_CURRENCY_PATTERN = re.compile(r"^[A-Z0-9]{3,8}$")
_TIME_PATTERN = re.compile(r"^[0-2][0-9]:[0-5][0-9]$")
_SENSITIVE_KEY_PARTS = (
    "api_key",
    "apikey",
    "secret",
    "token",
    "password",
    "credential",
    "private_note",
    "telegram",
    "handle",
    "live_control",
    "order_blocking",
    "broker_control",
    "exchange_write",
    "withdraw",
    "transfer",
)
_SENSITIVE_VALUE_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{8,}"),
    re.compile(r"\blin_api_[A-Za-z0-9_-]+"),
    re.compile(r"\bAKIA[0-9A-Z]{12,}"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"@[A-Za-z0-9_]{4,}"),
)


class IntakeSessionError(ValueError):
    pass


@dataclass(frozen=True)
class IntakePrivacyFlags:
    no_pii_confirmed: bool
    no_credentials_confirmed: bool
    raw_rows_stay_local: bool

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class IntakeSession:
    session_id: str
    prospect_label: str
    source_type: str
    file_references: dict[str, str]
    source_timezone: str
    display_timezone: str
    session: dict[str, str]
    account_currency: str
    privacy_flags: IntakePrivacyFlags
    status: str

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["privacy_flags"] = self.privacy_flags.to_dict()
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def build_intake_session(
    *,
    prospect_label: str,
    source_type: str,
    source_file: str | Path,
    source_timezone: str,
    account_currency: str,
    session_start: str,
    session_end: str,
    display_timezone: str = "Europe/Moscow",
    risk_rules_file: str | Path | None = None,
    status: str = "created",
    privacy_flags: IntakePrivacyFlags | None = None,
) -> IntakeSession:
    normalized_source_type = _safe_choice(
        source_type,
        field="source_type",
        choices=INTAKE_SOURCE_TYPES,
    )
    normalized_status = _safe_choice(
        status,
        field="status",
        choices=INTAKE_SESSION_STATUSES,
    )
    safe_prospect_label = _safe_text(
        prospect_label,
        field="prospect_label",
        allow_at_sign=False,
    )
    safe_file_references = {
        "source_export": _safe_file_reference(source_file),
    }
    if risk_rules_file is not None:
        safe_file_references["risk_rules"] = _safe_file_reference(risk_rules_file)

    safe_source_timezone = _safe_timezone(source_timezone, field="source_timezone")
    safe_display_timezone = _safe_timezone(display_timezone, field="display_timezone")
    safe_session = {
        "start": _safe_time(session_start, field="session_start"),
        "end": _safe_time(session_end, field="session_end"),
    }
    safe_currency = _safe_currency(account_currency)
    flags = privacy_flags or IntakePrivacyFlags(
        no_pii_confirmed=True,
        no_credentials_confirmed=True,
        raw_rows_stay_local=True,
    )
    _validate_privacy_flags(flags)

    session_id = _derive_session_id(
        prospect_label=safe_prospect_label,
        source_type=normalized_source_type,
        file_references=safe_file_references,
        source_timezone=safe_source_timezone,
        display_timezone=safe_display_timezone,
        session=safe_session,
        account_currency=safe_currency,
        privacy_flags=flags,
    )
    return IntakeSession(
        session_id=session_id,
        prospect_label=safe_prospect_label,
        source_type=normalized_source_type,
        file_references=safe_file_references,
        source_timezone=safe_source_timezone,
        display_timezone=safe_display_timezone,
        session=safe_session,
        account_currency=safe_currency,
        privacy_flags=flags,
        status=normalized_status,
    )


def write_intake_session(session: IntakeSession, output_dir: str | Path) -> Path:
    _validate_session(session)
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    output_path = directory / "intake_session.json"
    output_path.write_text(session.to_json(), encoding="utf-8")
    return output_path


def transition_intake_session(
    session: IntakeSession,
    next_status: str,
) -> IntakeSession:
    _validate_session(session)
    normalized_status = _safe_choice(
        next_status,
        field="status",
        choices=INTAKE_SESSION_STATUSES,
    )
    allowed = INTAKE_STATUS_TRANSITIONS[session.status]
    if normalized_status not in allowed:
        raise IntakeSessionError(
            f"cannot transition intake session from {session.status} "
            f"to {normalized_status}"
        )
    return replace(session, status=normalized_status)


def _derive_session_id(
    *,
    prospect_label: str,
    source_type: str,
    file_references: dict[str, str],
    source_timezone: str,
    display_timezone: str,
    session: dict[str, str],
    account_currency: str,
    privacy_flags: IntakePrivacyFlags,
) -> str:
    payload = {
        "account_currency": account_currency,
        "display_timezone": display_timezone,
        "file_references": file_references,
        "privacy_flags": privacy_flags.to_dict(),
        "prospect_label": prospect_label,
        "session": session,
        "source_timezone": source_timezone,
        "source_type": source_type,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return f"intake_{digest[:16]}"


def _validate_session(session: IntakeSession) -> None:
    if _SESSION_ID_PATTERN.fullmatch(session.session_id) is None:
        raise IntakeSessionError("session_id is not a deterministic intake id")
    _safe_text(session.prospect_label, field="prospect_label", allow_at_sign=False)
    _safe_choice(session.source_type, field="source_type", choices=INTAKE_SOURCE_TYPES)
    _safe_choice(session.status, field="status", choices=INTAKE_SESSION_STATUSES)
    for label, value in session.file_references.items():
        _safe_text(label, field="file reference label", allow_at_sign=False)
        _safe_file_reference(value)
    _safe_timezone(session.source_timezone, field="source_timezone")
    _safe_timezone(session.display_timezone, field="display_timezone")
    _safe_time(session.session["start"], field="session_start")
    _safe_time(session.session["end"], field="session_end")
    _safe_currency(session.account_currency)
    _validate_privacy_flags(session.privacy_flags)


def _safe_choice(value: str, *, field: str, choices: frozenset[str]) -> str:
    normalized = _safe_text(value, field=field).casefold()
    if normalized not in choices:
        raise IntakeSessionError(
            f"{field} must be one of: {', '.join(sorted(choices))}"
        )
    return normalized


def _safe_timezone(value: str, *, field: str) -> str:
    text = _safe_text(value, field=field)
    try:
        ZoneInfo(text)
    except ZoneInfoNotFoundError as error:
        raise IntakeSessionError(f"{field} must be an IANA timezone") from error
    return text


def _safe_time(value: str, *, field: str) -> str:
    text = _safe_text(value, field=field)
    if _TIME_PATTERN.fullmatch(text) is None:
        raise IntakeSessionError(f"{field} must use HH:MM format")
    hour = int(text.split(":", 1)[0])
    if hour > 23:
        raise IntakeSessionError(f"{field} must use HH:MM format")
    return text


def _safe_currency(value: str) -> str:
    text = _safe_text(value, field="account_currency").upper()
    if _CURRENCY_PATTERN.fullmatch(text) is None:
        raise IntakeSessionError(
            "account_currency must use 3-8 uppercase letters or digits"
        )
    return text


def _safe_file_reference(value: str | Path) -> str:
    text = _safe_text(str(value), field="file reference")
    path = Path(text)
    if path.is_absolute():
        text = path.name
    if not Path(text).name:
        raise IntakeSessionError("file reference must include a file name")
    return text


def _validate_privacy_flags(flags: IntakePrivacyFlags) -> None:
    if not flags.no_credentials_confirmed:
        raise IntakeSessionError("metadata must confirm no credentials or API keys")
    if not flags.raw_rows_stay_local:
        raise IntakeSessionError("metadata must keep raw rows local")


def _safe_text(value: str, *, field: str, allow_at_sign: bool = True) -> str:
    text = str(value).strip()
    if not text:
        raise IntakeSessionError(f"{field} must not be blank")
    if "\n" in text or "\r" in text:
        raise IntakeSessionError(f"{field} must be a single line")
    _reject_sensitive_text(field, text, allow_at_sign=allow_at_sign)
    return text


def _reject_sensitive_text(field: str, text: str, *, allow_at_sign: bool) -> None:
    normalized_field = field.casefold().replace("-", "_").replace(" ", "_")
    if any(part in normalized_field for part in _SENSITIVE_KEY_PARTS):
        raise IntakeSessionError(f"{field} is not allowed in intake metadata")
    normalized_text = text.casefold().replace("-", "_").replace(" ", "_")
    if any(part in normalized_text for part in _SENSITIVE_KEY_PARTS):
        raise IntakeSessionError(f"{field} contains sensitive metadata")
    for pattern in _SENSITIVE_VALUE_PATTERNS:
        if pattern.search(text) and (allow_at_sign or pattern.pattern[0] != "@"):
            raise IntakeSessionError(f"{field} contains sensitive metadata")
    if not allow_at_sign and "@" in text:
        raise IntakeSessionError(f"{field} must be a prospect-safe label")
