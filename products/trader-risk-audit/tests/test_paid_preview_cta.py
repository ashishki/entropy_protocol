from __future__ import annotations

from pathlib import Path

RU = Path("docs/PAID_PILOT_OFFER_RU.md").read_text(encoding="utf-8")
EN = Path("docs/PAID_PILOT_OFFER_EN.md").read_text(encoding="utf-8")


def test_paid_preview_cta_package_terms() -> None:
    combined = f"{RU}\n{EN}"

    assert "One manual audit report" in combined
    assert "48-72 hours" in combined
    assert "$49-$149" in combined
    assert "Real trade export" in combined
    assert "Written risk rules" in combined


def test_paid_preview_cta_boundaries() -> None:
    combined = f"{RU}\n{EN}".casefold()

    assert "static paid pilot offer" in combined
    assert "saas checkout" in combined
    assert "account system" in combined
    assert "no checkout flow is implemented" in combined
    assert "not investment advice" in combined
    assert "does not control live trading" in combined
    assert "no guaranteed improvement" in combined
    assert "stripe" not in combined
