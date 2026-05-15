"""Local DuckDB-backed retrieval ingestion store."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

import duckdb
from pydantic import BaseModel, ConfigDict, Field, field_validator

from signal_sandbox.corpus import SourceDocument

INDEX_SCHEMA_VERSION = "retrieval-index-v1"
VECTOR_DIMENSIONS = 8


class RetrievalStoreError(Exception):
    """Base exception for retrieval store failures."""


class RetrievalDocumentConflict(RetrievalStoreError):
    """Raised when a document ID is reused for different source content."""


class EmbeddingMetadata(BaseModel):
    model_config = ConfigDict(strict=True)

    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    version: str = Field(min_length=1)
    fixture_id: str | None = None
    dimensions: int = Field(gt=0)


class IndexedSourceDocument(BaseModel):
    model_config = ConfigDict(strict=True)

    document_id: str = Field(min_length=1)
    capture_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    author: str = Field(min_length=1)
    timestamp_utc: datetime
    evidence_url: str = Field(min_length=1)
    text_sha256: str = Field(min_length=64, max_length=64)
    embedding_metadata: EmbeddingMetadata
    index_schema_version: str = Field(min_length=1)
    index_build_checksum: str = Field(min_length=64, max_length=64)
    vector_path: str = Field(min_length=1)

    @field_validator("timestamp_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        if isinstance(value, datetime):
            return value
        if isinstance(value, str):
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        raise ValueError("timestamp_utc must be a datetime or ISO-8601 string")


class RetrievalIngestResult(BaseModel):
    model_config = ConfigDict(strict=True)

    indexed_documents: list[IndexedSourceDocument]
    index_schema_version: str
    document_count: int


class LocalRetrievalStore:
    """Store cited SourceDocument metadata in DuckDB plus vector sidecar files."""

    def __init__(self, workspace: Path):
        self.root = workspace / "retrieval"
        self.vector_dir = self.root / "vectors"
        self.db_path = self.root / "index.duckdb"
        self.root.mkdir(parents=True, exist_ok=True)
        self.vector_dir.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def ingest_documents(
        self,
        documents: list[SourceDocument],
        *,
        embedding_metadata: EmbeddingMetadata | None = None,
    ) -> RetrievalIngestResult:
        metadata = embedding_metadata or deterministic_test_embedding_metadata()
        indexed: list[IndexedSourceDocument] = []
        with duckdb.connect(str(self.db_path)) as connection:
            for document in sorted(documents, key=lambda item: item.document_id):
                existing_hash = connection.execute(
                    "select text_sha256 from documents where document_id = ?",
                    [document.document_id],
                ).fetchone()
                if (
                    existing_hash is not None
                    and existing_hash[0] != document.text_sha256
                ):
                    raise RetrievalDocumentConflict("document_id content hash changed")

                vector = deterministic_test_embedding(document)
                vector_path = self._write_vector_sidecar(document, metadata, vector)
                checksum = _index_build_checksum(document, metadata, vector_path)
                if existing_hash is None:
                    connection.execute(
                        """
                        insert into documents values (
                            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                        )
                        """,
                        [
                            document.document_id,
                            document.capture_id,
                            document.source_id,
                            document.author,
                            document.timestamp_utc.isoformat(),
                            document.text,
                            document.evidence_url,
                            document.text_sha256,
                            json.dumps(
                                document.metadata,
                                sort_keys=True,
                                separators=(",", ":"),
                            ),
                            metadata.provider,
                            metadata.model,
                            metadata.version,
                            metadata.fixture_id,
                            metadata.dimensions,
                            INDEX_SCHEMA_VERSION,
                            vector_path,
                            checksum,
                        ],
                    )
                indexed.append(self._load_one(connection, document.document_id))

            document_count_row = connection.execute(
                "select count(*) from documents"
            ).fetchone()
            document_count = document_count_row[0] if document_count_row else 0

        return RetrievalIngestResult(
            indexed_documents=indexed,
            index_schema_version=INDEX_SCHEMA_VERSION,
            document_count=int(document_count),
        )

    def list_documents(self) -> list[IndexedSourceDocument]:
        with duckdb.connect(str(self.db_path)) as connection:
            rows = connection.execute(
                "select document_id from documents order by document_id"
            ).fetchall()
            return [self._load_one(connection, row[0]) for row in rows]

    def _initialize(self) -> None:
        with duckdb.connect(str(self.db_path)) as connection:
            connection.execute(
                """
                create table if not exists documents (
                    document_id varchar primary key,
                    capture_id varchar not null,
                    source_id varchar not null,
                    author varchar not null,
                    timestamp_utc varchar not null,
                    text varchar not null,
                    evidence_url varchar not null,
                    text_sha256 varchar not null,
                    metadata_json varchar not null,
                    embedding_provider varchar not null,
                    embedding_model varchar not null,
                    embedding_version varchar not null,
                    embedding_fixture_id varchar,
                    embedding_dimensions integer not null,
                    index_schema_version varchar not null,
                    vector_path varchar not null,
                    index_build_checksum varchar not null
                )
                """
            )

    def _load_one(
        self,
        connection: duckdb.DuckDBPyConnection,
        document_id: str,
    ) -> IndexedSourceDocument:
        row = connection.execute(
            """
            select document_id, capture_id, source_id, author, timestamp_utc,
                   evidence_url, text_sha256, embedding_provider,
                   embedding_model, embedding_version, embedding_fixture_id,
                   embedding_dimensions, index_schema_version, vector_path,
                   index_build_checksum
            from documents
            where document_id = ?
            """,
            [document_id],
        ).fetchone()
        if row is None:
            raise KeyError(document_id)
        return IndexedSourceDocument(
            document_id=row[0],
            capture_id=row[1],
            source_id=row[2],
            author=row[3],
            timestamp_utc=row[4],
            evidence_url=row[5],
            text_sha256=row[6],
            embedding_metadata=EmbeddingMetadata(
                provider=row[7],
                model=row[8],
                version=row[9],
                fixture_id=row[10],
                dimensions=row[11],
            ),
            index_schema_version=row[12],
            vector_path=row[13],
            index_build_checksum=row[14],
        )

    def _write_vector_sidecar(
        self,
        document: SourceDocument,
        metadata: EmbeddingMetadata,
        vector: list[float],
    ) -> str:
        filename = f"{_safe_document_key(document.document_id)}.json"
        path = self.vector_dir / filename
        payload = {
            "document_id": document.document_id,
            "text_sha256": document.text_sha256,
            "embedding_metadata": metadata.model_dump(mode="json"),
            "vector": vector,
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        if path.exists() and path.read_text(encoding="utf-8") == encoded:
            return path.relative_to(self.root).as_posix()
        path.write_text(encoded, encoding="utf-8")
        return path.relative_to(self.root).as_posix()


def deterministic_test_embedding_metadata() -> EmbeddingMetadata:
    return EmbeddingMetadata(
        provider="local-test",
        model="deterministic-sha256",
        version="1",
        fixture_id="deterministic-test-embedding-v1",
        dimensions=VECTOR_DIMENSIONS,
    )


def deterministic_test_embedding(document: SourceDocument) -> list[float]:
    digest = hashlib.sha256(
        f"{document.document_id}\n{document.text_sha256}\n{document.text}".encode()
    ).digest()
    return [
        round(int.from_bytes(digest[offset : offset + 4], "big") / 0xFFFFFFFF, 8)
        for offset in range(0, VECTOR_DIMENSIONS * 4, 4)
    ]


def _index_build_checksum(
    document: SourceDocument,
    metadata: EmbeddingMetadata,
    vector_path: str,
) -> str:
    payload = {
        "document_id": document.document_id,
        "text_sha256": document.text_sha256,
        "embedding_metadata": metadata.model_dump(mode="json"),
        "index_schema_version": INDEX_SCHEMA_VERSION,
        "vector_path": vector_path,
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode()).hexdigest()


def _safe_document_key(document_id: str) -> str:
    return hashlib.sha256(document_id.encode()).hexdigest()
