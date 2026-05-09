from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RU = ROOT / "docs" / "ICP_DEMO_VARIANTS_RU.md"
EN = ROOT / "docs" / "ICP_DEMO_VARIANTS_EN.md"
ICPS = (
    "prop/funded traders",
    "active crypto discretionary traders",
    "small teams/coaches",
)


def test_icp_variants_cover_required_sections() -> None:
    for text in _docs():
        for icp in ICPS:
            assert icp in text
        required_sections = (
            "likely pain",
            "current workaround",
            "demo angle",
            "required proof",
            "paid pilot ask",
        )
        for section in required_sections:
            assert text.count(section) >= len(ICPS)


def test_icp_variants_preserve_product_boundary() -> None:
    for text in _docs():
        required = (
            "post-trade audit",
            "no broker control",
            "no signal analytics",
            "not investment advice",
            "does not control live trading",
            "no order blocking",
        )
        for phrase in required:
            assert phrase in text


def test_icp_variants_map_to_validation_gate() -> None:
    for text in _docs():
        required = (
            "same validation evidence gate",
            "10 qualified prospects",
            "5 exports/rules",
            "3 paid audits",
            "2 repeat audit commitments",
            "not vanity metrics",
        )
        for phrase in required:
            assert phrase in text


def _docs() -> tuple[str, str]:
    return (_normalized(RU), _normalized(EN))


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())
