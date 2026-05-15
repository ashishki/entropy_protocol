"""Unit tests for artifact evidence-index automation helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from entropy.artifacts import (
    ArtifactEvidenceIndexEntry,
    ArtifactEvidenceIndexViolation,
    build_artifact_evidence_index_rows,
    default_artifact_evidence_index_entries,
    upsert_artifact_evidence_index_rows,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_index_helper_requires_existing_refs(tmp_path: Path) -> None:
    existing = tmp_path / "existing.md"
    existing.write_text("ok\n", encoding="utf-8")

    rows = build_artifact_evidence_index_rows(
        (
            ArtifactEvidenceIndexEntry(
                topic="Existing Evidence",
                artifact_type="Test result",
                locations=("existing.md",),
                scope_covered="existing file reference",
                last_verified="2026-05-14: scoped test passed",
            ),
        ),
        project_root=tmp_path,
    )

    assert rows == (
        "| Existing Evidence | Test result | `existing.md` | existing file reference | "
        "2026-05-14: scoped test passed | Yes |",
    )

    with pytest.raises(ArtifactEvidenceIndexViolation, match="does not exist"):
        build_artifact_evidence_index_rows(
            (
                ArtifactEvidenceIndexEntry(
                    topic="Missing Evidence",
                    artifact_type="Test result",
                    locations=("missing.md",),
                    scope_covered="missing file reference",
                    last_verified="2026-05-14: scoped test failed",
                ),
            ),
            project_root=tmp_path,
        )


def test_index_helper_emits_deterministic_rows() -> None:
    entries = default_artifact_evidence_index_entries(
        last_verified="2026-05-14: artifact pipeline checks passed"
    )

    rows = build_artifact_evidence_index_rows(entries, project_root=PROJECT_ROOT)

    assert rows == build_artifact_evidence_index_rows(reversed(entries), project_root=PROJECT_ROOT)
    assert [row.split("|")[1].strip() for row in rows] == [
        "T75-T78 Executable Artifact Validation",
        "T79-T82 Artifact Registry",
        "T83-T86 Reproducibility Runner",
        "T87-T88 Evidence Packet Schema And CLI",
    ]
    assert "`src/entropy/artifacts/validation.py`" in rows[0]
    assert "`src/entropy/artifacts/registry.py`" in rows[1]
    assert "`src/entropy/artifacts/reproducibility.py`" in rows[2]
    assert "`src/entropy/artifacts/evidence.py`" in rows[3]

    updated = upsert_artifact_evidence_index_rows(
        "\n".join(
            (
                "# Evidence Index",
                "",
                "## Evidence Table",
                "",
                "| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |",
                "|------------------------|---------------|----------|---------------|---------------|------------|",
                "| T79-T82 Artifact Registry | old | `old.md` | old | old | Yes |",
                "",
                "## Pending Evidence",
                "",
                "None.",
                "",
            )
        ),
        rows[1:2],
    )

    assert updated.count("T79-T82 Artifact Registry") == 1
    assert "`src/entropy/artifacts/registry.py`" in updated
    assert "`old.md`" not in updated


def test_index_helper_rejects_missing_canonical_proof() -> None:
    with pytest.raises(ValidationError, match="cannot be canonical proof"):
        ArtifactEvidenceIndexEntry(
            topic="Pending Evidence",
            artifact_type="Generated packet",
            locations=("pending.json",),
            scope_covered="not yet verified",
            last_verified="pending",
            status="pending",
            canonical=True,
        )

    pending = ArtifactEvidenceIndexEntry(
        topic="Pending Evidence",
        artifact_type="Generated packet",
        locations=("pending.json",),
        scope_covered="not yet verified",
        last_verified="pending",
        status="pending",
        canonical=False,
    )
    with pytest.raises(ArtifactEvidenceIndexViolation, match="require verified"):
        build_artifact_evidence_index_rows((pending,), project_root=PROJECT_ROOT)
