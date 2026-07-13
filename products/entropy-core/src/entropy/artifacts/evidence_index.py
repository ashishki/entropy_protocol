"""Deterministic evidence-index row helpers for artifact evidence outputs."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

ArtifactEvidenceIndexStatus = Literal["verified", "pending", "missing"]


class ArtifactEvidenceIndexViolation(ValueError):
    """Raised when evidence-index rows would overstate proof status."""


class ArtifactEvidenceIndexEntry(BaseModel):
    """One generated Markdown row candidate for the evidence index."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    topic: str = Field(min_length=1)
    artifact_type: str = Field(min_length=1)
    locations: tuple[str, ...] = Field(min_length=1)
    scope_covered: str = Field(min_length=1)
    last_verified: str = Field(min_length=1)
    status: ArtifactEvidenceIndexStatus = "verified"
    canonical: bool = True

    @model_validator(mode="after")
    def validate_markdown_cells(self) -> "ArtifactEvidenceIndexEntry":
        cell_values = (
            self.topic,
            self.artifact_type,
            self.scope_covered,
            self.last_verified,
            *self.locations,
        )
        for value in cell_values:
            if "|" in value or "\n" in value:
                raise ArtifactEvidenceIndexViolation("Evidence index cells cannot contain pipes.")
        if self.canonical and self.status != "verified":
            raise ArtifactEvidenceIndexViolation(
                "Pending or missing artifact evidence cannot be canonical proof."
            )
        return self


def default_artifact_evidence_index_entries(
    *,
    last_verified: str,
) -> tuple[ArtifactEvidenceIndexEntry, ...]:
    """Return the Core artifact pipeline evidence rows in deterministic topic order."""
    return tuple(
        sorted(
            (
                ArtifactEvidenceIndexEntry(
                    topic="T75-T78 Executable Artifact Validation",
                    artifact_type="Test result / review report",
                    locations=(
                        "src/entropy/artifacts/contract.py",
                        "src/entropy/artifacts/validation.py",
                        "src/entropy/cli.py",
                        "tests/unit/test_artifact_contract_v1.py",
                        "tests/unit/test_artifact_validation.py",
                        "tests/unit/test_artifact_cli.py",
                        "tests/fixtures/artifacts/",
                        "docs/audit/EXECUTABLE_ARTIFACT_VALIDATION_REVIEW.md",
                    ),
                    scope_covered=(
                        "Executable artifact schema, deterministic loading, redacted "
                        "validation results, and local validation CLI behavior"
                    ),
                    last_verified=last_verified,
                ),
                ArtifactEvidenceIndexEntry(
                    topic="T79-T82 Artifact Registry",
                    artifact_type="Test result / review report",
                    locations=(
                        "src/entropy/artifacts/registry.py",
                        "src/entropy/cli.py",
                        "tests/unit/test_artifact_registry.py",
                        "tests/unit/test_artifact_registry_cli.py",
                        "docs/audit/ARTIFACT_REGISTRY_REVIEW.md",
                    ),
                    scope_covered=(
                        "Governed immutable registry records, append-only events, "
                        "local registry CLI behavior, duplicate rejection, and safe metadata"
                    ),
                    last_verified=last_verified,
                ),
                ArtifactEvidenceIndexEntry(
                    topic="T83-T86 Reproducibility Runner",
                    artifact_type="Test result / review report",
                    locations=(
                        "src/entropy/artifacts/reproducibility.py",
                        "src/entropy/cli.py",
                        "tests/unit/test_reproducibility_manifest.py",
                        "tests/unit/test_reproducibility_runner.py",
                        "tests/unit/test_reproducibility_cli.py",
                        "docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",
                    ),
                    scope_covered=(
                        "Reproducibility manifest schema, deterministic hash comparison, "
                        "safe diff metadata, compare-only CLI, and blocked direct reruns"
                    ),
                    last_verified=last_verified,
                ),
                ArtifactEvidenceIndexEntry(
                    topic="T87-T88 Evidence Packet Schema And CLI",
                    artifact_type="Test result",
                    locations=(
                        "src/entropy/artifacts/evidence.py",
                        "src/entropy/cli.py",
                        "tests/unit/test_artifact_evidence_packet.py",
                        "tests/unit/test_artifact_evidence_cli.py",
                    ),
                    scope_covered=(
                        "Machine-readable evidence packet schema, deterministic "
                        "serialization, unsupported approval rejection, local evidence "
                        "build, and safe evidence inspect CLI"
                    ),
                    last_verified=last_verified,
                ),
            ),
            key=lambda entry: entry.topic,
        )
    )


def build_artifact_evidence_index_rows(
    entries: Iterable[ArtifactEvidenceIndexEntry],
    *,
    project_root: str | Path = ".",
) -> tuple[str, ...]:
    """Validate references and render deterministic Markdown evidence rows."""
    normalized_entries = tuple(sorted(entries, key=lambda entry: entry.topic))
    root = Path(project_root)
    for entry in normalized_entries:
        _validate_references_exist(entry, root)
    return tuple(_format_row(entry) for entry in normalized_entries)


def upsert_artifact_evidence_index_rows(index_text: str, rows: Iterable[str]) -> str:
    """Return index text with generated rows inserted or replaced by topic."""
    new_rows = tuple(sorted(rows, key=_row_topic))
    topics = {_row_topic(row) for row in new_rows}
    try:
        start = index_text.index("## Evidence Table")
        end = index_text.index("## Pending Evidence", start)
    except ValueError as exc:
        raise ArtifactEvidenceIndexViolation("Evidence index table headings are missing.") from exc

    table_lines = index_text[start:end].rstrip("\n").splitlines()
    kept_lines: list[str] = []
    for line in table_lines:
        if line.startswith("|") and _is_data_row(line) and _row_topic(line) in topics:
            continue
        kept_lines.append(line.rstrip())

    updated_table = "\n".join((*kept_lines, *new_rows))
    return index_text[:start] + updated_table + "\n\n" + index_text[end:].lstrip("\n")


def _validate_references_exist(entry: ArtifactEvidenceIndexEntry, root: Path) -> None:
    if entry.status != "verified":
        raise ArtifactEvidenceIndexViolation("Evidence index rows require verified artifacts.")

    for location in entry.locations:
        file_ref = location.partition("::")[0]
        path = Path(file_ref)
        if path.is_absolute() or ".." in path.parts:
            raise ArtifactEvidenceIndexViolation("Evidence index references must be repo-relative.")
        if not (root / path).exists():
            raise ArtifactEvidenceIndexViolation(
                "Evidence index reference does not exist: " + file_ref
            )


def _format_row(entry: ArtifactEvidenceIndexEntry) -> str:
    canonical = "Yes" if entry.canonical else "No"
    locations = "; ".join(f"`{location}`" for location in entry.locations)
    return (
        f"| {entry.topic} | {entry.artifact_type} | {locations} | "
        f"{entry.scope_covered} | {entry.last_verified} | {canonical} |"
    )


def _row_topic(row: str) -> str:
    cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
    if len(cells) < 1 or not cells[0]:
        raise ArtifactEvidenceIndexViolation("Evidence index row is malformed.")
    return cells[0]


def _is_data_row(line: str) -> bool:
    stripped = line.replace("|", "").strip()
    return bool(stripped) and set(stripped) != {"-"} and "Topic / Finding / Task" not in line


__all__ = [
    "ArtifactEvidenceIndexEntry",
    "ArtifactEvidenceIndexStatus",
    "ArtifactEvidenceIndexViolation",
    "build_artifact_evidence_index_rows",
    "default_artifact_evidence_index_entries",
    "upsert_artifact_evidence_index_rows",
]
