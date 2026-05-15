from __future__ import annotations

from pathlib import Path

REVIEW = Path("docs/INTERNAL_VALIDATION_REVIEW_RU.md")


def _review_text() -> str:
    return " ".join(REVIEW.read_text(encoding="utf-8").casefold().split())


def test_internal_readiness_review_records_required_gate_results() -> None:
    text = _review_text()

    required_gate_results = (
        "reproducibility",
        "pass",
        "explainability",
        "scenario coverage",
        "two-minute demo readability",
        "claim safety",
        "manifest content hash",
        "source row ids",
        "max daily loss",
        "max drawdown",
        "cooldown",
        "max position size",
        "forbidden asset",
    )
    for phrase in required_gate_results:
        assert phrase in text


def test_internal_readiness_review_preserves_paid_pilot_gate() -> None:
    text = _review_text()

    required_market_gate = (
        "market validation still requires real trader evidence",
        "3 paid audit reports",
        "10 qualified prospects",
        "within 14 days",
        "2 repeat audit commitments",
        "within 30 days",
        "public sample artifacts must not be counted",
        "qualified prospect calls",
        "paid pilot reports",
        "pmf evidence",
        "proof that traders will pay",
    )
    for phrase in required_market_gate:
        assert phrase in text


def test_internal_readiness_review_states_go_no_go_action() -> None:
    text = _review_text()

    assert "go for manual trader outreach" in text
    assert "no product blocker prevents manual outreach" in text
    concrete_actions = (
        "contact 20 warm or semi-warm prospects",
        "run 10 past-behavior calls",
        "ask for real trade export plus written risk rules",
        "one-time manual audit at $49-$149",
        "track every non-sensitive objection",
    )
    for action in concrete_actions:
        assert action in text

    concrete_risks = (
        "refuse to pay",
        "unsupported columns",
        "dispute p&l attribution",
        "forbidden scope",
        "do not build new feature scope until paid evidence justifies it",
    )
    for risk in concrete_risks:
        assert risk in text
