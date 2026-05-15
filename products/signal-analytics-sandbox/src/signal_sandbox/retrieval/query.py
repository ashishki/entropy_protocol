"""Cited retrieval query API."""

from __future__ import annotations

import json
import re
from datetime import datetime
from decimal import Decimal

import duckdb
from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.retrieval.store import LocalRetrievalStore


class RetrievalQueryFilters(BaseModel):
    model_config = ConfigDict(strict=True)

    channel_id: str | None = None
    author: str | None = None
    asset: str | None = None
    idea_type: str | None = None
    start_utc: datetime | None = None
    end_utc: datetime | None = None

    @field_validator("start_utc", "end_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime | None:
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp filter must be a datetime or ISO-8601 string")


class CitedRetrievalResult(BaseModel):
    model_config = ConfigDict(strict=True)

    document_id: str = Field(min_length=1)
    snippet: str = Field(min_length=1)
    score: Decimal = Field(ge=Decimal("0"))
    source_timestamp_utc: datetime
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)

    @field_validator("source_timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("source_timestamp_utc must be a datetime or ISO-8601 string")


def query_retrieval_store(
    store: LocalRetrievalStore,
    query: str,
    *,
    filters: RetrievalQueryFilters | None = None,
    limit: int = 10,
) -> list[CitedRetrievalResult]:
    active_filters = filters or RetrievalQueryFilters()
    query_terms = _terms(query)
    rows = _load_rows(store)
    results: list[CitedRetrievalResult] = []
    for row in rows:
        metadata = json.loads(row["metadata_json"])
        timestamp = datetime.fromisoformat(row["timestamp_utc"].replace("Z", "+00:00"))
        if not _matches_filters(row, metadata, timestamp, active_filters):
            continue
        score = _score(row["text"], query_terms)
        if score == Decimal("0"):
            continue
        results.append(
            CitedRetrievalResult(
                document_id=row["document_id"],
                snippet=_snippet(row["text"], query_terms),
                score=score,
                source_timestamp_utc=timestamp,
                evidence_url=row["evidence_url"],
                text_sha256=row["text_sha256"],
            )
        )
    return sorted(
        results,
        key=lambda item: (-item.score, item.source_timestamp_utc, item.document_id),
    )[:limit]


def _load_rows(store: LocalRetrievalStore) -> list[dict[str, str]]:
    with duckdb.connect(str(store.db_path)) as connection:
        rows = connection.execute(
            """
            select document_id, source_id, author, timestamp_utc, text,
                   evidence_url, text_sha256, metadata_json
            from documents
            order by document_id
            """
        ).fetchall()
    keys = [
        "document_id",
        "source_id",
        "author",
        "timestamp_utc",
        "text",
        "evidence_url",
        "text_sha256",
        "metadata_json",
    ]
    return [dict(zip(keys, row, strict=True)) for row in rows]


def _matches_filters(
    row: dict[str, str],
    metadata: dict[str, str],
    timestamp: datetime,
    filters: RetrievalQueryFilters,
) -> bool:
    channel_id = metadata.get("channel_id", row["source_id"])
    if filters.channel_id is not None and channel_id != filters.channel_id:
        return False
    if filters.author is not None and row["author"] != filters.author:
        return False
    if filters.asset is not None and metadata.get("asset") != filters.asset:
        return False
    if filters.idea_type is not None and metadata.get("idea_type") != filters.idea_type:
        return False
    if filters.start_utc is not None and timestamp < filters.start_utc:
        return False
    if filters.end_utc is not None and timestamp > filters.end_utc:
        return False
    return True


def _score(text: str, query_terms: set[str]) -> Decimal:
    if not query_terms:
        return Decimal("0")
    text_terms = _terms(text)
    hits = len(query_terms & text_terms)
    return (Decimal(hits) / Decimal(len(query_terms))).quantize(Decimal("0.000001"))


def _snippet(text: str, query_terms: set[str], *, max_length: int = 160) -> str:
    lowered = text.lower()
    positions = [lowered.find(term) for term in query_terms if lowered.find(term) >= 0]
    start = max(min(positions) - 40, 0) if positions else 0
    snippet = text[start : start + max_length].strip()
    return snippet or text[:max_length].strip()


def _terms(value: str) -> set[str]:
    return {term.lower() for term in re.findall(r"[A-Za-z0-9_#$]+", value)}
