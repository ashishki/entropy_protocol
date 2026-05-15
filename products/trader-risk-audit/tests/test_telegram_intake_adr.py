from __future__ import annotations

from pathlib import Path

ADR = Path("docs/adr/ADR-001-telegram-intake-delivery.md")


def test_adr_declares_allowed_and_forbidden_telegram_scope() -> None:
    text = _adr_text()

    allowed_scope = (
        "telegram may receive user files",
        "return status",
        "deliver approved reports",
    )
    for phrase in allowed_scope:
        assert phrase in text

    forbidden_scope = (
        "may not connect to brokers",
        "accept api keys",
        "block orders",
        "parse signal channels",
        "generate trading advice",
    )
    for phrase in forbidden_scope:
        assert phrase in text


def test_adr_preserves_operator_approval_and_deterministic_truth() -> None:
    text = _adr_text()

    required_phrases = (
        "operator approval is required before report delivery",
        "deterministic artifact",
        "final violation truth remains in deterministic audit artifacts",
        "normalized trades",
        "approved policy",
        "violation records",
        "attribution summary",
        "artifact manifest hashes",
        "must not create new claims",
    )
    for phrase in required_phrases:
        assert phrase in text


def test_adr_documents_security_and_retention_boundaries() -> None:
    text = _adr_text()

    required_phrases = (
        "environment variables",
        "must not contain raw user files",
        "telegram handles",
        "pilot files remain local by default",
        "operator-controlled workspace",
        "no hosted database",
        "local retention/delete workflow",
        "deletion must be explicit",
    )
    for phrase in required_phrases:
        assert phrase in text


def _adr_text() -> str:
    return " ".join(ADR.read_text(encoding="utf-8").casefold().split())
