"""Reset-era phase-gate evidence packet assembly."""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from entropy.evidence.artifacts import DEFAULT_EVIDENCE_INDEX, EvidenceCollectionError
from entropy.governance.approval import HumanApprovalRecord, build_phase_gate_report

DEFAULT_PHASE3_REQUIRED_EVIDENCE_TOPICS = (
    "T07 Governance Approval Gate Audit",
    "T08 Data and Leakage Gate Verification",
    "T09 SimBroker and Cost Surface Regression",
    "T10 Attribution Stream Boundary Audit",
    "T11 Phase-Gate Evidence Packet",
)
DEFAULT_PHASE3_REQUIRED_HUMAN_APPROVALS = (
    "phase_gate:phase-3-evaluation-safety",
    "holdout_access:archive_holdout",
    "provider_activation:declared_provider_contract",
    "product_bridge_activation:declared_bridge_contract",
)
DEFAULT_BLOCKED_CLAIM_SURFACES = (
    "OOS/performance approval",
    "production approval",
    "capital-ready approval",
)


@dataclass(frozen=True)
class EvidenceIndexRow:
    """One canonical evidence row selected for a phase-gate packet."""

    topic: str
    artifact_type: str
    locations: tuple[str, ...]
    scope: str
    last_verified: str
    canonical: bool


@dataclass(frozen=True)
class ClaimSurfaceStatus:
    """A reportable claim surface and its current gate status."""

    surface: str
    status: Literal["BLOCKED"]
    reason_code: str


@dataclass(frozen=True)
class PhaseGateEvidencePacket:
    """Deterministic packet for a reset-era phase-gate review."""

    phase: int
    phase_name: str
    phase_gate_id: str
    baseline: str
    phase_gate_status: Literal["APPROVED", "NOT_APPROVED"]
    phase_gate_reason_code: str
    required_human_approvals: tuple[str, ...]
    blocked_claim_surfaces: tuple[ClaimSurfaceStatus, ...]
    evidence_rows: tuple[EvidenceIndexRow, ...]

    def to_markdown(self) -> str:
        """Render a stable Markdown packet."""
        lines = [
            f"# Phase {self.phase} Evidence Packet",
            "",
            "Status: IMPLEMENTATION_EVIDENCE_ONLY",
            f"Phase gate id: {self.phase_gate_id}",
            f"Phase gate approval: {self.phase_gate_status}",
            f"Phase gate reason: {self.phase_gate_reason_code}",
            f"Baseline: {self.baseline}",
            "",
            "## Required Human Approvals",
            "",
        ]
        lines.extend(f"- {approval}" for approval in self.required_human_approvals)
        lines.extend(
            [
                "",
                "## Blocked Claim Surfaces",
                "",
            ]
        )
        lines.extend(
            f"- {surface.surface}: {surface.status} ({surface.reason_code})"
            for surface in self.blocked_claim_surfaces
        )
        lines.extend(
            [
                "",
                "## Evidence Rows",
                "",
                "| Topic | Type | Locations | Last verified | Canonical |",
                "|-------|------|-----------|---------------|-----------|",
            ]
        )
        for row in self.evidence_rows:
            locations = "; ".join(f"`{location}`" for location in row.locations)
            canonical = "Yes" if row.canonical else "No"
            lines.append(
                f"| {row.topic} | {row.artifact_type} | {locations} | "
                f"{row.last_verified} | {canonical} |"
            )
        lines.append("")
        return "\n".join(lines)


