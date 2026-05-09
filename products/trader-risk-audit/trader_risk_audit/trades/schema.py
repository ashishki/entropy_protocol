from __future__ import annotations

import hashlib
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

TradeSide = Literal["buy", "sell"]

DEFAULT_SIDE_ALIASES: Mapping[TradeSide, frozenset[str]] = {
    "buy": frozenset({"buy", "b", "long"}),
    "sell": frozenset({"sell", "s", "short"}),
}

_REQUIRED_FIELDS = ("timestamp", "symbol", "side", "quantity", "price")


@dataclass(frozen=True)
class FieldValidationError:
    field: str
    message: str


class TradeValidationError(ValueError):
    def __init__(self, errors: Iterable[FieldValidationError]) -> None:
        self.errors = tuple(errors)
        detail = ", ".join(f"{error.field}: {error.message}" for error in self.errors)
        super().__init__(detail)

    @property
    def fields(self) -> tuple[str, ...]:
        return tuple(error.field for error in self.errors)


@dataclass(frozen=True)
class TradeRecord:
    timestamp: datetime
    symbol: str
    side: TradeSide
    quantity: Decimal
    price: Decimal
    fees: Decimal
    account_id: str
    source_file: str
    source_row_number: int
    row_id: str

    @classmethod
    def from_mapping(
        cls,
        values: Mapping[str, Any],
        *,
        side_aliases: Mapping[TradeSide, Iterable[str]] = DEFAULT_SIDE_ALIASES,
    ) -> TradeRecord:
        errors = _missing_required_field_errors(values)
        if errors:
            raise TradeValidationError(errors)

        parsed_errors: list[FieldValidationError] = []
        timestamp = _parse_timestamp(values["timestamp"], parsed_errors)
        side = _parse_side(values["side"], side_aliases, parsed_errors)
        quantity = _parse_decimal(values["quantity"], "quantity", parsed_errors)
        price = _parse_decimal(values["price"], "price", parsed_errors)
        fees = _parse_decimal(values.get("fees", "0"), "fees", parsed_errors)
        source_row_number = _parse_source_row_number(
            values.get("source_row_number", 0),
            parsed_errors,
        )
        symbol = _parse_text(values["symbol"], "symbol", parsed_errors)
        account_id = _parse_text(
            values.get("account_id", ""), "account_id", parsed_errors
        )
        source_file = _parse_text(
            values.get("source_file", ""),
            "source_file",
            parsed_errors,
        )
        row_id = _parse_row_id_override(values.get("row_id"), parsed_errors)

        if parsed_errors:
            raise TradeValidationError(parsed_errors)

        if row_id is None:
            row_id = _build_row_id(
                timestamp=timestamp,
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                source_file=source_file,
                source_row_number=source_row_number,
            )
        return cls(
            timestamp=timestamp,
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            fees=fees,
            account_id=account_id,
            source_file=source_file,
            source_row_number=source_row_number,
            row_id=row_id,
        )


def normalize_side(
    value: object,
    *,
    side_aliases: Mapping[TradeSide, Iterable[str]] = DEFAULT_SIDE_ALIASES,
) -> TradeSide:
    normalized = str(value).strip().casefold()
    alias_map = {
        alias.strip().casefold(): canonical_side
        for canonical_side, aliases in side_aliases.items()
        for alias in aliases
    }
    try:
        return alias_map[normalized]
    except KeyError as exc:
        raise TradeValidationError(
            [FieldValidationError("side", f"unsupported side value {value!r}")]
        ) from exc


def _missing_required_field_errors(
    values: Mapping[str, Any],
) -> tuple[FieldValidationError, ...]:
    return tuple(
        FieldValidationError(field, "required field is missing")
        for field in _REQUIRED_FIELDS
        if values.get(field) in (None, "")
    )


def _parse_timestamp(value: object, errors: list[FieldValidationError]) -> datetime:
    if isinstance(value, datetime):
        timestamp = value
    else:
        raw_timestamp = str(value).strip()
        if raw_timestamp.endswith("Z"):
            raw_timestamp = f"{raw_timestamp[:-1]}+00:00"
        try:
            timestamp = datetime.fromisoformat(raw_timestamp)
        except ValueError:
            errors.append(
                FieldValidationError("timestamp", "must be ISO-8601 datetime")
            )
            return datetime.min

    if timestamp.tzinfo is None:
        errors.append(FieldValidationError("timestamp", "must include timezone"))
    return timestamp


def _parse_side(
    value: object,
    side_aliases: Mapping[TradeSide, Iterable[str]],
    errors: list[FieldValidationError],
) -> TradeSide:
    try:
        return normalize_side(value, side_aliases=side_aliases)
    except TradeValidationError as exc:
        errors.extend(exc.errors)
        return "buy"


def _parse_decimal(
    value: object,
    field: str,
    errors: list[FieldValidationError],
) -> Decimal:
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        errors.append(FieldValidationError(field, "must be a decimal value"))
        return Decimal("0")


def _parse_source_row_number(
    value: object,
    errors: list[FieldValidationError],
) -> int:
    try:
        row_number = int(value)
    except (TypeError, ValueError):
        errors.append(FieldValidationError("source_row_number", "must be an integer"))
        return 0
    if row_number < 0:
        errors.append(FieldValidationError("source_row_number", "must be non-negative"))
    return row_number


def _parse_text(
    value: object,
    field: str,
    errors: list[FieldValidationError],
) -> str:
    text = str(value).strip()
    if not text:
        errors.append(FieldValidationError(field, "must not be blank"))
    return text


def _parse_row_id_override(
    value: object,
    errors: list[FieldValidationError],
) -> str | None:
    if value in (None, ""):
        return None
    row_id = str(value).strip()
    if not row_id:
        errors.append(FieldValidationError("row_id", "must not be blank"))
        return None
    return row_id


def _build_row_id(
    *,
    timestamp: datetime,
    symbol: str,
    side: TradeSide,
    quantity: Decimal,
    price: Decimal,
    source_file: str,
    source_row_number: int,
) -> str:
    parts = (
        timestamp.isoformat(),
        symbol.casefold(),
        side,
        str(quantity.normalize()),
        str(price.normalize()),
        source_file,
        str(source_row_number),
    )
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"trade_{digest}"
