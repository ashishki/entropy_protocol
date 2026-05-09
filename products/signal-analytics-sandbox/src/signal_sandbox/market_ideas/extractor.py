"""Deterministic MarketIdea draft extractor."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.profiles import ChannelProfile, ChannelProfileRegistry

METADATA_VERSION = "market_idea.v0.1"


class IdeaType(StrEnum):
    TRADE_SETUP = "trade_setup"
    DIRECTIONAL_THESIS = "directional_thesis"
    MARKET_REGIME = "market_regime"
    WATCHLIST = "watchlist"
    CATALYST_REACTION = "catalyst_reaction"
    RISK_WARNING = "risk_warning"
    NON_MARKET = "non_market"


class Direction(StrEnum):
    LONG = "long"
    SHORT = "short"
    FLAT = "flat"
    MIXED = "mixed"
    UNKNOWN = "unknown"


class ApprovalState(StrEnum):
    DRAFT = "draft"
    QUEUED_FOR_REVIEW = "queued_for_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXCLUDED = "excluded"


class ExtractionSource(StrEnum):
    RULE = "rule"


class ResolutionState(StrEnum):
    RESOLVED = "resolved"
    AMBIGUOUS = "ambiguous"
    UNRESOLVED = "unresolved"
    NOT_APPLICABLE = "not_applicable"


class EvidenceSpan(BaseModel):
    model_config = ConfigDict(strict=True)

    span_id: str = Field(min_length=1)
    source_document_id: str = Field(min_length=1)
    start_char: int = Field(ge=0)
    end_char: int = Field(gt=0)
    excerpt: str = Field(min_length=1)
    supports: str = Field(
        pattern=(
            "^(asset|direction|entry|stop_or_invalidation|target_or_horizon|"
            "idea_type|risk|catalyst|non_market|uncertainty)$"
        )
    )
    support_strength: str = Field(pattern="^(explicit|implied|weak)$")


class MarketIdeaDraft(BaseModel):
    model_config = ConfigDict(strict=True)

    idea_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_document_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)
    source_timestamp_utc: datetime
    extracted_timestamp_utc: datetime
    idea_type: IdeaType
    approval_state: ApprovalState
    extraction_source: ExtractionSource
    evidence_spans: list[EvidenceSpan] = Field(default_factory=list)
    resolution_state: ResolutionState
    review_required: bool
    metadata_version: str = METADATA_VERSION
    asset_mentions: list[str] = Field(default_factory=list)
    direction: Direction = Direction.UNKNOWN
    horizon_hint: list[str] = Field(default_factory=list)
    confidence: Decimal = Decimal("0")
    ambiguity_flags: list[str] = Field(default_factory=list)
    rag_context_refs: list[str] = Field(default_factory=list)

    @field_validator("source_timestamp_utc", "extracted_timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp must be a datetime or ISO-8601 string")


class MarketIdeaDraftExtractor:
    def __init__(self, profile_registry: ChannelProfileRegistry | None = None):
        self.profile_registry = profile_registry or ChannelProfileRegistry()

    def extract(self, document: SourceDocument) -> MarketIdeaDraft:
        profile = self.profile_registry.get(document.source_id)
        asset_mentions = _asset_mentions(document.text, profile)
        direction = _direction(document.text)
        idea_type = _idea_type(document.text, asset_mentions, direction)
        horizons = _horizon_hints(document.text)
        evidence_spans = _evidence_spans(
            document=document,
            idea_type=idea_type,
            asset_mentions=asset_mentions,
            direction=direction,
            horizons=horizons,
        )
        return MarketIdeaDraft(
            idea_id=_idea_id(document, idea_type),
            source_id=document.source_id,
            capture_id=document.capture_id,
            source_document_id=document.document_id,
            evidence_url=document.evidence_url,
            text_sha256=document.text_sha256,
            source_timestamp_utc=document.timestamp_utc,
            extracted_timestamp_utc=document.timestamp_utc,
            idea_type=idea_type,
            approval_state=ApprovalState.QUEUED_FOR_REVIEW,
            extraction_source=ExtractionSource.RULE,
            evidence_spans=evidence_spans,
            resolution_state=_resolution_state(idea_type, asset_mentions),
            review_required=True,
            asset_mentions=asset_mentions,
            direction=direction,
            horizon_hint=horizons,
            confidence=_confidence(idea_type, asset_mentions, direction),
            ambiguity_flags=_ambiguity_flags(idea_type, asset_mentions, direction),
        )


def _asset_mentions(text: str, profile: ChannelProfile | None) -> list[str]:
    matches: list[str] = []
    if profile is not None:
        for term in profile.accepted_draft_terms:
            if (
                term.category == "asset_alias"
                and term.term.casefold() in text.casefold()
            ):
                matches.append(term.term.lstrip("#$").upper())
    if not matches:
        matches.extend(
            token.lstrip("#$").upper()
            for token in re.findall(r"[$#][A-Za-z]{2,10}", text)
        )
    return sorted(set(matches))


def _direction(text: str) -> Direction:
    folded = text.casefold()
    long = any(term in folded for term in ("long", "buy", "bullish", "upside", "рост"))
    short = any(
        term in folded for term in ("short", "sell", "bearish", "downside", "паден")
    )
    flat = any(term in folded for term in ("flat", "range", "neutral", "боков"))
    if (long and short) or (flat and (long or short)):
        return Direction.MIXED
    if long:
        return Direction.LONG
    if short:
        return Direction.SHORT
    if flat:
        return Direction.FLAT
    return Direction.UNKNOWN


def _idea_type(
    text: str,
    asset_mentions: list[str],
    direction: Direction,
) -> IdeaType:
    folded = text.casefold()
    has_trade_fields = _contains_any(
        folded,
        ("entry", "вход", "stop", "target", "цель"),
    )
    if (
        asset_mentions
        and direction in {Direction.LONG, Direction.SHORT}
        and has_trade_fields
    ):
        return IdeaType.TRADE_SETUP
    if _contains_any(folded, ("watchlist", "watch", "наблюда", "след", "wait")):
        return IdeaType.WATCHLIST
    if _contains_any(folded, ("etf", "earnings", "cpi", "fed", "санкц", "news")):
        return IdeaType.CATALYST_REACTION
    if _contains_any(
        folded,
        ("risk-on", "risk-off", "liquidity", "volatility", "regime"),
    ):
        return IdeaType.MARKET_REGIME
    if _contains_any(folded, ("risk", "warning", "invalid", "no trade", "отмена")):
        return IdeaType.RISK_WARNING
    if asset_mentions and direction != Direction.UNKNOWN:
        return IdeaType.DIRECTIONAL_THESIS
    return IdeaType.NON_MARKET


def _horizon_hints(text: str) -> list[str]:
    folded = text.casefold()
    horizons: list[str] = []
    for label in ("intraday", "1d", "3d", "7d", "30d"):
        if label in folded:
            horizons.append(label)
    if "week" in folded or "недел" in folded:
        horizons.append("7d")
    if "month" in folded or "месяц" in folded:
        horizons.append("30d")
    return sorted(set(horizons)) or ["unspecified"]


def _evidence_spans(
    *,
    document: SourceDocument,
    idea_type: IdeaType,
    asset_mentions: list[str],
    direction: Direction,
    horizons: list[str],
) -> list[EvidenceSpan]:
    spans: list[EvidenceSpan] = []
    for asset in asset_mentions:
        span = _find_first_span(
            document,
            (f"#{asset}", f"${asset}", asset),
            "asset",
            len(spans),
        )
        if span is not None:
            spans.append(span)
    direction_span = _find_direction_span(document, direction, len(spans))
    if direction_span is not None:
        spans.append(direction_span)
    for support, terms in (
        ("stop_or_invalidation", ("stop", "invalid", "invalidation", "отмена")),
        ("target_or_horizon", (*horizons, "target", "цель")),
        ("catalyst", ("etf", "earnings", "cpi", "fed", "санкц", "news")),
        ("risk", ("risk", "warning", "no trade", "отмена")),
    ):
        span = _find_first_span(document, terms, support, len(spans))
        if span is not None:
            spans.append(span)
    if not spans:
        spans.append(_fallback_span(document, idea_type))
    return spans


def _find_direction_span(
    document: SourceDocument,
    direction: Direction,
    index: int,
) -> EvidenceSpan | None:
    if direction == Direction.LONG:
        return _find_first_span(
            document, ("long", "buy", "bullish", "upside", "рост"), "direction", index
        )
    if direction == Direction.SHORT:
        return _find_first_span(
            document,
            ("short", "sell", "bearish", "downside", "паден"),
            "direction",
            index,
        )
    if direction == Direction.FLAT:
        return _find_first_span(
            document,
            ("flat", "range", "neutral"),
            "direction",
            index,
        )
    return None


def _find_first_span(
    document: SourceDocument,
    terms: tuple[str, ...],
    support: str,
    index: int,
) -> EvidenceSpan | None:
    for term in terms:
        if term == "unspecified":
            continue
        span = _find_span(document, term, support, index)
        if span is not None:
            return span
    return None


def _find_span(
    document: SourceDocument,
    term: str,
    support: str,
    index: int,
) -> EvidenceSpan | None:
    match = re.search(re.escape(term), document.text, flags=re.IGNORECASE)
    if match is None:
        return None
    return EvidenceSpan(
        span_id=f"span-{index + 1}",
        source_document_id=document.document_id,
        start_char=match.start(),
        end_char=match.end(),
        excerpt=document.text[match.start() : match.end()],
        supports=support,
        support_strength="explicit",
    )


def _fallback_span(document: SourceDocument, idea_type: IdeaType) -> EvidenceSpan:
    excerpt = document.text[:80] or "empty source text"
    return EvidenceSpan(
        span_id="span-1",
        source_document_id=document.document_id,
        start_char=0,
        end_char=max(len(excerpt), 1),
        excerpt=excerpt,
        supports="non_market" if idea_type == IdeaType.NON_MARKET else "idea_type",
        support_strength="weak",
    )


def _resolution_state(
    idea_type: IdeaType,
    asset_mentions: list[str],
) -> ResolutionState:
    if idea_type in {IdeaType.NON_MARKET, IdeaType.RISK_WARNING, IdeaType.WATCHLIST}:
        return ResolutionState.NOT_APPLICABLE
    if len(asset_mentions) == 1:
        return ResolutionState.RESOLVED
    if len(asset_mentions) > 1:
        return ResolutionState.AMBIGUOUS
    return ResolutionState.UNRESOLVED


def _confidence(
    idea_type: IdeaType,
    asset_mentions: list[str],
    direction: Direction,
) -> Decimal:
    if idea_type == IdeaType.NON_MARKET:
        return Decimal("0.30")
    if asset_mentions and direction != Direction.UNKNOWN:
        return Decimal("0.75")
    return Decimal("0.55")


def _ambiguity_flags(
    idea_type: IdeaType,
    asset_mentions: list[str],
    direction: Direction,
) -> list[str]:
    flags: list[str] = []
    if idea_type != IdeaType.NON_MARKET and not asset_mentions:
        flags.append("missing_asset")
    if idea_type not in {IdeaType.NON_MARKET, IdeaType.MARKET_REGIME}:
        if direction == Direction.UNKNOWN:
            flags.append("missing_direction")
        if direction == Direction.MIXED:
            flags.append("mixed_direction")
    return flags


def _idea_id(document: SourceDocument, idea_type: IdeaType) -> str:
    payload = "|".join(
        [
            document.source_id,
            document.capture_id,
            document.document_id,
            document.text_sha256,
            idea_type.value,
            METADATA_VERSION,
        ]
    )
    return f"idea-{hashlib.sha256(payload.encode()).hexdigest()[:16]}"


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)
