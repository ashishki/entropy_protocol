from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RU = ROOT / "docs" / "BEFORE_AFTER_REPORT_COMPARISON_RU.md"
EN = ROOT / "docs" / "BEFORE_AFTER_REPORT_COMPARISON_EN.md"


def test_before_after_comparison_uses_safe_sample_data() -> None:
    for text in _docs():
        required = (
            "public sample",
            "demo/public_sample_001",
            "raw trade export",
            "timestamp",
            "symbol",
            "side",
            "quantity",
            "price",
            "no real customer data",
            "no telegram handles",
            "no broker account ids",
        )
        for phrase in required:
            assert phrase in text


def test_before_after_comparison_preserves_claim_boundaries() -> None:
    for text in _docs():
        required = (
            "deterministic rule checks",
            "source row ids",
            "violation-attributed p&l",
            "not investment advice",
            "does not control live trading",
            "no performance promise",
            "no broker apis",
            "no signal parsing",
            "no order blocking",
        )
        for phrase in required:
            assert phrase in text


def test_before_after_comparison_has_paid_pilot_cta() -> None:
    for text in _docs():
        required = (
            "real trade export",
            "written risk rules",
            "paid pilot",
            "manual audit",
            "source rows",
            "p&l impact",
        )
        for phrase in required:
            assert phrase in text


def _docs() -> tuple[str, str]:
    return (_normalized(RU), _normalized(EN))


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())
