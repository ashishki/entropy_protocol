from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from trader_risk_audit.policy.schema import RiskPolicy

_SENSITIVE_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{8,}"),
    re.compile(r"\bsk-ant-[A-Za-z0-9_-]{8,}"),
    re.compile(r"\blin_api_[A-Za-z0-9_-]+"),
    re.compile(r"\bAKIA[0-9A-Z]{12,}"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"@[A-Za-z0-9_]{4,}"),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
)
_SENSITIVE_WORDS = (
    "api key",
    "apikey",
    "secret",
    "password",
    "credential",
    "private note",
    "telegram handle",
)
_SAFE_TEXT_PATTERN = re.compile(r"[^A-Za-z0-9 .,;:_()/+-]")


class UnsupportedRuleRegisterError(ValueError):
    pass


@dataclass(frozen=True)
class UnsupportedRuleEntry:
    request_id: str
    sanitized_summary: str
    reason_code: str
    status: str = "manual_review_required"


def create_unsupported_rule_entry(
    *,
    user_text: str,
    reason_code: str,
) -> UnsupportedRuleEntry:
    _reject_sensitive_text(user_text)
    safe_reason = _safe_token(reason_code, field="reason_code")
    sanitized = _sanitize_summary(user_text)
    if not sanitized:
        raise UnsupportedRuleRegisterError("unsupported rule summary must not be blank")
    digest = hashlib.sha256(f"{sanitized}|{safe_reason}".encode()).hexdigest()
    return UnsupportedRuleEntry(
        request_id=f"unsupported_{digest[:12]}",
        sanitized_summary=sanitized,
        reason_code=safe_reason,
    )


def append_unsupported_rule_entry(
    path: str | Path,
    entry: UnsupportedRuleEntry,
) -> Path:
    register_path = Path(path)
    register_path.parent.mkdir(parents=True, exist_ok=True)
    existing = (
        register_path.read_text(encoding="utf-8") if register_path.exists() else ""
    )
    prefix = "" if existing else "# Unsupported Rule Register\n\n"
    register_path.write_text(
        existing
        + prefix
        + "\n".join(
            (
                f"## {entry.request_id}",
                f"- Status: {entry.status}",
                f"- Reason: {entry.reason_code}",
                f"- Summary: {entry.sanitized_summary}",
                "",
            )
        ),
        encoding="utf-8",
    )
    return register_path


def render_unsupported_rule_limitations(
    entries: tuple[UnsupportedRuleEntry, ...],
) -> tuple[str, ...]:
    return tuple(
        (
            f"{entry.request_id}: unsupported rule request held for manual review "
            f"({entry.reason_code}) - {entry.sanitized_summary}"
        )
        for entry in entries
    )


def policy_excludes_unsupported_rules(
    policy: RiskPolicy,
    entries: tuple[UnsupportedRuleEntry, ...],
) -> bool:
    unsupported_ids = {entry.request_id for entry in entries}
    return all(rule.rule_id not in unsupported_ids for rule in policy.rules)


def _reject_sensitive_text(value: str) -> None:
    lowered = value.casefold()
    if any(pattern.search(value) for pattern in _SENSITIVE_PATTERNS) or any(
        word in lowered for word in _SENSITIVE_WORDS
    ):
        raise UnsupportedRuleRegisterError(
            "unsupported rule text must not contain credentials, handles, "
            "or private notes"
        )


def _sanitize_summary(value: str) -> str:
    collapsed = " ".join(value.strip().split())
    cleaned = _SAFE_TEXT_PATTERN.sub("", collapsed)
    return cleaned[:160].strip()


def _safe_token(value: str, *, field: str) -> str:
    token = value.strip().casefold().replace("-", "_").replace(" ", "_")
    if not token or not re.fullmatch(r"[a-z0-9_]+", token):
        raise UnsupportedRuleRegisterError(f"{field} must be a safe token")
    return token
