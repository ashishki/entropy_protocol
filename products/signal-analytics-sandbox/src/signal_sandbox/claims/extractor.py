"""Deterministic structured claim extraction for V1 metrics."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.corpus import SourceDocument

METADATA_VERSION = "structured_claim.v1"

ASSET_ALIASES: dict[str, tuple[str, ...]] = {
    "BTC": ("#BTC", "$BTC", "BTC", "BTCUSD", "BTCUSDT", "bitcoin", "биткоин", "битк"),
    "ETH": ("#ETH", "$ETH", "ETH", "ETHUSD", "ETHUSDT", "ethereum", "эфир"),
    "TON": ("#TON", "$TON", "TON", "TONUSDT"),
    "SBER": ("#SBER", "$SBER", "SBRF", "#SBRF"),
}

BLOCKED_ASSET_TOKENS = {"SIGN-UP"}


class StructuredClaimType(StrEnum):
    TRADE_SETUP = "trade_setup"
    DIRECTIONAL_THESIS = "directional_thesis"
    POSITION_DISCLOSURE = "position_disclosure"
    TRADE_MANAGEMENT = "trade_management"
    RISK_WARNING = "risk_warning"
    CONTEXT_ONLY = "context_only"


class ClaimDirection(StrEnum):
    LONG = "long"
    SHORT = "short"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class ClaimEvidenceSpan(BaseModel):
    model_config = ConfigDict(strict=True)

    span_id: str = Field(min_length=1)
    source_document_id: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(gt=0)
    excerpt: str = Field(min_length=1)
    supports: str = Field(
        pattern=(
            "^(asset|direction|entry|stop|target|risk_reward|claim_type|"
            "horizon|blocker)$"
        )
    )


class StructuredClaim(BaseModel):
    model_config = ConfigDict(strict=True)

    claim_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_document_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)
    source_timestamp_utc: datetime
    claim_type: StructuredClaimType
    assets: list[str] = Field(default_factory=list)
    direction: ClaimDirection = ClaimDirection.UNKNOWN
    entry: Decimal | None = None
    stop: Decimal | None = None
    target: Decimal | None = None
    risk_reward: Decimal | None = None
    horizon_hint: list[str] = Field(default_factory=list)
    evidence_spans: list[ClaimEvidenceSpan] = Field(default_factory=list)
    ambiguity_flags: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    metadata_version: str = METADATA_VERSION

    @field_validator("source_timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("source_timestamp_utc must be datetime or ISO string")


class StructuredClaimExtractor:
    """Rule-only extractor; never calls LLMs, market APIs, or the network."""

    def extract(self, document: SourceDocument) -> list[StructuredClaim]:
        assets, asset_spans, blocked_tokens = _extract_assets(document)
        direction, direction_span = _extract_direction(document)
        claim_type, type_span = _claim_type(document.text, assets, direction)
        entry, entry_span = _extract_level(document, ("entry", "вход", "выше"))
        stop, stop_span = _extract_level(document, ("stop", "стоп"))
        target, target_span = _extract_level(document, ("target", "цель", "тейк"))
        risk_reward, rr_span = _extract_risk_reward(document)
        horizon_hint, horizon_spans = _extract_horizons(document)

        spans = [
            *asset_spans,
            *([direction_span] if direction_span is not None else []),
            *([type_span] if type_span is not None else []),
            *([entry_span] if entry_span is not None else []),
            *([stop_span] if stop_span is not None else []),
            *([target_span] if target_span is not None else []),
            *([rr_span] if rr_span is not None else []),
            *horizon_spans,
        ]

        return [
            StructuredClaim(
                claim_id=_claim_id(document, claim_type, assets, direction),
                source_id=document.source_id,
                capture_id=document.capture_id,
                source_document_id=document.document_id,
                evidence_url=document.evidence_url,
                text_sha256=document.text_sha256,
                source_timestamp_utc=document.timestamp_utc,
                claim_type=claim_type,
                assets=assets,
                direction=direction,
                entry=entry,
                stop=stop,
                target=target,
                risk_reward=risk_reward,
                horizon_hint=horizon_hint,
                evidence_spans=_renumber_spans(spans) or [_fallback_span(document)],
                ambiguity_flags=_ambiguity_flags(
                    assets=assets,
                    direction=direction,
                    blocked_tokens=blocked_tokens,
                ),
                blockers=_blockers(
                    claim_type=claim_type,
                    assets=assets,
                    direction=direction,
                    entry=entry,
                    stop=stop,
                    target=target,
                    blocked_tokens=blocked_tokens,
                ),
            )
        ]


def extract_structured_claims(document: SourceDocument) -> list[StructuredClaim]:
    return StructuredClaimExtractor().extract(document)


def _extract_assets(
    document: SourceDocument,
) -> tuple[list[str], list[ClaimEvidenceSpan], list[str]]:
    found: dict[str, ClaimEvidenceSpan] = {}
    blocked: list[str] = []
    for token in re.findall(r"[$#]?[A-Za-z][A-Za-z0-9-]{1,14}", document.text):
        symbol = token.lstrip("#$").upper()
        if symbol in BLOCKED_ASSET_TOKENS:
            blocked.append(symbol)
            continue
        if token.startswith(("#", "$")) and 2 <= len(symbol) <= 10:
            found.setdefault(symbol, _span(document, token, "asset"))

    folded = document.text.casefold()
    for asset, aliases in ASSET_ALIASES.items():
        for alias in aliases:
            if _alias_in_text(document.text, folded, alias):
                found.setdefault(asset, _span(document, alias, "asset"))
                break

    for noise in BLOCKED_ASSET_TOKENS:
        if noise.casefold() in folded:
            blocked.append(noise)

    return sorted(found), list(found.values()), sorted(set(blocked))


def _extract_direction(
    document: SourceDocument,
) -> tuple[ClaimDirection, ClaimEvidenceSpan | None]:
    folded = document.text.casefold()
    negated_long = _contains_any(
        folded,
        ("никаких покупок", "not bullish", "не быч", "не лонг", "not a long"),
    )
    negated_short = _contains_any(folded, ("не шорт", "not a short"))
    long_terms = (
        "long",
        "buy",
        "bullish",
        "bullrun",
        "upside",
        "лонг",
        "покуп",
        "рост",
        "буллран",
    )
    short_terms = ("short", "sell", "bearish", "downside", "шорт", "паден")
    has_long = _contains_any(folded, long_terms) and not negated_long
    has_short = _contains_any(folded, short_terms) and not negated_short
    if has_long and has_short:
        return ClaimDirection.MIXED, _first_term_span(
            document,
            (*long_terms, *short_terms),
            "direction",
        )
    if has_long:
        return ClaimDirection.LONG, _first_term_span(document, long_terms, "direction")
    if has_short:
        return ClaimDirection.SHORT, _first_term_span(
            document,
            short_terms,
            "direction",
        )
    return ClaimDirection.UNKNOWN, None


def _claim_type(
    text: str,
    assets: list[str],
    direction: ClaimDirection,
) -> tuple[StructuredClaimType, ClaimEvidenceSpan | None]:
    folded = text.casefold()
    if _contains_any(
        folded,
        ("закрыл", "закрою", "closed", "close", "прикрыл", "moved stop"),
    ):
        return StructuredClaimType.TRADE_MANAGEMENT, None
    if _contains_any(folded, ("позиция", "position", "держу", "holding", "набрал")):
        return StructuredClaimType.POSITION_DISCLOSURE, None
    if _contains_any(
        folded,
        (
            "entry",
            "вход",
            "stop",
            "стоп",
            "target",
            "цель",
            "выше",
            "ниже",
            "trap line",
            "safety trade",
        ),
    ):
        return StructuredClaimType.TRADE_SETUP, None
    if _contains_any(folded, ("risk warning", "no trade", "риск", "опасн")):
        return StructuredClaimType.RISK_WARNING, None
    if assets and direction in {ClaimDirection.LONG, ClaimDirection.SHORT}:
        return StructuredClaimType.DIRECTIONAL_THESIS, None
    return StructuredClaimType.CONTEXT_ONLY, None


def _extract_level(
    document: SourceDocument,
    labels: tuple[str, ...],
) -> tuple[Decimal | None, ClaimEvidenceSpan | None]:
    label_pattern = "|".join(re.escape(label) for label in labels)
    pattern = rf"(?:{label_pattern})\s*[:=]?\s*(\d+(?:[.,]\d+)?)"
    match = re.search(pattern, document.text, flags=re.IGNORECASE)
    if match is None:
        return None, None
    value = Decimal(match.group(1).replace(",", "."))
    support = "entry"
    if any(label in {"stop", "стоп"} for label in labels):
        support = "stop"
    if any(label in {"target", "цель", "тейк"} for label in labels):
        support = "target"
    return value, _match_span(document, match, support)


def _extract_risk_reward(
    document: SourceDocument,
) -> tuple[Decimal | None, ClaimEvidenceSpan | None]:
    match = re.search(r"\b(?:rr|r/r)\s*[:=]?\s*(\d+(?:[.,]\d+)?)", document.text, re.I)
    if match is None:
        return None, None
    return Decimal(match.group(1).replace(",", ".")), _match_span(
        document,
        match,
        "risk_reward",
    )


def _extract_horizons(
    document: SourceDocument,
) -> tuple[list[str], list[ClaimEvidenceSpan]]:
    horizons: list[str] = []
    spans: list[ClaimEvidenceSpan] = []
    for label in ("1d", "3d", "7d", "30d"):
        span = _first_term_span(document, (label,), "horizon")
        if span is not None:
            horizons.append(label)
            spans.append(span)
    folded = document.text.casefold()
    if "week" in folded or "недел" in folded:
        horizons.append("7d")
    if "month" in folded or "месяц" in folded:
        horizons.append("30d")
    return sorted(set(horizons)), spans


def _blockers(
    *,
    claim_type: StructuredClaimType,
    assets: list[str],
    direction: ClaimDirection,
    entry: Decimal | None,
    stop: Decimal | None,
    target: Decimal | None,
    blocked_tokens: list[str],
) -> list[str]:
    blockers: list[str] = []
    if not assets and claim_type not in {
        StructuredClaimType.CONTEXT_ONLY,
        StructuredClaimType.RISK_WARNING,
    }:
        blockers.append("missing_asset")
    if direction == ClaimDirection.UNKNOWN and claim_type not in {
        StructuredClaimType.CONTEXT_ONLY,
        StructuredClaimType.RISK_WARNING,
        StructuredClaimType.TRADE_MANAGEMENT,
    }:
        blockers.append("missing_direction")
    if claim_type == StructuredClaimType.TRADE_SETUP:
        if entry is None:
            blockers.append("missing_entry")
        if stop is None:
            blockers.append("missing_stop")
        if target is None:
            blockers.append("missing_target")
    if claim_type == StructuredClaimType.TRADE_MANAGEMENT:
        blockers.append("requires_original_setup_link")
    for token in blocked_tokens:
        blockers.append(f"blocked_asset_token:{token}")
    return blockers


def _ambiguity_flags(
    *,
    assets: list[str],
    direction: ClaimDirection,
    blocked_tokens: list[str],
) -> list[str]:
    flags: list[str] = []
    if len(assets) > 1:
        flags.append("multiple_assets")
    if direction == ClaimDirection.MIXED:
        flags.append("mixed_direction")
    if blocked_tokens:
        flags.append("blocked_asset_token")
    return flags


def _span(document: SourceDocument, term: str, support: str) -> ClaimEvidenceSpan:
    match = re.search(re.escape(term), document.text, flags=re.IGNORECASE)
    if match is None:
        return _fallback_span(document)
    return _match_span(document, match, support)


def _first_term_span(
    document: SourceDocument,
    terms: tuple[str, ...],
    support: str,
) -> ClaimEvidenceSpan | None:
    for term in terms:
        match = re.search(re.escape(term), document.text, flags=re.IGNORECASE)
        if match is not None:
            return _match_span(document, match, support)
    return None


def _match_span(
    document: SourceDocument,
    match: re.Match[str],
    support: str,
) -> ClaimEvidenceSpan:
    return ClaimEvidenceSpan(
        span_id="span-0",
        source_document_id=document.document_id,
        start_char=match.start(),
        end_char=match.end(),
        excerpt=document.text[match.start() : match.end()],
        supports=support,
    )


def _fallback_span(document: SourceDocument) -> ClaimEvidenceSpan:
    excerpt = document.text[:80] or "empty source text"
    return ClaimEvidenceSpan(
        span_id="span-1",
        source_document_id=document.document_id,
        start_char=0,
        end_char=max(len(excerpt), 1),
        excerpt=excerpt,
        supports="claim_type",
    )


def _renumber_spans(spans: list[ClaimEvidenceSpan]) -> list[ClaimEvidenceSpan]:
    return [
        span.model_copy(update={"span_id": f"span-{index}"})
        for index, span in enumerate(spans, start=1)
    ]


def _claim_id(
    document: SourceDocument,
    claim_type: StructuredClaimType,
    assets: list[str],
    direction: ClaimDirection,
) -> str:
    payload = "|".join(
        [
            document.source_id,
            document.capture_id,
            document.document_id,
            document.text_sha256,
            claim_type.value,
            ",".join(assets),
            direction.value,
            METADATA_VERSION,
        ]
    )
    return f"claim-{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def _alias_in_text(text: str, folded_text: str, alias: str) -> bool:
    if re.fullmatch(r"[A-Za-z0-9]+", alias):
        return (
            re.search(
                rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])",
                text,
                flags=re.IGNORECASE,
            )
            is not None
        )
    return alias.casefold() in folded_text
