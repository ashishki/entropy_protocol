from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

from trader_risk_audit.trades.schema import TradeRecord, TradeValidationError

_FIELD_ALIASES: Mapping[str, tuple[str, ...]] = {
    "timestamp": ("timestamp", "time", "exec_time", "executed_at"),
    "symbol": ("symbol",),
    "side": ("side", "is_buyer"),
    "quantity": ("quantity", "qty", "exec_qty"),
    "price": ("price", "exec_price"),
    "fees": ("fees", "fee", "commission", "exec_fee"),
}
_REQUIRED_FIELDS = ("timestamp", "symbol", "side", "quantity", "price")
_EXECUTION_ID_FIELDS = ("exec_id", "execution_id", "trade_id", "id")
_ORDER_ID_FIELDS = ("order_id", "orderId")


@dataclass(frozen=True)
class ExchangeNormalizationIssue:
    field: str
    message: str
    source_ref: str


class ExchangeNormalizationError(ValueError):
    def __init__(self, issues: Iterable[ExchangeNormalizationIssue]) -> None:
        self.issues = tuple(issues)
        detail = "; ".join(
            f"{issue.source_ref} {issue.field}: {issue.message}"
            for issue in self.issues
        )
        super().__init__(detail)

    @property
    def fields(self) -> tuple[str, ...]:
        return tuple(issue.field for issue in self.issues)


def normalize_exchange_records(
    *,
    exchange: str,
    market: str,
    records: Sequence[Mapping[str, Any]],
) -> tuple[TradeRecord, ...]:
    normalized_records = [
        _normalize_exchange_record(
            exchange=exchange,
            market=market,
            record=record,
            source_row_number=source_row_number,
        )
        for source_row_number, record in enumerate(records, start=1)
    ]
    return tuple(
        sorted(
            normalized_records,
            key=lambda item: (item.timestamp, item.source_row_number, item.row_id),
        )
    )


def _normalize_exchange_record(
    *,
    exchange: str,
    market: str,
    record: Mapping[str, Any],
    source_row_number: int,
) -> TradeRecord:
    source_ref = f"record {source_row_number}"
    canonical = _canonical_trade_mapping(
        exchange=exchange,
        market=market,
        record=record,
        source_row_number=source_row_number,
    )
    missing_issues = _missing_required_issues(canonical, source_ref=source_ref)
    if missing_issues:
        raise ExchangeNormalizationError(missing_issues)

    try:
        trade = TradeRecord.from_mapping(canonical)
    except TradeValidationError as exc:
        raise ExchangeNormalizationError(
            ExchangeNormalizationIssue(
                field=error.field,
                message=error.message,
                source_ref=source_ref,
            )
            for error in exc.errors
        ) from exc

    row_id = _build_exchange_row_id(
        exchange=exchange,
        symbol=str(canonical["symbol"]),
        timestamp=str(canonical["timestamp"]),
        execution_id=_first_present(record, _EXECUTION_ID_FIELDS),
        order_id=_first_present(record, _ORDER_ID_FIELDS),
    )
    return replace(trade, row_id=row_id)


def _canonical_trade_mapping(
    *,
    exchange: str,
    market: str,
    record: Mapping[str, Any],
    source_row_number: int,
) -> dict[str, object]:
    canonical: dict[str, object] = {
        "account_id": f"{exchange}_read_only_import",
        "fees": "0",
        "source_file": f"exchange:{exchange}:{market}",
        "source_row_number": source_row_number,
    }
    for canonical_field, aliases in _FIELD_ALIASES.items():
        value = _first_present(record, aliases)
        if value is not None:
            canonical[canonical_field] = _normalize_field_value(canonical_field, value)
    return canonical


def _missing_required_issues(
    canonical: Mapping[str, object],
    *,
    source_ref: str,
) -> tuple[ExchangeNormalizationIssue, ...]:
    return tuple(
        ExchangeNormalizationIssue(
            field=field,
            message="required field is missing",
            source_ref=source_ref,
        )
        for field in _REQUIRED_FIELDS
        if canonical.get(field) in (None, "")
    )


def _normalize_field_value(field: str, value: object) -> object:
    if field == "side" and isinstance(value, bool):
        return "buy" if value else "sell"
    return value


def _first_present(record: Mapping[str, Any], fields: Iterable[str]) -> object | None:
    for field in fields:
        value = record.get(field)
        if value not in (None, ""):
            return value
    return None


def _build_exchange_row_id(
    *,
    exchange: str,
    symbol: str,
    timestamp: str,
    execution_id: object | None,
    order_id: object | None,
) -> str:
    parts = (
        exchange.casefold(),
        symbol.casefold(),
        str(execution_id or ""),
        str(order_id or ""),
        timestamp,
    )
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"exchange_{digest}"
