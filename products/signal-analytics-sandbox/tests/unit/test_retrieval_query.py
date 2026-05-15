from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.retrieval import LocalRetrievalStore
from signal_sandbox.retrieval.query import (
    CitedRetrievalResult,
    RetrievalQueryFilters,
    query_retrieval_store,
)


def test_query_results_are_cited(tmp_path) -> None:
    store = LocalRetrievalStore(tmp_path)
    document = _source_document(
        "doc-1",
        text="BTC thesis remains constructive after ETF inflows",
        day=1,
    )
    store.ingest_documents([document])

    results = query_retrieval_store(store, "BTC ETF")

    assert len(results) == 1
    assert results[0].document_id == "doc-1"
    assert "BTC" in results[0].snippet
    assert results[0].score == Decimal("1.000000")
    assert results[0].source_timestamp_utc == document.timestamp_utc
    assert results[0].evidence_url == document.evidence_url
    assert results[0].text_sha256 == document.text_sha256


def test_channel_and_time_filters(tmp_path) -> None:
    store = LocalRetrievalStore(tmp_path)
    first = _source_document("doc-1", text="BTC regime update", day=1)
    second = _source_document(
        "doc-2",
        text="BTC later update",
        day=3,
        metadata={"channel_id": "other", "asset": "BTC"},
    )
    store.ingest_documents([first, second])

    results = query_retrieval_store(
        store,
        "BTC update",
        filters=RetrievalQueryFilters(
            channel_id="example",
            start_utc=datetime(2026, 5, 1, tzinfo=UTC),
            end_utc=datetime(2026, 5, 2, tzinfo=UTC),
        ),
    )

    assert [result.document_id for result in results] == ["doc-1"]


def test_uncited_results_rejected() -> None:
    with pytest.raises(ValidationError):
        CitedRetrievalResult(
            document_id="",
            snippet="BTC",
            score=Decimal("1"),
            source_timestamp_utc=datetime(2026, 5, 9, tzinfo=UTC),
            evidence_url="",
            text_sha256="not-a-sha",
        )


def _source_document(
    document_id: str,
    *,
    text: str,
    day: int,
    metadata: dict[str, str] | None = None,
) -> SourceDocument:
    return SourceDocument(
        document_id=document_id,
        capture_id=f"capture-{document_id}",
        source_id="example",
        author="example",
        timestamp_utc=datetime(2026, 5, day, tzinfo=UTC),
        text=text,
        evidence_url=f"https://t.me/example/{day}",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
        metadata=metadata or {"channel_id": "example", "asset": "BTC"},
    )
