from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from signal_sandbox.corpus import SourceDocument
from signal_sandbox.retrieval import (
    LocalRetrievalStore,
    deterministic_test_embedding_metadata,
)


def test_ingest_preserves_document_ids(tmp_path) -> None:
    store = LocalRetrievalStore(tmp_path)
    documents = [_source_document("doc-1"), _source_document("doc-2")]

    result = store.ingest_documents(documents)

    assert [item.document_id for item in result.indexed_documents] == [
        "doc-1",
        "doc-2",
    ]
    assert result.document_count == 2
    assert result.indexed_documents[0].evidence_url == "https://t.me/example/1"
    assert result.indexed_documents[0].text_sha256 == documents[0].text_sha256
    assert result.indexed_documents[0].index_schema_version == "retrieval-index-v1"


def test_ingest_is_idempotent(tmp_path) -> None:
    store = LocalRetrievalStore(tmp_path)
    document = _source_document("doc-1")

    first = store.ingest_documents([document])
    second = store.ingest_documents([document])

    assert second.document_count == 1
    assert second.indexed_documents == first.indexed_documents
    assert len(store.list_documents()) == 1


def test_embedding_metadata_recorded(tmp_path) -> None:
    store = LocalRetrievalStore(tmp_path)
    metadata = deterministic_test_embedding_metadata()

    result = store.ingest_documents(
        [_source_document("doc-1")],
        embedding_metadata=metadata,
    )
    indexed = result.indexed_documents[0]

    assert indexed.embedding_metadata == metadata
    assert indexed.embedding_metadata.fixture_id == "deterministic-test-embedding-v1"
    assert indexed.vector_path.startswith("vectors/")
    assert len(indexed.index_build_checksum) == 64


def _source_document(document_id: str) -> SourceDocument:
    text = f"{document_id} says BTC context"
    return SourceDocument(
        document_id=document_id,
        capture_id=f"capture-{document_id}",
        source_id="example",
        author="example",
        timestamp_utc=datetime(2026, 5, 9, tzinfo=UTC),
        text=text,
        evidence_url="https://t.me/example/1",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )
