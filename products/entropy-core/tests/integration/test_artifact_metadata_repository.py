"""Integration-style tests for artifact metadata repository write contracts."""

from __future__ import annotations

import inspect
from typing import Any

from entropy.artifacts import ArtifactMetadataRepository
from entropy.artifacts.repository import ArtifactMetadataRepository as RepositoryClass
from entropy.db.models import ArtifactRecordMetadata, ArtifactValidationEvent
from tests.unit.test_artifact_metadata_repository import valid_record


class FakeSession:
    """Minimal SQLAlchemy session stand-in for insert-only repository tests."""

    def __init__(self) -> None:
        self.added: list[object] = []
        self.commit_count = 0

    def add(self, value: object) -> None:
        self.added.append(value)

    def commit(self) -> None:
        self.commit_count += 1


def test_repository_inserts_artifact_metadata() -> None:
    session = FakeSession()
    record = valid_record()
    repository = ArtifactMetadataRepository(session)  # type: ignore[arg-type]

    metadata_result = repository.insert_artifact_metadata(record)
    event_result = repository.append_validation_event(
        event_id="event-001",
        artifact_id=record.artifact_id,
        validation_result=record.validation_result,
    )

    assert metadata_result.backend == "database"
    assert event_result.backend == "database"
    assert session.commit_count == 2
    assert isinstance(session.added[0], ArtifactRecordMetadata)
    assert isinstance(session.added[1], ArtifactValidationEvent)
    assert session.added[0].artifact_id == record.artifact_id  # type: ignore[attr-defined]
    assert session.added[1].artifact_id == record.artifact_id  # type: ignore[attr-defined]


def test_repository_has_no_update_delete_event_paths() -> None:
    source = inspect.getsource(RepositoryClass).lower()

    assert ".add(" in source
    assert ".commit(" in source
    assert ".execute(" not in source
    assert " update " not in source
    assert " delete " not in source
    assert not hasattr(RepositoryClass, "update_validation_event")
    assert not hasattr(RepositoryClass, "delete_validation_event")


def test_repository_uses_sqlalchemy_objects_without_string_sql() -> None:
    session = FakeSession()
    repository = ArtifactMetadataRepository(session)  # type: ignore[arg-type]

    repository.insert_artifact_metadata(valid_record())

    assert all(not isinstance(value, str) for value in session.added)
    assert all(hasattr(value, "__table__") for value in session.added)


def _unused_type_anchor(_: Any) -> None:
    """Keep imported typing behavior explicit for static checkers."""
