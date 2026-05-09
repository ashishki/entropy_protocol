from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass
from typing import Any

SENSITIVE_FIELD_FRAGMENTS = (
    "account_balance",
    "accountbalance",
    "account_id",
    "accountid",
    "apikey",
    "api_key",
    "api_secret",
    "balance",
    "customer",
    "private_note",
    "privatenote",
    "secret",
    "signature",
)


@dataclass(frozen=True)
class FetchedPage:
    endpoint_label: str
    page_number: int
    record_count: int
    cursor: str | None = None

    def __post_init__(self) -> None:
        _require_non_blank(self.endpoint_label, field="endpoint_label")
        if self.page_number < 1:
            raise ValueError("page_number must be >= 1")
        if self.record_count < 0:
            raise ValueError("record_count must be >= 0")
        if self.cursor is not None:
            _require_non_blank(self.cursor, field="cursor")


@dataclass(frozen=True)
class RawExchangeSnapshot:
    exchange: str
    market: str
    symbols: tuple[str, ...]
    start_time: str
    end_time: str
    fetched_pages: tuple[FetchedPage, ...]
    source_endpoint_labels: tuple[str, ...]
    raw_records: tuple[dict[str, Any], ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.exchange, field="exchange")
        _require_non_blank(self.market, field="market")
        _require_non_blank(self.start_time, field="start_time")
        _require_non_blank(self.end_time, field="end_time")
        if not self.symbols:
            raise ValueError("symbols must not be empty")
        for symbol in self.symbols:
            _require_non_blank(symbol, field="symbols")
        if not self.fetched_pages:
            raise ValueError("fetched_pages must not be empty")
        if not self.source_endpoint_labels:
            raise ValueError("source_endpoint_labels must not be empty")
        for label in self.source_endpoint_labels:
            _require_non_blank(label, field="source_endpoint_labels")
        _reject_sensitive_payload(self.to_dict())

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


def build_raw_exchange_snapshot(
    *,
    exchange: str,
    market: str,
    symbols: Sequence[str],
    start_time: str,
    end_time: str,
    fetched_pages: Sequence[FetchedPage],
    source_endpoint_labels: Sequence[str],
    raw_records: Sequence[Mapping[str, Any]],
) -> RawExchangeSnapshot:
    return RawExchangeSnapshot(
        exchange=exchange,
        market=market,
        symbols=tuple(symbols),
        start_time=start_time,
        end_time=end_time,
        fetched_pages=tuple(fetched_pages),
        source_endpoint_labels=tuple(source_endpoint_labels),
        raw_records=tuple(dict(record) for record in raw_records),
    )


def _reject_sensitive_payload(payload: object) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            normalized_key = _normalize_key(str(key))
            has_sensitive_name = any(
                fragment in normalized_key for fragment in SENSITIVE_FIELD_FRAGMENTS
            )
            if has_sensitive_name:
                raise ValueError(
                    f"Raw exchange snapshot contains forbidden field: {key}"
                )
            _reject_sensitive_payload(value)
        return
    if isinstance(payload, Sequence) and not isinstance(payload, str | bytes):
        for item in payload:
            _reject_sensitive_payload(item)


def _normalize_key(value: str) -> str:
    return "".join(
        character
        for character in value.casefold()
        if character.isalnum() or character == "_"
    )


def _require_non_blank(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must not be blank")
    return text
