from __future__ import annotations

import hashlib
import hmac
import json
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlencode

from trader_risk_audit.exchange.credentials import REDACTED_VALUE, ExchangeCredentials
from trader_risk_audit.exchange.normalizer import normalize_exchange_records
from trader_risk_audit.trades.schema import TradeRecord

BINANCE_SPOT_MY_TRADES_ENDPOINT = "binance.spot.my_trades"
BINANCE_SPOT_MY_TRADES_PATH = "/api/v3/myTrades"
BINANCE_ALLOWED_ENDPOINT_LABELS = (BINANCE_SPOT_MY_TRADES_ENDPOINT,)
BINANCE_SPOT_MARKET = "spot"
BINANCE_SPOT_MY_TRADES_LIMIT = 1000
BINANCE_SPOT_MY_TRADES_WINDOW = timedelta(hours=24)
BINANCE_SUPPORTED_TRADE_FIELDS = frozenset(
    {
        "commission",
        "commission_asset",
        "commissionAsset",
        "id",
        "is_buyer",
        "is_maker",
        "isBuyer",
        "isMaker",
        "order_id",
        "orderId",
        "price",
        "qty",
        "quantity",
        "source_row_id",
        "symbol",
        "time",
        "trade_id",
    }
)
_UNIX_EPOCH = datetime(1970, 1, 1, tzinfo=UTC)
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


class BinanceFetchPlanError(ValueError):
    pass


class BinanceNormalizationError(ValueError):
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


@dataclass(frozen=True)
class BinanceNormalizationWarning:
    field: str
    message: str
    source_ref: str


@dataclass(frozen=True)
class BinanceTradeMetadata:
    row_id: str
    fee_asset: str
    liquidity: str
    source_ref: str


@dataclass(frozen=True)
class BinanceNormalizationResult:
    trades: tuple[TradeRecord, ...]
    metadata: tuple[BinanceTradeMetadata, ...]
    warnings: tuple[BinanceNormalizationWarning, ...]


