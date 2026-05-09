from __future__ import annotations

from trader_risk_audit.exchange.bybit import (
    BYBIT_ALLOWED_ENDPOINT_LABELS,
    BYBIT_EXECUTION_HISTORY_ENDPOINT,
    BYBIT_KEY_INFO_ENDPOINT,
    collect_bybit_cursor_pages,
    plan_bybit_execution_fetches,
)


def test_bybit_fetch_plan_slices_seven_day_windows() -> None:
    windows = plan_bybit_execution_fetches(
        category="linear",
        symbol="BTCUSDT",
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-17T00:00:00Z",
    )

    assert [(window.start_time, window.end_time) for window in windows] == [
        ("2026-04-01T00:00:00Z", "2026-04-08T00:00:00Z"),
        ("2026-04-08T00:00:00Z", "2026-04-15T00:00:00Z"),
        ("2026-04-15T00:00:00Z", "2026-04-17T00:00:00Z"),
    ]
    assert {window.category for window in windows} == {"linear"}
    assert {window.symbol for window in windows} == {"BTCUSDT"}
    assert {window.endpoint_label for window in windows} == {
        BYBIT_EXECUTION_HISTORY_ENDPOINT
    }


def test_bybit_cursor_pagination_is_deterministic() -> None:
    responses = {
        None: {
            "result": {
                "list": [{"execId": "exec_001"}],
                "nextPageCursor": "cursor_2",
            }
        },
        "cursor_2": {
            "result": {
                "list": [{"execId": "exec_002"}],
                "nextPageCursor": "cursor_3",
            }
        },
        "cursor_3": {
            "result": {
                "list": [{"execId": "exec_003"}],
                "nextPageCursor": "",
            }
        },
    }
    requested_cursors: list[str | None] = []

    def fetch_page(cursor: str | None):
        requested_cursors.append(cursor)
        return responses[cursor]

    pages = collect_bybit_cursor_pages(fetch_page)

    assert requested_cursors == [None, "cursor_2", "cursor_3"]
    assert [page.page_number for page in pages] == [1, 2, 3]
    assert [page.request_cursor for page in pages] == [None, "cursor_2", "cursor_3"]
    assert [page.records[0]["execId"] for page in pages] == [
        "exec_001",
        "exec_002",
        "exec_003",
    ]


def test_bybit_client_exposes_no_write_endpoints() -> None:
    assert BYBIT_ALLOWED_ENDPOINT_LABELS == (
        BYBIT_EXECUTION_HISTORY_ENDPOINT,
        BYBIT_KEY_INFO_ENDPOINT,
    )
    forbidden_fragments = (
        "amend",
        "cancel",
        "close",
        "leverage",
        "margin",
        "order.create",
        "order",
        "place",
        "transfer",
        "withdraw",
    )
    rendered = "\n".join(BYBIT_ALLOWED_ENDPOINT_LABELS)

    for fragment in forbidden_fragments:
        assert fragment not in rendered
