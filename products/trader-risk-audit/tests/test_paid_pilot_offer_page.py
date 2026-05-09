from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RU = ROOT / "docs" / "PAID_PILOT_OFFER_RU.md"
EN = ROOT / "docs" / "PAID_PILOT_OFFER_EN.md"


def test_offer_page_contains_required_sections() -> None:
    for text in _docs():
        required = (
            "deliverables",
            "required inputs",
            "timeline",
            "privacy boundary",
            "no-advice boundary",
            "pilot price placeholder",
            "paid pilot cta",
            "manual audit",
        )
        for phrase in required:
            assert phrase in text


def test_offer_page_preserves_claim_boundaries() -> None:
    for text in _docs():
        required = (
            "not pmf",
            "no guaranteed improvement",
            "no performance prediction",
            "no broker control",
            "no live risk prevention",
            "not investment advice",
            "does not control live trading",
        )
        for phrase in required:
            assert phrase in text


def test_offer_page_references_conversion_assets() -> None:
    for text in _docs():
        required = (
            "demo_script",
            "before_after_report_comparison",
            "objection_handling",
            "pilot intake contract",
            "docs/demo_script_ru.md",
            "docs/before_after_report_comparison_ru.md",
            "docs/objection_handling_ru.md",
            "docs/pilot_intake_contract_ru.md",
        )
        for phrase in required:
            assert phrase in text


def _docs() -> tuple[str, str]:
    return (_normalized(RU), _normalized(EN))


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())
