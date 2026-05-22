"""Deterministic report language safety checks."""

from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class ReportSafetyCategory(StrEnum):
    ADVICE = "advice"
    FUTURE_PROFIT = "future_profit"
    UNSUPPORTED_RANKING = "unsupported_ranking"
    MARKETPLACE = "marketplace"
    UNREVIEWED_MEDIA = "unreviewed_media"
    MISSING_REQUIRED_CONTEXT = "missing_required_context"


class ReportSafetyFinding(BaseModel):
    model_config = ConfigDict(strict=True)

    category: ReportSafetyCategory
    phrase: str = Field(min_length=1)
    line_number: int = Field(ge=1)
    line_text: str = Field(min_length=1)


class ReportSafetyResult(BaseModel):
    model_config = ConfigDict(strict=True)

    passed: bool
    findings: list[ReportSafetyFinding] = Field(default_factory=list)
    required_context_present: dict[str, bool]


_FORBIDDEN_PATTERNS: tuple[tuple[ReportSafetyCategory, re.Pattern[str]], ...] = (
    (
        ReportSafetyCategory.ADVICE,
        re.compile(
            r"\b(should|must)\s+(buy|sell|short|long|trade|hold)\b|"
            r"\b(buy|sell|short|long)\s+now\b|"
            r"\brecommend(?:ed|s|ation)?\s+to\s+(buy|sell|short|long)\b",
            re.IGNORECASE,
        ),
    ),
    (
        ReportSafetyCategory.FUTURE_PROFIT,
        re.compile(
            r"\b(guaranteed|sure|risk-free)\s+(profit|return|gain)\b|"
            r"\bwill\s+(profit|make money|outperform|win)\b|"
            r"\bpromise\s+of\s+future\s+(profit|return|performance)\b",
            re.IGNORECASE,
        ),
    ),
    (
        ReportSafetyCategory.UNSUPPORTED_RANKING,
        re.compile(
            r"\b(best|top|number one|#1)\s+(channel|author|trader|signal)\b|"
            r"\bleaderboard\s+(rank|ranking|score)\b",
            re.IGNORECASE,
        ),
    ),
    (
        ReportSafetyCategory.MARKETPLACE,
        re.compile(
            r"\b(marketplace|buy access|subscribe now|paid signal)\b",
            re.IGNORECASE,
        ),
    ),
    (
        ReportSafetyCategory.UNREVIEWED_MEDIA,
        re.compile(
            r"\b(media|ocr|chart|transcript)[-\s]+backed\s+claim\b",
            re.IGNORECASE,
        ),
    ),
)

_NEGATING_CONTEXT = (
    "not ",
    "no ",
    "must not",
    "do not",
    "does not",
    "disallowed",
    "excluded",
    "remains excluded",
    "without",
)


def check_report_language_safety(report_text: str) -> ReportSafetyResult:
    findings: list[ReportSafetyFinding] = []
    for line_number, line in enumerate(report_text.splitlines(), start=1):
        normalized_line = line.strip()
        if not normalized_line:
            continue
        for category, pattern in _FORBIDDEN_PATTERNS:
            match = pattern.search(normalized_line)
            if match is None or _is_negated_safety_context(normalized_line):
                continue
            findings.append(
                ReportSafetyFinding(
                    category=category,
                    phrase=match.group(0),
                    line_number=line_number,
                    line_text=normalized_line,
                )
            )

    required_context_present = {
        "limitations": "## Limitations" in report_text,
        "evidence_links": "https://t.me/" in report_text,
        "gate_status": "Decision: approve_internal_only" in report_text,
        "external_blocked": "not approved for external/customer-facing delivery"
        in report_text,
        "media_exclusion": "Audio, OCR, and chart claims remain excluded"
        in report_text,
    }
    for key, present in required_context_present.items():
        if present:
            continue
        findings.append(
            ReportSafetyFinding(
                category=ReportSafetyCategory.MISSING_REQUIRED_CONTEXT,
                phrase=key,
                line_number=1,
                line_text=f"missing required context: {key}",
            )
        )

    return ReportSafetyResult(
        passed=not findings,
        findings=findings,
        required_context_present=required_context_present,
    )


def _is_negated_safety_context(line: str) -> bool:
    folded = line.casefold()
    return any(marker in folded for marker in _NEGATING_CONTEXT)
