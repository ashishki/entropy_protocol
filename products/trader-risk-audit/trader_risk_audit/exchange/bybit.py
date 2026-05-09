from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from typing import Any

from trader_risk_audit.exchange.credentials import (
    APPROVED_READ_ONLY,
    ExchangeCredentials,
    PermissionReview,
    build_exchange_import_safe_metadata,
    inspect_bybit_api_key_metadata,
)
from trader_risk_audit.exchange.normalizer import normalize_exchange_records
from trader_risk_audit.trades.schema import TradeRecord

BYBIT_EXECUTION_HISTORY_ENDPOINT = "bybit.v5.execution.list"
BYBIT_KEY_INFO_ENDPOINT = "bybit.v5.user.query_api"
BYBIT_ALLOWED_ENDPOINT_LABELS = (
    BYBIT_EXECUTION_HISTORY_ENDPOINT,
    BYBIT_KEY_INFO_ENDPOINT,
)
BYBIT_SUPPORTED_EXECUTION_CATEGORIES = ("linear", "spot")
BYBIT_EXECUTION_WINDOW = timedelta(days=7)
BYBIT_SUPPORTED_EXECUTION_FIELDS = frozenset(
    {
        "category",
        "exec_fee",
        "exec_id",
        "exec_price",
        "exec_qty",
        "exec_time",
        "fee_currency",
        "is_maker",
        "order_id",
        "side",
        "source_row_id",
        "symbol",
    }
)


@dataclass(frozen=True)
class BybitPermissionCheck:
    permission_review: PermissionReview
    safe_metadata: dict[str, object]

    @property
    def approved(self) -> bool:
        return self.permission_review.status == APPROVED_READ_ONLY


class BybitPermissionError(PermissionError):
    def __init__(self, permission_review: PermissionReview) -> None:
        self.permission_review = permission_review
        super().__init__(
            f"bybit permission check failed: {permission_review.status}; "
            f"reason={permission_review.reason}"
        )


@dataclass(frozen=True)
class BybitExecutionFetchWindow:
    category: str
    symbol: str
    start_time: str
    end_time: str
    endpoint_label: str = BYBIT_EXECUTION_HISTORY_ENDPOINT


@dataclass(frozen=True)
class BybitExecutionPage:
    page_number: int
    request_cursor: str | None
    next_cursor: str | None
    records: tuple[Mapping[str, Any], ...]
    endpoint_label: str = BYBIT_EXECUTION_HISTORY_ENDPOINT


class BybitFetchPlanError(ValueError):
    pass


@dataclass(frozen=True)
class BybitNormalizationWarning:
    field: str
    message: str
    source_ref: str


@dataclass(frozen=True)
class BybitNormalizationResult:
    trades: tuple[TradeRecord, ...]
    warnings: tuple[BybitNormalizationWarning, ...]


def check_bybit_api_key_permissions(
    metadata_response: Mapping[str, Any],
    *,
    credentials: ExchangeCredentials | None = None,
) -> BybitPermissionCheck:
    review = inspect_bybit_api_key_metadata(metadata_response)
    safe_metadata: dict[str, object] = {"permission_review": review.to_safe_metadata()}
    if credentials is not None:
        safe_metadata = build_exchange_import_safe_metadata(
            credentials=credentials,
            permission_review=review,
        )
    return BybitPermissionCheck(
        permission_review=review,
        safe_metadata=safe_metadata,
    )


def require_bybit_read_only_permissions(
    metadata_response: Mapping[str, Any],
    *,
    credentials: ExchangeCredentials | None = None,
) -> BybitPermissionCheck:
    check = check_bybit_api_key_permissions(
        metadata_response,
        credentials=credentials,
    )
    if not check.approved:
        raise BybitPermissionError(check.permission_review)
    return check


def plan_bybit_execution_fetches(
    *,
    category: str,
    symbol: str,
    start_time: str,
    end_time: str,
) -> tuple[BybitExecutionFetchWindow, ...]:
    normalized_category = _normalize_category(category)
    normalized_symbol = _require_non_blank(symbol, field="symbol")
    current_start = _parse_timestamp(start_time, field="start_time")
    final_end = _parse_timestamp(end_time, field="end_time")
    if current_start >= final_end:
        raise BybitFetchPlanError("start_time must be before end_time")

    windows: list[BybitExecutionFetchWindow] = []
    while current_start < final_end:
        current_end = min(current_start + BYBIT_EXECUTION_WINDOW, final_end)
        windows.append(
            BybitExecutionFetchWindow(
                category=normalized_category,
                symbol=normalized_symbol,
                start_time=_serialize_timestamp(current_start),
                end_time=_serialize_timestamp(current_end),
            )
        )
        current_start = current_end
    return tuple(windows)


