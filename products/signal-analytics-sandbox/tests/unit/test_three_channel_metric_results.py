from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_three_channel_metric_results_use_open_public_windows() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_METRIC_RESULTS.json").read_text(
            encoding="utf-8"
        )
    )

    method = artifact["method"]
    assert method["source_method"] == "public_telegram_s_html"
    assert method["bulk_market_database_used"] is False
    assert method["investment_advice"] is False
    assert method["primary_horizon"] == "7d"
    assert method["providers"] == ["binance_public_klines", "moex_iss_candles"]


def test_three_channel_metric_results_compare_all_channels() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_METRIC_RESULTS.json").read_text(
            encoding="utf-8"
        )
    )

    summaries = {row["source_id"]: row for row in artifact["channel_summaries"]}
    assert set(summaries) == {"bablos79", "nemphiscrypts", "pifagortrade"}
    assert artifact["totals"]["primary_evaluable_claims"] >= 150
    assert artifact["totals"]["confirmed_hits"] > 0
    assert artifact["totals"]["contradicted_misses"] > 0
    assert summaries["bablos79"]["provider_counts"]["moex_iss"] >= 10
    assert summaries["nemphiscrypts"]["provider_counts"]["binance"] >= 40
    assert summaries["pifagortrade"]["provider_counts"]["binance"] >= 100


def test_three_channel_metric_report_contains_evidence_and_limits() -> None:
    report = (PROJECT_ROOT / "docs/pilot/three_channel_METRIC_REPORT.md").read_text(
        encoding="utf-8"
    )

    assert "Channel Comparison" in report
    assert "Confirmed Examples" in report
    assert "Contradicted Examples" in report
    assert "not investment advice" in report
    assert "no bulk market-history database" in report
    assert "https://t.me/" in report
