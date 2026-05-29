from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from signal_sandbox.claims import (
    ClaimDirection,
    StructuredClaimExtractor,
    StructuredClaimType,
    extract_structured_claims,
)
from signal_sandbox.corpus import SourceDocument


def test_structured_claim_extractor_emits_rows_from_source_document() -> None:
    claims = extract_structured_claims(
        _document("long #BTC entry 100 stop 90 target 130 rr 2 7d")
    )

    assert len(claims) == 1
    claim = claims[0]
    assert claim.source_document_id == "doc-1"
    assert claim.claim_type == StructuredClaimType.TRADE_SETUP
    assert claim.assets == ["BTC"]
    assert claim.direction == ClaimDirection.LONG
    assert claim.entry is not None
    assert claim.stop is not None
    assert claim.target is not None
    assert claim.risk_reward is not None
    assert claim.horizon_hint == ["7d"]


def test_structured_claim_extractor_distinguishes_claim_types() -> None:
    extractor = StructuredClaimExtractor()
    cases = {
        "long #BTC entry 100 stop 90 target 130": StructuredClaimType.TRADE_SETUP,
        "#ETH bullish for the week": StructuredClaimType.DIRECTIONAL_THESIS,
        "держу позиция #SBER long": StructuredClaimType.POSITION_DISCLOSURE,
        "#BTC закрыл шорт": StructuredClaimType.TRADE_MANAGEMENT,
        "risk warning no trade after invalidation": StructuredClaimType.RISK_WARNING,
        "macro context, no specific asset": StructuredClaimType.CONTEXT_ONLY,
    }

    for index, (text, claim_type) in enumerate(cases.items(), start=1):
        claim = extractor.extract(_document(text, document_id=f"doc-{index}"))[0]
        assert claim.claim_type == claim_type


def test_levels_only_populate_from_evidence_and_missing_fields_block() -> None:
    claim = extract_structured_claims(_document("#BTC выше 100, стоп 90"))[0]
    spans = {span.supports: span for span in claim.evidence_spans}

    assert claim.claim_type == StructuredClaimType.TRADE_SETUP
    assert claim.entry is not None
    assert claim.stop is not None
    assert claim.target is None
    assert "missing_target" in claim.blockers
    assert "entry" in spans
    assert "stop" in spans
    assert "target" not in spans


def test_extractor_records_ambiguity_and_blocked_asset_tokens() -> None:
    claim = extract_structured_claims(
        _document("long #BTC and #ETH, sign-up bonus is not an asset")
    )[0]

    assert claim.assets == ["BTC", "ETH"]
    assert "multiple_assets" in claim.ambiguity_flags
    assert "blocked_asset_token:SIGN-UP" in claim.blockers


def _document(text: str, *, document_id: str = "doc-1") -> SourceDocument:
    return SourceDocument(
        document_id=document_id,
        capture_id=f"capture-{document_id}",
        source_id="test_channel",
        author="test_channel",
        timestamp_utc=datetime(2026, 5, 19, tzinfo=UTC),
        text=text,
        evidence_url=f"https://t.me/test/{document_id}",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )
