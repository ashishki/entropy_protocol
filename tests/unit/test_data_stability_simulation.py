from __future__ import annotations

from datetime import date

from entropy.evidence.data_stability_simulation import generate_fixture_stability_window


def test_generate_fixture_stability_window_reaches_mechanical_ready_state(tmp_path) -> None:
    result = generate_fixture_stability_window(
        output_dir=tmp_path,
        start_date=date(2026, 1, 1),
        day_count=90,
        target_symbols=("BTC-USD", "ETH-USD"),
    )

    assert result.fixture_only is True
    assert result.gate_claim_allowed is False
    assert result.row_count == 180
    assert result.summary.monitored_day_count == 90
    assert result.summary.missing_symbol_days == 0
    assert result.summary.unexplained_gap_count == 0
    assert result.summary.packet_status == "PACKET_READY_FOR_REVIEW"
    assert result.rows_path.exists()
    assert result.summary_path.exists()


def test_generate_fixture_stability_window_keeps_short_window_incomplete(tmp_path) -> None:
    result = generate_fixture_stability_window(
        output_dir=tmp_path,
        start_date=date(2026, 1, 1),
        day_count=89,
        target_symbols=("BTC-USD",),
    )

    assert result.summary.monitored_day_count == 89
    assert result.summary.packet_status == "INCOMPLETE"
