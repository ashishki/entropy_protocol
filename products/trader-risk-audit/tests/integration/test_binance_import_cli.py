from __future__ import annotations

import json

import pytest

from trader_risk_audit.cli import main


def test_binance_import_requires_symbols_and_range(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as missing_symbol:
        main(
            [
                "exchange-import",
                "binance-spot-plan",
                "--start-time",
                "2026-04-01T00:00:00Z",
                "--end-time",
                "2026-04-02T00:00:00Z",
            ]
        )
    with pytest.raises(SystemExit) as missing_start_time:
        main(
            [
                "exchange-import",
                "binance-spot-plan",
                "--symbol",
                "BTCUSDT",
                "--end-time",
                "2026-04-02T00:00:00Z",
            ]
        )
    with pytest.raises(SystemExit) as missing_end_time:
        main(
            [
                "exchange-import",
                "binance-spot-plan",
                "--symbol",
                "BTCUSDT",
                "--start-time",
                "2026-04-01T00:00:00Z",
            ]
        )

    assert missing_symbol.value.code == 2
    assert missing_start_time.value.code == 2
    assert missing_end_time.value.code == 2

    result = main(
        [
            "exchange-import",
            "binance-spot-plan",
            "--symbol",
            "BTCUSDT",
            "--start-time",
            "2026-04-01T00:00:00Z",
            "--end-time",
            "2026-04-02T00:00:00Z",
        ]
    )

    payload = json.loads(capsys.readouterr().out)
    assert result == 0
    assert payload["exchange"] == "binance"
    assert payload["market"] == "spot"
    assert payload["symbols"] == ["BTCUSDT"]
    assert payload["source_endpoint_labels"] == ["binance.spot.my_trades"]
    assert payload["windows"][0]["path"] == "/api/v3/myTrades"
