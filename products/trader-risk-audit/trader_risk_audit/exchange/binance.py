from __future__ import annotations

import hashlib
import hmac
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

from trader_risk_audit.exchange.credentials import REDACTED_VALUE, ExchangeCredentials

BINANCE_SPOT_MY_TRADES_ENDPOINT = "binance.spot.my_trades"
BINANCE_SPOT_MY_TRADES_PATH = "/api/v3/myTrades"
BINANCE_ALLOWED_ENDPOINT_LABELS = (BINANCE_SPOT_MY_TRADES_ENDPOINT,)
_SIGNED_QUERY_PARAM_ORDER = (
    "symbol",
    "startTime",
    "endTime",
    "timestamp",
    "recvWindow",
    "limit",
)


class BinanceSigningError(ValueError):
    pass


@dataclass(frozen=True, repr=False)
class BinanceSignedRequest:
    endpoint_label: str
    method: str
    path: str
    query_string: str
    headers: Mapping[str, str]
    signature: str

    def __repr__(self) -> str:
        return (
            "BinanceSignedRequest("
            f"endpoint_label={self.endpoint_label!r}, "
            f"method={self.method!r}, "
            f"path={self.path!r}, "
            f"query_string={_redact_signature_from_query(self.query_string)!r}, "
            f"headers={self.safe_headers()!r}, "
            f"signature={REDACTED_VALUE!r})"
        )

    def safe_headers(self) -> dict[str, str]:
        return {"X-MBX-APIKEY": REDACTED_VALUE}

    def to_safe_metadata(self) -> dict[str, object]:
        return {
            "endpoint_label": self.endpoint_label,
            "method": self.method,
            "path": self.path,
            "query_string": _redact_signature_from_query(self.query_string),
            "headers": self.safe_headers(),
            "signature": REDACTED_VALUE,
        }


@dataclass(frozen=True, repr=False)
class BinanceSigner:
    credentials: ExchangeCredentials

    def __post_init__(self) -> None:
        if self.credentials.exchange.casefold() != "binance":
            raise BinanceSigningError("Binance signer requires Binance credentials")

    def __repr__(self) -> str:
        return (
            "BinanceSigner("
            f"credentials={self.credentials.to_safe_metadata()!r}, "
            f"allowed_endpoint_labels={BINANCE_ALLOWED_ENDPOINT_LABELS!r})"
        )

    def sign_my_trades_request(
        self,
        *,
        symbol: str,
        start_time_ms: int,
        end_time_ms: int,
        timestamp_ms: int,
        recv_window_ms: int = 5000,
        limit: int | None = None,
    ) -> BinanceSignedRequest:
        params: dict[str, object] = {
            "symbol": _require_non_blank(symbol, field="symbol"),
            "startTime": _require_positive_int(start_time_ms, field="start_time_ms"),
            "endTime": _require_positive_int(end_time_ms, field="end_time_ms"),
            "timestamp": _require_positive_int(timestamp_ms, field="timestamp_ms"),
            "recvWindow": _require_positive_int(recv_window_ms, field="recv_window_ms"),
        }
        if params["startTime"] > params["endTime"]:
            raise BinanceSigningError("start_time_ms must be <= end_time_ms")
        if limit is not None:
            params["limit"] = _require_positive_int(limit, field="limit")
        return sign_binance_account_request(
            credentials=self.credentials,
            endpoint_label=BINANCE_SPOT_MY_TRADES_ENDPOINT,
            path=BINANCE_SPOT_MY_TRADES_PATH,
            params=params,
        )


def sign_binance_account_request(
    *,
    credentials: ExchangeCredentials,
    endpoint_label: str,
    path: str,
    params: Mapping[str, object],
) -> BinanceSignedRequest:
    if credentials.exchange.casefold() != "binance":
        raise BinanceSigningError("Binance signed requests require Binance credentials")
    if endpoint_label not in BINANCE_ALLOWED_ENDPOINT_LABELS:
        raise BinanceSigningError("unsupported Binance account-data endpoint label")
    if path != BINANCE_SPOT_MY_TRADES_PATH:
        raise BinanceSigningError("unsupported Binance account-data path")

    query_without_signature = urlencode(_ordered_query_params(params))
    signature = hmac.new(
        credentials.api_secret.encode("utf-8"),
        query_without_signature.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    query_string = f"{query_without_signature}&signature={signature}"
    return BinanceSignedRequest(
        endpoint_label=endpoint_label,
        method="GET",
        path=path,
        query_string=query_string,
        headers={"X-MBX-APIKEY": credentials.api_key},
        signature=signature,
    )


def _redact_signature_from_query(query_string: str) -> str:
    parts = []
    for part in query_string.split("&"):
        if part.startswith("signature="):
            parts.append(f"signature={REDACTED_VALUE}")
        else:
            parts.append(part)
    return "&".join(parts)


def _ordered_query_params(params: Mapping[str, object]) -> tuple[tuple[str, str], ...]:
    known = tuple(
        (key, str(params[key])) for key in _SIGNED_QUERY_PARAM_ORDER if key in params
    )
    extras = tuple(
        (key, str(value))
        for key, value in sorted(params.items())
        if key not in _SIGNED_QUERY_PARAM_ORDER
    )
    return known + extras


def _require_non_blank(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise BinanceSigningError(f"{field} must not be blank")
    return text.upper()


def _require_positive_int(value: Any, *, field: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise BinanceSigningError(f"{field} must be an integer") from exc
    if parsed < 1:
        raise BinanceSigningError(f"{field} must be positive")
    return parsed
