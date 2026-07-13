"""Local deterministic evidence-index lookup primitives."""

from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict


EVIDENCE_LOOKUP_STATUSES = ("found", "insufficient_evidence")
EVIDENCE_LOOKUP_BLOCKED_SURFACES = (
    "runtime_rag",
    "hosted_search",
    "public_api",
    "public_sdk",
    "live_execution",
    "holdout_access",
    "production_credentials",
    "capital",
    "external_compliance",
)


class EvidenceLookupResult(BaseModel):
    """Safe local metadata for one evidence lookup."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    query: str
    status: Literal["found", "insufficient_evidence"]
    topic: str | None = None
    artifact_type: str | None = None
    locations: tuple[str, ...] = ()
    scope_covered: str | None = None
    last_verified: str | None = None
    canonical: bool | None = None
    reason_code: str
    approval_state: Literal["not_approved"] = "not_approved"
    blocked_surfaces: tuple[str, ...] = EVIDENCE_LOOKUP_BLOCKED_SURFACES


def lookup_evidence_index(index_text: str, query: str) -> EvidenceLookupResult:
    """Return exact local evidence metadata from a Markdown evidence table."""

    normalized_query = query.strip().lower()
    if not normalized_query:
        return _missing_result(query, "empty_query")

    for row in _iter_evidence_rows(index_text):
        topic = row["topic"]
        locations = _split_locations(row["location"])
        if normalized_query == topic.lower() or normalized_query in {
            location.lower() for location in locations
        }:
            return EvidenceLookupResult(
                query=query,
                status="found",
                topic=topic,
                artifact_type=row["artifact_type"],
                locations=locations,
                scope_covered=row["scope_covered"],
                last_verified=row["last_verified"],
                canonical=row["canonical"].lower() == "yes",
                reason_code="exact_evidence_match",
            )
    return _missing_result(query, "evidence_topic_not_found")


def lookup_packet_evidence_refs(
    index_text: str,
    evidence_refs: tuple[str, ...],
) -> tuple[EvidenceLookupResult, ...]:
    """Lookup local evidence metadata for packet evidence references."""

    if not evidence_refs:
        return (_missing_result("", "empty_evidence_refs"),)
    return tuple(lookup_evidence_index(index_text, ref) for ref in evidence_refs)


def _iter_evidence_rows(index_text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in index_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) != 6 or cells[0] == "Topic / Finding / Task":
            continue
        rows.append(
            {
                "topic": cells[0],
                "artifact_type": cells[1],
                "location": cells[2],
                "scope_covered": cells[3],
                "last_verified": cells[4],
                "canonical": cells[5],
            }
        )
    return rows


def _split_locations(location_cell: str) -> tuple[str, ...]:
    return tuple(
        location.strip().strip("`") for location in location_cell.split(";") if location.strip()
    )


def _missing_result(query: str, reason_code: str) -> EvidenceLookupResult:
    return EvidenceLookupResult(
        query=query,
        status="insufficient_evidence",
        reason_code=reason_code,
    )
