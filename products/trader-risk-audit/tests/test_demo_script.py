from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RU_SCRIPT = ROOT / "docs" / "DEMO_SCRIPT_RU.md"
EN_SCRIPT = ROOT / "docs" / "DEMO_SCRIPT_EN.md"


def test_demo_script_covers_required_flow() -> None:
    for text in _scripts():
        required_flow = (
            "problem",
            "upload",
            "selected profile",
            "report summary",
            "source row ids",
            "p&l impact",
            "next pilot ask",
            "real trade export",
            "written risk rules",
        )
        for phrase in required_flow:
            assert phrase in text


def test_demo_script_preserves_claim_boundaries() -> None:
    for text in _scripts():
        required_boundaries = (
            "not investment advice",
            "does not control live trading",
            "no performance promise",
            "no broker apis",
            "no signal parsing",
            "no order blocking",
            "no auto-advice",
            "public sample is not market validation",
            "not pmf evidence",
        )
        for phrase in required_boundaries:
            assert phrase in text


def test_demo_script_explains_policy_profiles() -> None:
    for text in _scripts():
        required_profile_copy = (
            "soft",
            "medium",
            "hard",
            "custom rules",
            "customizable audit presets",
            "trader custom rules",
            "prop/funded account rules",
            "not optimal risk settings",
        )
        for phrase in required_profile_copy:
            assert phrase in text


def _scripts() -> tuple[str, str]:
    return (
        _normalized(RU_SCRIPT),
        _normalized(EN_SCRIPT),
    )


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())
