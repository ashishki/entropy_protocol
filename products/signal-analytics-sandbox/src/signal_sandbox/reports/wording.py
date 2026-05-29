"""Customer-safe wording rules for report surfaces."""

from __future__ import annotations

import re
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class WordingCategory(StrEnum):
    ADVICE = "advice"
    FUTURE_PROFIT = "future_profit"
    LEADERBOARD = "leaderboard"
    MARKETPLACE = "marketplace"
    OVERCLAIM = "overclaim"


class WordingRule(BaseModel):
    model_config = ConfigDict(strict=True, arbitrary_types_allowed=True)

    category: WordingCategory
    pattern: re.Pattern[str]
    explanation: str = Field(min_length=1)


class WordingFinding(BaseModel):
    model_config = ConfigDict(strict=True)

    category: WordingCategory
    phrase: str = Field(min_length=1)
    explanation: str = Field(min_length=1)


ALLOWED_CONTEXT_PHRASES: tuple[str, ...] = (
    "historical research only",
    "not financial advice",
    "internal-only",
    "internal only",
    "not approved for external/customer-facing delivery",
    "unsupported rows are exclusions",
)


FORBIDDEN_WORDING_RULES: tuple[WordingRule, ...] = (
    WordingRule(
        category=WordingCategory.ADVICE,
        pattern=re.compile(
            r"\b(should|must)\s+(buy|sell|short|long|trade|hold)\b|"
            r"\b(buy|sell|short|long)\s+now\b|"
            r"\brecommend(?:ed|s|ation)?\s+to\s+(buy|sell|short|long)\b",
            re.IGNORECASE,
        ),
        explanation="Do not provide trading or investment instructions.",
    ),
    WordingRule(
        category=WordingCategory.FUTURE_PROFIT,
        pattern=re.compile(
            r"\b(guaranteed|sure|risk-free)\s+(profit|return|gain)\b|"
            r"\bwill\s+(profit|make money|outperform|win)\b|"
            r"\bpromise\s+of\s+future\s+(profit|return|performance)\b",
            re.IGNORECASE,
        ),
        explanation="Do not promise future profit or performance.",
    ),
    WordingRule(
        category=WordingCategory.LEADERBOARD,
        pattern=re.compile(
            r"\b(best|top|number one|#1)\s+(channel|author|trader|signal)\b|"
            r"\bleaderboard\s+(rank|ranking|score)\b",
            re.IGNORECASE,
        ),
        explanation="Do not create unsupported channel ranking language.",
    ),
    WordingRule(
        category=WordingCategory.MARKETPLACE,
        pattern=re.compile(
            r"\b(marketplace|buy access|subscribe now|paid signal)\b",
            re.IGNORECASE,
        ),
        explanation="Do not imply a paid signal marketplace or sales claim.",
    ),
    WordingRule(
        category=WordingCategory.OVERCLAIM,
        pattern=re.compile(
            r"\b(proven edge|verified profitable|predicts the market)\b|"
            r"\bstatistically significant\b(?!.*\b(sample|method|test)\b)",
            re.IGNORECASE,
        ),
        explanation="Do not overstate evidence strength or statistical support.",
    ),
)


def find_forbidden_wording(text: str) -> list[WordingFinding]:
    findings: list[WordingFinding] = []
    for rule in FORBIDDEN_WORDING_RULES:
        match = rule.pattern.search(text)
        if match is None:
            continue
        findings.append(
            WordingFinding(
                category=rule.category,
                phrase=match.group(0),
                explanation=rule.explanation,
            )
        )
    return findings


def is_customer_safe_wording(text: str) -> bool:
    return not find_forbidden_wording(text)
