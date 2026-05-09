from __future__ import annotations

import json

from trader_risk_audit.exchange.binance import (
    BINANCE_ALLOWED_ENDPOINT_LABELS,
    BINANCE_SPOT_MY_TRADES_ENDPOINT,
    BINANCE_SPOT_MY_TRADES_PATH,
    BinanceSigner,
    BinanceSigningError,
    sign_binance_account_request,
)
from trader_risk_audit.exchange.credentials import ExchangeCredentials


def test_binance_signed_query_is_deterministic() -> None:
    signer = BinanceSigner(_credentials())

    request = signer.sign_my_trades_request(
        symbol="btcusdt",
        start_time_ms=1711963200000,
        end_time_ms=1711966800000,
        timestamp_ms=1711966900000,
        recv_window_ms=5000,
        limit=500,
    )
    repeated = signer.sign_my_trades_request(
        symbol="BTCUSDT",
        start_time_ms=1711963200000,
        end_time_ms=1711966800000,
        timestamp_ms=1711966900000,
        recv_window_ms=5000,
        limit=500,
    )

    assert request == repeated
    assert request.endpoint_label == BINANCE_SPOT_MY_TRADES_ENDPOINT
    assert request.method == "GET"
    assert request.path == BINANCE_SPOT_MY_TRADES_PATH
    assert request.query_string == (
        "symbol=BTCUSDT&startTime=1711963200000&endTime=1711966800000"
        "&timestamp=1711966900000&recvWindow=5000&limit=500"
        "&signature=d18532cf9d4e4a5dfe7cb429864326248ebd7889d41e4187449c622480b37d3b"
    )

    reversed_params_request = sign_binance_account_request(
        credentials=_credentials(),
        endpoint_label=BINANCE_SPOT_MY_TRADES_ENDPOINT,
        path=BINANCE_SPOT_MY_TRADES_PATH,
        params={
            "limit": 500,
            "recvWindow": 5000,
            "timestamp": 1711966900000,
            "endTime": 1711966800000,
            "startTime": 1711963200000,
            "symbol": "BTCUSDT",
        },
    )

    assert reversed_params_request.query_string == request.query_string


def test_binance_signer_redacts_secrets() -> None:
    credentials = _credentials()
    signer = BinanceSigner(credentials)
    request = signer.sign_my_trades_request(
        symbol="BTCUSDT",
        start_time_ms=1711963200000,
        end_time_ms=1711966800000,
        timestamp_ms=1711966900000,
    )
    try:
        sign_binance_account_request(
            credentials=credentials,
            endpoint_label="fixture_binance_secret_456",
            path=BINANCE_SPOT_MY_TRADES_PATH,
            params={"timestamp": 1711966900000},
        )
    except BinanceSigningError as exc:
        error_text = str(exc)
    else:
        raise AssertionError("unsupported endpoint should fail")

    rendered = "\n".join(
        (
            repr(signer),
            repr(request),
            json.dumps(request.to_safe_metadata(), sort_keys=True),
            error_text,
        )
    )

    assert "fixture_binance_key_123" not in rendered
    assert "fixture_binance_secret_456" not in rendered
    assert request.signature not in rendered
    assert "<redacted>" in rendered


def test_binance_client_exposes_no_write_endpoints() -> None:
    rendered = "\n".join(
        (*BINANCE_ALLOWED_ENDPOINT_LABELS, BINANCE_SPOT_MY_TRADES_PATH)
    )

    assert BINANCE_ALLOWED_ENDPOINT_LABELS == (BINANCE_SPOT_MY_TRADES_ENDPOINT,)
    assert "my_trades" in rendered
    for forbidden in ("order", "withdraw", "transfer", "leverage", "margin"):
        assert forbidden not in rendered.casefold()


def _credentials() -> ExchangeCredentials:
    return ExchangeCredentials(
        exchange="binance",
        api_key="fixture_binance_key_123",
        api_secret="fixture_binance_secret_456",
    )
