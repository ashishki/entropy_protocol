from __future__ import annotations

from pathlib import Path

from signal_sandbox.reports import is_customer_safe_wording

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_paid_pilot_offer_includes_scope_price_turnaround_and_deliverables() -> None:
    offer = (PROJECT_ROOT / "docs/pilot/PAID_PILOT_OFFER.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "## Scope",
        "## Deliverables",
        "## Price Hypothesis",
        "USD 2,500-7,500",
        "## Turnaround",
        "5-10 business days",
        "## External Boundary",
    ):
        assert required in offer


def test_paid_pilot_offer_defines_exclusions_and_safe_boundary() -> None:
    offer = (PROJECT_ROOT / "docs/pilot/PAID_PILOT_OFFER.md").read_text(
        encoding="utf-8"
    )

    for required in (
        "not trading advice",
        "not a live signal service",
        "unreviewed transcript/OCR/chart claims",
        "unsupported provider/proxy assumptions",
        "Gate: `approve_internal_only`",
        "Current gate decision is",
    ):
        assert required in offer

    assert is_customer_safe_wording(offer)
