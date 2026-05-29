from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DASHBOARD = PROJECT_ROOT / "docs/pilot/preclient_dashboard/index.html"


def test_preclient_dashboard_static_renders_all_channel_cards() -> None:
    html = DASHBOARD.read_text(encoding="utf-8")

    assert "<title>Signal Analytics Pre-Client Dashboard</title>" in html
    assert html.count('class="channel-card"') == 3
    for channel in ("bablos79", "nemphiscrypts", "pifagortrade"):
        assert f'data-source-id="{channel}"' in html
        assert f"../reports/preclient/{channel}_DEEP_REPORT_V0.md" in html


def test_preclient_dashboard_static_shows_required_card_status_fields() -> None:
    html = DASHBOARD.read_text(encoding="utf-8")

    assert html.count("internal_only_not_dashboard_safe") == 3
    assert html.count("<b>evidence confidence</b> low") == 3
    assert html.count('<span class="metric-label">sample</span>') == 3
    assert html.count('<span class="metric-label">media</span>') == 3
    assert html.count('<span class="metric-label">RR/setup</span>') == 3
    assert html.count("<b>no-advice</b> internal research only") == 3
    assert "../preclient_FREE_DASHBOARD_CARDS.json" in html
    assert "../preclient_EVIDENCE_APPENDIX.md" in html
    assert "../preclient_CANDIDATE_OUTCOMES.md" in html


def test_preclient_dashboard_static_avoids_forbidden_external_flows() -> None:
    html = DASHBOARD.read_text(encoding="utf-8").lower()

    for forbidden in (
        "payment",
        "checkout",
        "subscribe",
        "pricing",
        "buy now",
        "best channel",
        "leaderboard",
        "marketplace",
        "future profit",
        "private-source",
        "private source",
        "private group",
        "guaranteed",
        "$",
    ):
        assert forbidden not in html
