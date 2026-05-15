from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from trader_risk_audit.policy.rule_catalog import rule_availability


@dataclass(frozen=True)
class RuleBuilderQuestionSet:
    profile: str
    account_ids: tuple[str, ...]
    source_timezone: str
    session_start: str
    session_end: str

    def to_intake_session_payload(self) -> dict[str, object]:
        return {
            "source_timezone": self.source_timezone,
            "session": {
                "start": self.session_start,
                "end": self.session_end,
            },
        }


def explain_unavailable_rules(schema_profile: Mapping[str, Any]) -> tuple[str, ...]:
    lines: list[str] = []
    for item in rule_availability(schema_profile):
        if item.available:
            continue
        requirements = ", ".join(item.missing_requirements)
        lines.append(
            f"{item.rule_type}: unavailable because {requirements}; "
            "use available catalog rules or mark this request for manual review."
        )
    return tuple(lines)


def load_schema_profile(path: str | Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    import json

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("schema profile must contain a JSON object")
    return payload


def build_noninteractive_question_set(
    *,
    profile: str,
    account_ids: tuple[str, ...],
    source_timezone: str,
    session_start: str,
    session_end: str,
) -> RuleBuilderQuestionSet:
    return RuleBuilderQuestionSet(
        profile=_required_text(profile, "profile"),
        account_ids=tuple(
            _required_text(account, "account-id") for account in account_ids
        ),
        source_timezone=_required_text(source_timezone, "source-timezone"),
        session_start=_required_text(session_start, "session-start"),
        session_end=_required_text(session_end, "session-end"),
    )


def prompt_question_set() -> RuleBuilderQuestionSet:
    return build_noninteractive_question_set(
        profile=input("Profile: "),
        account_ids=(_required_text(input("Account label: "), "account label"),),
        source_timezone=input("Source timezone: "),
        session_start=input("Session start: "),
        session_end=input("Session end: "),
    )


def _required_text(value: str, field: str) -> str:
    text = value.strip()
    if not text:
        raise ValueError(f"{field} must not be blank")
    return text