def build_phase_gate_evidence_packet(
    *,
    phase: int,
    phase_name: str,
    phase_gate_id: str,
    baseline: str,
    task_results: Mapping[str, bool],
    approval_records: Iterable[HumanApprovalRecord] = (),
    evidence_index_path: Path | str = DEFAULT_EVIDENCE_INDEX,
    project_root: Path | str | None = None,
    required_evidence_topics: Sequence[str] = DEFAULT_PHASE3_REQUIRED_EVIDENCE_TOPICS,
    required_human_approvals: Sequence[str] = DEFAULT_PHASE3_REQUIRED_HUMAN_APPROVALS,
    blocked_claim_surfaces: Sequence[str] = DEFAULT_BLOCKED_CLAIM_SURFACES,
) -> PhaseGateEvidencePacket:
    """Build and verify a deterministic phase-gate evidence packet."""
    evidence_path = Path(evidence_index_path)
    root = Path(project_root) if project_root is not None else Path.cwd()
    evidence_rows = _select_required_rows(
        evidence_path.read_text(encoding="utf-8"),
        required_evidence_topics,
    )
    for row in evidence_rows:
        if not row.canonical:
            raise EvidenceCollectionError(f"Evidence row is not canonical: {row.topic}")
        _verify_locations(row.locations, project_root=root)

    gate_report = build_phase_gate_report(
        phase=phase,
        phase_gate_id=phase_gate_id,
        task_results=task_results,
        approval_records=approval_records,
    )

    return PhaseGateEvidencePacket(
        phase=phase,
        phase_name=phase_name,
        phase_gate_id=phase_gate_id,
        baseline=baseline,
        phase_gate_status=gate_report.status,
        phase_gate_reason_code=gate_report.reason_code,
        required_human_approvals=tuple(required_human_approvals),
        blocked_claim_surfaces=tuple(
            ClaimSurfaceStatus(
                surface=surface,
                status="BLOCKED",
                reason_code="NO_MATCHING_HUMAN_GATE_EVIDENCE",
            )
            for surface in blocked_claim_surfaces
        ),
        evidence_rows=tuple(evidence_rows),
    )


def _select_required_rows(
    evidence_index_text: str,
    required_topics: Sequence[str],
) -> tuple[EvidenceIndexRow, ...]:
    rows = _parse_evidence_table(evidence_index_text)
    selected: list[EvidenceIndexRow] = []
    for topic in required_topics:
        row = next((candidate for candidate in rows if candidate.topic == topic), None)
        if row is None:
            raise EvidenceCollectionError(f"Missing evidence row: {topic}")
        selected.append(row)
    return tuple(selected)


def _parse_evidence_table(evidence_index_text: str) -> tuple[EvidenceIndexRow, ...]:
    try:
        start = evidence_index_text.index("## Evidence Table")
        end = evidence_index_text.index("## Pending Evidence", start)
    except ValueError as exc:
        raise EvidenceCollectionError("Evidence index table headings are missing") from exc

    rows: list[EvidenceIndexRow] = []
    for line in evidence_index_text[start:end].splitlines():
        if not line.startswith("|") or set(line.replace("|", "").strip()) <= {"-"}:
            continue
        if "Topic / Finding / Task" in line:
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6:
            raise EvidenceCollectionError("Malformed evidence row: " + line)
        rows.append(
            EvidenceIndexRow(
                topic=cells[0],
                artifact_type=cells[1],
                locations=tuple(re.findall(r"`([^`]+)`", cells[2])),
                scope=cells[3],
                last_verified=cells[4],
                canonical=cells[5].lower() == "yes",
            )
        )
    return tuple(rows)


def _verify_locations(locations: Sequence[str], *, project_root: Path) -> None:
    if not locations:
        raise EvidenceCollectionError("Evidence row has no artifact locations")
    for location in locations:
        file_path, _, symbol_name = location.partition("::")
        artifact_path = project_root / file_path
        if not artifact_path.exists():
            raise EvidenceCollectionError("Missing evidence artifact: " + location)
        if symbol_name and not _python_file_defines_symbol(artifact_path, symbol_name):
            raise EvidenceCollectionError("Missing evidence symbol: " + location)


def _python_file_defines_symbol(path: Path, symbol_name: str) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return any(
        isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef) and node.name == symbol_name
        for node in ast.walk(tree)
    )


__all__ = [
    "DEFAULT_BLOCKED_CLAIM_SURFACES",
    "DEFAULT_PHASE3_REQUIRED_EVIDENCE_TOPICS",
    "DEFAULT_PHASE3_REQUIRED_HUMAN_APPROVALS",
    "ClaimSurfaceStatus",
    "EvidenceIndexRow",
    "PhaseGateEvidencePacket",
    "build_phase_gate_evidence_packet",
]
