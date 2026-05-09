from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RU = ROOT / "docs" / "OBJECTION_HANDLING_RU.md"
EN = ROOT / "docs" / "OBJECTION_HANDLING_EN.md"


def test_objection_pack_covers_required_objections() -> None:
    for text in _docs():
        required = (
            "privacy",
            "broker api",
            "no advice",
            "why not my journal",
            "pricing",
            "repeat audit",
        )
        for phrase in required:
            assert phrase in text


def test_objection_pack_preserves_claim_boundaries() -> None:
    for text in _docs():
        required = (
            "not legal advice",
            "not investment advice",
            "no performance promise",
            "does not control live trading",
            "no broker apis",
            "no order blocking",
            "no signal parsing",
        )
        for phrase in required:
            assert phrase in text


def test_objection_pack_points_to_pilot_gate() -> None:
    for text in _docs():
        required = (
            "pilot intake contract",
            "paid pilot evidence gate",
            "10 qualified prospects",
            "5 exports/rules",
            "3 paid audits",
            "2 repeat audit commitments",
        )
        for phrase in required:
            assert phrase in text


def _docs() -> tuple[str, str]:
    return (_normalized(RU), _normalized(EN))


def _normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").casefold().split())