def collect_bybit_cursor_pages(
    fetch_page: Callable[[str | None], Mapping[str, Any]],
    *,
    initial_cursor: str | None = None,
    max_pages: int = 100,
) -> tuple[BybitExecutionPage, ...]:
    if max_pages < 1:
        raise BybitFetchPlanError("max_pages must be >= 1")

    pages: list[BybitExecutionPage] = []
    seen_cursors: set[str | None] = set()
    cursor = initial_cursor
    for page_number in range(1, max_pages + 1):
        if cursor in seen_cursors:
            raise BybitFetchPlanError("cursor pagination loop detected")
        seen_cursors.add(cursor)

        payload = fetch_page(cursor)
        result = payload.get("result", payload)
        if not isinstance(result, Mapping):
            raise BybitFetchPlanError(
                "Bybit page response must contain a result mapping"
            )
        raw_records = result.get("list", ())
        if not isinstance(raw_records, Sequence) or isinstance(
            raw_records, str | bytes
        ):
            raise BybitFetchPlanError("Bybit page result list must be a sequence")
        records = tuple(record for record in raw_records if isinstance(record, Mapping))
        next_cursor = _normalize_cursor(result.get("nextPageCursor"))
        pages.append(
            BybitExecutionPage(
                page_number=page_number,
                request_cursor=cursor,
                next_cursor=next_cursor,
                records=records,
            )
        )
        if next_cursor is None:
            return tuple(pages)
        cursor = next_cursor

    raise BybitFetchPlanError("cursor pagination exceeded max_pages")


def normalize_bybit_executions(
    records: Sequence[Mapping[str, Any]],
    *,
    category: str,
) -> BybitNormalizationResult:
    normalized_category = _normalize_category(category)
    ordered_records = tuple(sorted(records, key=_bybit_execution_sort_key))
    warnings = tuple(
        warning
        for source_row_number, record in enumerate(ordered_records, start=1)
        for warning in _unsupported_field_warnings(record, source_row_number)
    )
    trades = normalize_exchange_records(
        exchange="bybit",
        market=normalized_category,
        records=ordered_records,
    )
    traced_trades = tuple(
        replace(trade, row_id=_bybit_execution_trace_row_id(record))
        for trade, record in zip(trades, ordered_records, strict=True)
    )
    return BybitNormalizationResult(trades=traced_trades, warnings=warnings)


def _normalize_category(category: str) -> str:
    normalized = _require_non_blank(category, field="category").casefold()
    if normalized not in BYBIT_SUPPORTED_EXECUTION_CATEGORIES:
        allowed = ", ".join(BYBIT_SUPPORTED_EXECUTION_CATEGORIES)
        raise BybitFetchPlanError(
            f"unsupported Bybit category: {normalized}; allowed: {allowed}"
        )
    return normalized


def _parse_timestamp(value: str, *, field: str) -> datetime:
    raw_value = _require_non_blank(value, field=field)
    if raw_value.endswith("Z"):
        raw_value = f"{raw_value[:-1]}+00:00"
    try:
        return datetime.fromisoformat(raw_value)
    except ValueError as exc:
        raise BybitFetchPlanError(f"{field} must be ISO-8601 datetime") from exc


def _serialize_timestamp(value: datetime) -> str:
    return value.isoformat().replace("+00:00", "Z")


def _normalize_cursor(value: object) -> str | None:
    if value in (None, ""):
        return None
    return str(value)


def _require_non_blank(value: str, *, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise BybitFetchPlanError(f"{field} must not be blank")
    return text


def _bybit_execution_sort_key(record: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(record.get("exec_time", record.get("timestamp", ""))),
        str(record.get("exec_id", "")),
        str(record.get("order_id", "")),
        str(record.get("symbol", "")),
    )


def _unsupported_field_warnings(
    record: Mapping[str, Any],
    source_row_number: int,
) -> tuple[BybitNormalizationWarning, ...]:
    return tuple(
        BybitNormalizationWarning(
            field=str(field),
            message="unsupported Bybit execution field ignored",
            source_ref=f"record {source_row_number}",
        )
        for field in sorted(record)
        if str(field) not in BYBIT_SUPPORTED_EXECUTION_FIELDS
    )


def _bybit_execution_trace_row_id(record: Mapping[str, Any]) -> str:
    source_id = _require_non_blank(
        str(
            record.get("exec_id")
            or record.get("source_row_id")
            or record.get("order_id")
            or ""
        ),
        field="exec_id",
    )
    safe_source_id = re.sub(r"[^A-Za-z0-9_.:-]+", "_", source_id).strip("._:-")
    if not safe_source_id:
        raise BybitFetchPlanError("exec_id must contain traceable characters")
    return f"bybit_exec_{safe_source_id}"