@dataclass(frozen=True)
class BinanceSpotTradeFetchWindow:
    request_number: int
    symbol: str
    start_time: str
    end_time: str
    start_time_ms: int
    end_time_ms: int
    limit: int = BINANCE_SPOT_MY_TRADES_LIMIT
    endpoint_label: str = BINANCE_SPOT_MY_TRADES_ENDPOINT
    method: str = "GET"
    path: str = BINANCE_SPOT_MY_TRADES_PATH
    market: str = BINANCE_SPOT_MARKET

    def to_source_metadata(self) -> dict[str, object]:
        return asdict(self)

    def to_request_params(self, *, timestamp_ms: int) -> dict[str, int | str]:
        return {
            "symbol": self.symbol,
            "startTime": self.start_time_ms,
            "endTime": self.end_time_ms,
            "timestamp": _require_positive_int(timestamp_ms, field="timestamp_ms"),
            "recvWindow": 5000,
            "limit": self.limit,
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


def plan_binance_spot_trade_fetches(
    *,
    symbols: tuple[str, ...],
    start_time: str,
    end_time: str,
    limit: int = BINANCE_SPOT_MY_TRADES_LIMIT,
) -> tuple[BinanceSpotTradeFetchWindow, ...]:
    normalized_symbols = _normalize_symbols(symbols)
    current_start = _parse_timestamp(start_time, field="start_time")
    final_end = _parse_timestamp(end_time, field="end_time")
    if current_start >= final_end:
        raise BinanceFetchPlanError("start_time must be before end_time")
    normalized_limit = _require_plan_positive_int(limit, field="limit")
    if normalized_limit > BINANCE_SPOT_MY_TRADES_LIMIT:
        raise BinanceFetchPlanError(f"limit must be <= {BINANCE_SPOT_MY_TRADES_LIMIT}")

    windows: list[BinanceSpotTradeFetchWindow] = []
    request_number = 1
    for symbol in normalized_symbols:
        window_start = current_start
        while window_start < final_end:
            window_end = min(window_start + BINANCE_SPOT_MY_TRADES_WINDOW, final_end)
            windows.append(
                BinanceSpotTradeFetchWindow(
                    request_number=request_number,
                    symbol=symbol,
                    start_time=_serialize_timestamp(window_start),
                    end_time=_serialize_timestamp(window_end),
                    start_time_ms=_timestamp_ms(window_start),
                    end_time_ms=_timestamp_ms(window_end),
                    limit=normalized_limit,
                )
            )
            request_number += 1
            window_start = window_end
    return tuple(windows)


def serialize_binance_spot_fetch_plan(
    windows: tuple[BinanceSpotTradeFetchWindow, ...],
) -> str:
    if not windows:
        raise BinanceFetchPlanError("fetch plan must contain at least one window")
    payload = {
        "exchange": "binance",
        "market": BINANCE_SPOT_MARKET,
        "symbols": tuple(dict.fromkeys(window.symbol for window in windows)),
        "start_time": windows[0].start_time,
        "end_time": windows[-1].end_time,
        "source_endpoint_labels": (BINANCE_SPOT_MY_TRADES_ENDPOINT,),
        "windows": tuple(window.to_source_metadata() for window in windows),
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def normalize_binance_spot_trades(
    records: Sequence[Mapping[str, Any]],
) -> BinanceNormalizationResult:
    ordered_records = tuple(sorted(records, key=_binance_trade_sort_key))
    canonical_records = tuple(
        _canonicalize_binance_record(record) for record in ordered_records
    )
    trades = normalize_exchange_records(
        exchange="binance",
        market=BINANCE_SPOT_MARKET,
        records=canonical_records,
    )
    traced_trades = tuple(
        replace(trade, row_id=_binance_trade_trace_row_id(record))
        for trade, record in zip(trades, ordered_records, strict=True)
    )
    metadata = tuple(
        _binance_trade_metadata(record=record, trade=trade, source_row_number=index)
        for index, (record, trade) in enumerate(
            zip(ordered_records, traced_trades, strict=True),
            start=1,
        )
    )
    warnings = tuple(
        warning
        for source_row_number, record in enumerate(ordered_records, start=1)
        for warning in _unsupported_field_warnings(record, source_row_number)
    )
    return BinanceNormalizationResult(
        trades=traced_trades,
        metadata=metadata,
        warnings=warnings,
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


def _canonicalize_binance_record(record: Mapping[str, Any]) -> dict[str, object]:
    canonical = dict(record)
    field_values = {
        "commission_asset": _first_present(
            record, ("commission_asset", "commissionAsset")
        ),
        "is_buyer": _first_present(record, ("is_buyer", "isBuyer")),
        "is_maker": _first_present(record, ("is_maker", "isMaker")),
        "order_id": _first_present(record, ("order_id", "orderId")),
        "quantity": _first_present(record, ("quantity", "qty")),
        "time": _normalize_binance_time(_first_present(record, ("time",))),
        "trade_id": _first_present(record, ("trade_id", "id")),
    }
    for field, value in field_values.items():
        if value is not None:
            canonical[field] = value
    return canonical


def _binance_trade_sort_key(record: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(_normalize_binance_time(_first_present(record, ("time",))) or ""),
        str(_first_present(record, ("order_id", "orderId")) or ""),
        str(_first_present(record, ("trade_id", "id")) or ""),
        str(record.get("symbol", "")),
    )


def _normalize_binance_time(value: object | None) -> object | None:
    if value in (None, ""):
        return None
    text = str(value).strip()
    if text.isdigit():
        timestamp = datetime.fromtimestamp(int(text) / 1000, tz=UTC)
        return _serialize_timestamp(timestamp)
    return value


def _unsupported_field_warnings(
    record: Mapping[str, Any],
    source_row_number: int,
) -> tuple[BinanceNormalizationWarning, ...]:
    return tuple(
        BinanceNormalizationWarning(
            field=str(field),
            message="unsupported Binance spot trade field ignored",
            source_ref=f"record {source_row_number}",
        )
        for field in sorted(record)
        if str(field) not in BINANCE_SUPPORTED_TRADE_FIELDS
    )


def _binance_trade_metadata(
    *,
    record: Mapping[str, Any],
    trade: TradeRecord,
    source_row_number: int,
) -> BinanceTradeMetadata:
    is_maker = bool(_first_present(record, ("is_maker", "isMaker")))
    return BinanceTradeMetadata(
        row_id=trade.row_id,
        fee_asset=str(
            _first_present(record, ("commission_asset", "commissionAsset")) or ""
        ),
        liquidity="maker" if is_maker else "taker",
        source_ref=f"record {source_row_number}",
    )


def _binance_trade_trace_row_id(record: Mapping[str, Any]) -> str:
    symbol = _trace_component(record.get("symbol"), field="symbol")
    order_id = _trace_component(
        _first_present(record, ("order_id", "orderId")),
        field="order_id",
    )
    trade_id = _trace_component(
        _first_present(record, ("trade_id", "id")),
        field="trade_id",
    )
    timestamp = _trace_component(
        _normalize_binance_time(_first_present(record, ("time",))),
        field="time",
    )
    return f"binance_spot_{symbol}_{order_id}_{trade_id}_{timestamp}"


def _trace_component(value: object | None, *, field: str) -> str:
    if value in (None, ""):
        raise BinanceNormalizationError(f"{field} is required for Binance trace id")
    safe_value = re.sub(r"[^A-Za-z0-9_.:-]+", "_", str(value).strip()).strip("._:-")
    if not safe_value:
        raise BinanceNormalizationError(f"{field} must contain traceable characters")
    return safe_value


def _first_present(record: Mapping[str, Any], fields: Iterable[str]) -> object | None:
    for field in fields:
        value = record.get(field)
        if value not in (None, ""):
            return value
    return None


def _normalize_symbols(symbols: tuple[str, ...]) -> tuple[str, ...]:
    normalized = sorted({_normalize_symbol_for_plan(symbol) for symbol in symbols})
    if not normalized:
        raise BinanceFetchPlanError("symbols must not be empty")
    return tuple(normalized)


def _normalize_symbol_for_plan(value: str) -> str:
    text = str(value).strip()
    if not text:
        raise BinanceFetchPlanError("symbols must not contain blank values")
    return text.upper()


def _parse_timestamp(value: str, *, field: str) -> datetime:
    raw_value = _normalize_time_text(value, field=field)
    if raw_value.endswith("Z"):
        raw_value = f"{raw_value[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(raw_value)
    except ValueError as exc:
        raise BinanceFetchPlanError(f"{field} must be ISO-8601 datetime") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise BinanceFetchPlanError(f"{field} must include a timezone")
    return parsed.astimezone(UTC)


def _normalize_time_text(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise BinanceFetchPlanError(f"{field} must not be blank")
    return text


def _serialize_timestamp(value: datetime) -> str:
    timespec = "milliseconds" if value.microsecond else "seconds"
    return value.isoformat(timespec=timespec).replace("+00:00", "Z")


def _timestamp_ms(value: datetime) -> int:
    delta = value - _UNIX_EPOCH
    return (
        (delta.days * 24 * 60 * 60 * 1000)
        + (delta.seconds * 1000)
        + (delta.microseconds // 1000)
    )


def _require_plan_positive_int(value: Any, *, field: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise BinanceFetchPlanError(f"{field} must be an integer") from exc
    if parsed < 1:
        raise BinanceFetchPlanError(f"{field} must be positive")
    return parsed


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
