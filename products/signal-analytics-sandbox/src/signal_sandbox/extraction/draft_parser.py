"""Deterministic draft parser for captured public posts."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from signal_sandbox.capture.loader import CapturedPost

DraftStatus = Literal[
    "not_a_signal",
    "insufficient_fields",
    "needs_review",
    "review_candidate",
]


@dataclass(frozen=True)
class ReviewDraft:
    capture_id: str
    evidence_url: str
    text_sha256: str
    suggested_status: DraftStatus
    candidate_fields: dict[str, object]
    missing_required_fields: list[str]
    reason_codes: list[str]
    confidence: float
    review_required: bool


def parse_draft(post: CapturedPost, profile: Mapping[str, Any]) -> ReviewDraft:
    """Parse a captured post into a review-only draft suggestion."""

    accepted_terms = _accepted_terms(profile)
    text = post.raw_text
    text_folded = text.casefold()

    assets = [
        term["term"].lstrip("#").upper()
        for term in accepted_terms
        if term["category"] == "asset_alias"
        and term["term"].casefold() in text_folded
    ]
    direction, direction_reason = _detect_direction(text_folded, accepted_terms)
    entry = _find_labeled_number(text, ("entry", "вход", "взял по", "купил по"))
    stop = _find_labeled_number(text, ("stop", "стоп"))
    target = _find_labeled_number(text, ("target", "цель", "таргет", "тейк"))
    uncertainty = _has_category(text_folded, accepted_terms, "uncertainty")
    close_or_reduce = direction == "close_or_reduce"

    candidate_fields: dict[str, object] = {
        "asset_candidates": assets,
        "direction_candidate": direction,
        "entry_candidate": entry,
        "stop_candidate": stop,
        "target_candidate": target,
    }
    missing = _missing_required_fields(assets, direction, entry, stop, target)
    status = _suggest_status(assets, direction, missing, uncertainty, close_or_reduce)
    reason_codes = _reason_codes(
        assets=assets,
        direction=direction,
        direction_reason=direction_reason,
        missing=missing,
        uncertainty=uncertainty,
        close_or_reduce=close_or_reduce,
    )

    return ReviewDraft(
        capture_id=post.capture_id,
        evidence_url=post.evidence_url,
        text_sha256=post.text_sha256,
        suggested_status=status,
        candidate_fields=candidate_fields,
        missing_required_fields=missing,
        reason_codes=reason_codes,
        confidence=_confidence(status, missing, uncertainty),
        review_required=status != "not_a_signal",
    )


def _accepted_terms(profile: Mapping[str, Any]) -> list[dict[str, str]]:
    candidates = profile.get("candidates", [])
    if not isinstance(candidates, Sequence) or isinstance(candidates, str):
        return []

    terms: list[dict[str, str]] = []
    for candidate in candidates:
        if not isinstance(candidate, Mapping):
            continue
        if candidate.get("profile_state") != "accepted_for_draft":
            continue
        term = candidate.get("term")
        category = candidate.get("category")
        if isinstance(term, str) and isinstance(category, str):
            terms.append({"term": term, "category": category})
    return terms


def _detect_direction(
    text_folded: str, accepted_terms: Sequence[Mapping[str, str]]
) -> tuple[str, str | None]:
    if _has_category(text_folded, accepted_terms, "close_or_reduce"):
        return "close_or_reduce", "close_or_reduce_term"
    if _has_category(text_folded, accepted_terms, "direction_short"):
        return "short", "direction_short_term"
    if _has_category(text_folded, accepted_terms, "direction_long"):
        return "long", "direction_long_term"
    return "unknown", None


def _has_category(
    text_folded: str, accepted_terms: Sequence[Mapping[str, str]], category: str
) -> bool:
    return any(
        term["category"] == category and term["term"].casefold() in text_folded
        for term in accepted_terms
    )


def _find_labeled_number(text: str, labels: Sequence[str]) -> str | None:
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = rf"(?:{label_pattern})\D{{0,20}}(\d+(?:[.,]\d+)?)"
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if match is None:
        return None
    return match.group(1).replace(",", ".")


def _missing_required_fields(
    assets: Sequence[str],
    direction: str,
    entry: str | None,
    stop: str | None,
    target: str | None,
) -> list[str]:
    missing: list[str] = []
    if not assets:
        missing.append("asset_symbol")
    if direction in {"unknown", "close_or_reduce"}:
        missing.append("direction")
    if entry is None:
        missing.append("entry")
    if stop is None:
        missing.append("stop")
    if target is None:
        missing.append("target")
    return missing


def _suggest_status(
    assets: Sequence[str],
    direction: str,
    missing: Sequence[str],
    uncertainty: bool,
    close_or_reduce: bool,
) -> DraftStatus:
    if uncertainty:
        return "needs_review"
    if not missing and direction in {"long", "short"}:
        return "review_candidate"
    if assets or direction != "unknown" or close_or_reduce:
        return "insufficient_fields"
    return "not_a_signal"


def _reason_codes(
    *,
    assets: Sequence[str],
    direction: str,
    direction_reason: str | None,
    missing: Sequence[str],
    uncertainty: bool,
    close_or_reduce: bool,
) -> list[str]:
    reasons: list[str] = []
    if assets:
        reasons.append("asset_alias_detected")
    if direction_reason is not None:
        reasons.append(direction_reason)
    if uncertainty:
        reasons.append("uncertainty_marker_detected")
    if close_or_reduce:
        reasons.append("close_or_reduce_requires_original_setup")
    reasons.extend(f"missing_{field}" for field in missing)
    if not reasons:
        reasons.append("no_trade_terms_detected")
    return reasons


def _confidence(
    status: DraftStatus, missing: Sequence[str], uncertainty: bool
) -> float:
    if status == "not_a_signal":
        return 0.72
    if status == "review_candidate":
        return 0.68
    if uncertainty:
        return 0.42
    return max(0.35, 0.64 - (0.05 * len(missing)))
