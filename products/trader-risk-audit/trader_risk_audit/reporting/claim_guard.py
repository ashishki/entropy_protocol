from __future__ import annotations

from dataclasses import dataclass

REQUIRED_DISCLAIMER = (
    "This audit is not investment advice and does not control live trading."
)


@dataclass(frozen=True)
class ForbiddenPhrase:
    category: str
    phrase: str


@dataclass(frozen=True)
class ClaimGuardFinding:
    category: str
    matched_text: str
    message: str


@dataclass(frozen=True)
class ClaimGuardResult:
    passed: bool
    findings: tuple[ClaimGuardFinding, ...]


DEFAULT_FORBIDDEN_PHRASES = (
    ForbiddenPhrase("profit_promise", "guaranteed profit"),
    ForbiddenPhrase("profit_promise", "guaranteed profits"),
    ForbiddenPhrase("profit_promise", "guarantees profit"),
    ForbiddenPhrase("profit_promise", "will be profitable"),
    ForbiddenPhrase("profit_promise", "will make money"),
    ForbiddenPhrase("live_order_control", "controls live orders"),
    ForbiddenPhrase("live_order_control", "will block orders"),
    ForbiddenPhrase("live_order_control", "automatically blocks trades"),
    ForbiddenPhrase("live_order_control", "prevents live trades"),
    ForbiddenPhrase("causal_loss_assertion", "caused your losses"),
    ForbiddenPhrase("causal_loss_assertion", "caused losses"),
    ForbiddenPhrase("counterfactual_returns", "would have made"),
    ForbiddenPhrase("counterfactual_returns", "would have prevented losses"),
)


def validate_report_claims(
    report_text: str,
    *,
    required_disclaimer: str = REQUIRED_DISCLAIMER,
    forbidden_phrases: tuple[ForbiddenPhrase, ...] = DEFAULT_FORBIDDEN_PHRASES,
) -> ClaimGuardResult:
    findings: list[ClaimGuardFinding] = []
    if _find_case_insensitive(report_text, required_disclaimer) is None:
        findings.append(
            ClaimGuardFinding(
                category="required_disclaimer",
                matched_text=required_disclaimer,
                message="missing required report disclaimer",
            )
        )

    for forbidden in forbidden_phrases:
        matched_text = _find_case_insensitive(report_text, forbidden.phrase)
        if matched_text is None:
            continue
        findings.append(
            ClaimGuardFinding(
                category=forbidden.category,
                matched_text=matched_text,
                message="forbidden report claim phrase",
            )
        )

    return ClaimGuardResult(passed=not findings, findings=tuple(findings))


def ensure_report_claims_valid(report_text: str) -> None:
    result = validate_report_claims(report_text)
    if not result.passed:
        finding_summary = ", ".join(
            f"{finding.category}: {finding.matched_text}" for finding in result.findings
        )
        raise ClaimGuardError(f"Report claim guard failed: {finding_summary}")


class ClaimGuardError(ValueError):
    pass


def _find_case_insensitive(text: str, phrase: str) -> str | None:
    start = text.casefold().find(phrase.casefold())
    if start == -1:
        return None
    return text[start : start + len(phrase)]
