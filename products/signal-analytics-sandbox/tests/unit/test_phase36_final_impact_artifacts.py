from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _read(relative_path: str) -> str:
    return (PROJECT_ROOT / relative_path).read_text(encoding="utf-8")


def test_impact_claim_taxonomy_distinguishes_pnl_and_non_pnl_claims() -> None:
    taxonomy = _read("docs/specs/CHANNEL_IMPACT_CLAIM_TAXONOMY.md")

    for required in (
        "`explicit_trade_setup`",
        "`trend_regime_view`",
        "`macro_thesis`",
        "`risk_process_statement`",
        "`watchlist`",
        "`non_market_commentary`",
        "Non-PnL claims cannot become win/loss rows",
        "`evidence_confidence`",
        "`customer_facing_allowed`",
    ):
        assert required in taxonomy


def test_dashboard_schema_and_paid_boundary_preserve_product_guardrails() -> None:
    schema = _read("docs/specs/CHANNEL_DASHBOARD_SCORE_SCHEMA.md")
    boundary = _read("docs/specs/PAID_CHANNEL_REPORT_BOUNDARY.md")

    for required in (
        "`signal_performance`",
        "`trend_sense`",
        "`insight_depth`",
        "`methodology_clarity`",
        "`risk_discipline`",
        "`practical_usefulness`",
        "`creativity`",
        "`evidence_confidence`",
        "`external_gate`",
        "`best_channel`",
        "`investment_advice`",
    ):
        assert required in schema

    for required in (
        "full claim ledger",
        "confirmed and contradicted examples",
        "methodology and risk-management notes",
        "Every public dashboard and every paid deep report needs an explicit",
        "future-profit claims",
    ):
        assert required in boundary


def test_phase36_scorecard_and_gate_are_internal_only_and_three_channel() -> None:
    scorecard = _read("docs/pilot/three_channel_PHASE36_IMPACT_SCORECARD.md")
    gate = _read("docs/pilot/three_channel_PHASE36_EXTERNAL_READY_GATE.md")
    review = _read("docs/archive/PHASE36_DEEP_REVIEW.md")

    for channel in ("`bablos79`", "`nemphiscrypts`", "`pifagortrade`"):
        assert channel in scorecard

    assert "Public dashboard use is not approved yet" in scorecard
    assert "Decision: `approve_internal_dashboard_prototype_only`" in gate
    assert "External delivery: `not_approved`" in gate
    assert "pass_internal_dashboard_prototype_only" in review
