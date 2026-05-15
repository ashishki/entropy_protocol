"""Unit tests for local artifact store abstractions."""

from __future__ import annotations

import inspect
from pathlib import Path

import pytest

import entropy.artifacts.store as store_module
from entropy.artifacts import ArtifactStoreViolation, FilesystemArtifactStore, ObjectArtifactStore


def test_filesystem_store_writes_content_addressed_payloads(tmp_path: Path) -> None:
    store = FilesystemArtifactStore(tmp_path)

    first_ref = store.write_payload('{"ok":true}', prefix="evidence")
    second_ref = store.write_payload('{"ok":true}', prefix="evidence")

    assert first_ref == second_ref
    assert first_ref.backend == "filesystem"
    assert first_ref.sha256.startswith("sha256:")
    assert first_ref.ref.startswith("artifact://filesystem/evidence/")
    assert (tmp_path / first_ref.relative_path).read_text(encoding="utf-8") == '{"ok":true}'


def test_store_rejects_unsafe_paths(tmp_path: Path) -> None:
    store = FilesystemArtifactStore(tmp_path)

    for prefix in ("../outside", "/absolute", "nested/../../outside", ""):
        with pytest.raises(ArtifactStoreViolation, match="safe relative paths"):
            store.write_payload(b"payload", prefix=prefix)


def test_object_store_boundary_has_no_runtime_dependency() -> None:
    assert hasattr(ObjectArtifactStore, "write_payload")
    source = inspect.getsource(store_module)

    assert "boto" not in source
    assert "s3fs" not in source
    assert "requests" not in source
    assert "httpx" not in source
