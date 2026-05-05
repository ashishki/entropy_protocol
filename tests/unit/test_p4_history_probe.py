"""Unit tests for P4 history eligibility probes."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from entropy.evidence.crypto_universe import get_default_phase0_crypto_universe
from entropy.evidence.p4_history_probe import (
    P4_HISTORY_PROBE_ID,
    render_p4_history_probe_summary,
    run_p4_history_probe,
)

UTC_TS = datetime(2026, 5, 5, tzinfo=timezone.utc)


def test_run_p4_history_probe_marks_eligible_assets(tmp_path: Path) -> None:
    universe = get_default_phase0_crypto_universe()

    result = run_p4_history_probe(
        universe=universe,
        output_dir=tmp_path,
        generated_at=UTC_TS,
        start_year=2020,
        start_month=1,
        end_year=2025,
        end_month=12,
        required_assets=15,
        url_exists=lambda _url: True,
        max_workers=4,
    )
    rendered = render_p4_history_probe_summary(result)

    assert result.probe_id == P4_HISTORY_PROBE_ID
    assert result.eligible_assets == 20
    assert result.universe_eligible is True
    assert result.rows[0].continuous_month_count == 72
    assert result.rows[0].estimated_completed_weeks >= 312
    assert result.rows[0].estimated_valid_labeled_weeks >= 156
    assert result.manifest_path.exists()
    assert "Universe eligible: `true`" in rendered


def test_run_p4_history_probe_marks_missing_suffix_ineligible(tmp_path: Path) -> None:
    universe = get_default_phase0_crypto_universe()

    def exists(url: str) -> bool:
        return not ("BTCUSDT-1d-2025-12.zip" in url or "ETHUSDT-1d-2025-12.zip" in url)

    result = run_p4_history_probe(
        universe=universe,
        output_dir=tmp_path,
        generated_at=UTC_TS,
        start_year=2025,
        start_month=11,
        end_year=2025,
        end_month=12,
        required_assets=20,
        required_completed_weeks=1,
        required_valid_labeled_weeks=1,
        warmup_weeks=0,
        url_exists=exists,
        max_workers=4,
    )

    btc = result.rows[0]
    assert btc.symbol == "BTCUSDT"
    assert btc.continuous_month_count == 0
    assert btc.eligible is False
    assert btc.reason_code == "insufficient_continuous_history"
