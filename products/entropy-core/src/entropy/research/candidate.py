"""First research candidate preregistration packet."""

from __future__ import annotations

import json
from collections.abc import Sequence
from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

FIRST_RESEARCH_CANDIDATE_SCHEMA_VERSION = "first-research-candidate/v1"

CANONICAL_HYPOTHESIS_FAMILIES = (
    "Funding Signals",
    "Volatility Compression",
    "Structure Levels",
    "Regime-Conditioned Signals",
    "Liquidity / Flow Signals",
)
FIRST_RESEARCH_NO_CLAIM_LABELS = (
    "archive_only_candidate",
    "human_registration_required",
    "not_evaluated",
    "not_holdout_unlock",
    "not_oos_performance",
    "not_phase_gate_approval",
    "not_production",
    "not_capital_ready",
    "not_live_feed",
    "not_broker_exchange",
)
REQUIRED_HASH_PLACEHOLDERS = (
    "dataset_hash",
    "code_hash",
    "policy_hash",
    "parameter_hash",
)
FORBIDDEN_REQUESTED_SURFACE_MARKERS = (
    "holdout",
    "oos",
    "performance",
    "production",
    "capital_ready",
    "live_feed",
    "live_broker",
    "broker",
    "exchange",
)


class CandidateSurfaceError(ValueError):
    """Raised when a candidate packet requests a forbidden surface."""


class CandidateBaseModel(BaseModel):
    """Base model for frozen deterministic candidate packet schemas."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")


class FrozenParameter(CandidateBaseModel):
    """One preregistered parameter lock."""

    name: str
    value: str
    rationale: str


class CandidateHashPlaceholders(CandidateBaseModel):
    """Hash slots that must be bound before evaluation."""

    dataset_hash: str = "PENDING_T16_DATASET_HASH_BINDING"
    code_hash: str = "PENDING_T17_CODE_HASH_BINDING"
    policy_hash: str = "PENDING_T17_POLICY_HASH_BINDING"
    parameter_hash: str = "PENDING_T15_PARAMETER_HASH_BINDING"


class FirstResearchCandidatePacket(CandidateBaseModel):
    """Archive-only preregistration candidate for the first research packet."""

    schema_version: Literal["first-research-candidate/v1"] = FIRST_RESEARCH_CANDIDATE_SCHEMA_VERSION
    candidate_id: str
    hypothesis_text: str
    hypothesis_family: Literal[
        "Funding Signals",
        "Volatility Compression",
        "Structure Levels",
        "Regime-Conditioned Signals",
        "Liquidity / Flow Signals",
    ]
    scope: str
    frozen_parameters: tuple[FrozenParameter, ...] = Field(min_length=1)
    primary_metric: str
    baseline_comparator: str
    minimum_sample_requirement: str
    invalidation_condition: str
    leakage_risks: tuple[str, ...] = Field(min_length=1)
    required_human_registration_gate: Literal["human_registration_required"] = (
        "human_registration_required"
    )
    hash_placeholders: CandidateHashPlaceholders = Field(default_factory=CandidateHashPlaceholders)
    no_claim_labels: tuple[str, ...] = FIRST_RESEARCH_NO_CLAIM_LABELS
    requested_surfaces: tuple[str, ...] = ("archive_local_fixture",)
    evaluation_status: Literal["not_evaluated"] = "not_evaluated"

    @model_validator(mode="after")
    def validate_boundaries(self) -> "FirstResearchCandidatePacket":
        validate_candidate_requested_surfaces(self.requested_surfaces)
        missing_labels = set(FIRST_RESEARCH_NO_CLAIM_LABELS).difference(self.no_claim_labels)
        if missing_labels:
            raise CandidateSurfaceError(
                "Missing first research no-claim labels: " + ", ".join(sorted(missing_labels))
            )
        return self

    def to_markdown(self) -> str:
        """Render the candidate packet as stable Markdown."""
        lines = [
            "# First Research Candidate Packet",
            "",
            "Status: CANDIDATE_ONLY_NOT_REGISTERED",
            f"Schema version: {self.schema_version}",
            f"Candidate id: {self.candidate_id}",
            f"Hypothesis family: {self.hypothesis_family}",
            f"Scope: {self.scope}",
            f"Required gate: {self.required_human_registration_gate}",
            f"Evaluation status: {self.evaluation_status}",
            "",
            "## Hypothesis",
            "",
            self.hypothesis_text,
            "",
            "## Frozen Parameters",
            "",
            "| Name | Value | Rationale |",
            "|------|-------|-----------|",
        ]
        lines.extend(
            f"| {parameter.name} | {parameter.value} | {parameter.rationale} |"
            for parameter in self.frozen_parameters
        )
        lines.extend(
            [
                "",
                "## Readiness Fields",
                "",
                f"- Primary metric: {self.primary_metric}",
                f"- Baseline comparator: {self.baseline_comparator}",
                f"- Minimum sample requirement: {self.minimum_sample_requirement}",
                f"- Invalidation condition: {self.invalidation_condition}",
                "",
                "## Leakage Risks",
                "",
            ]
        )
        lines.extend(f"- {risk}" for risk in self.leakage_risks)
        lines.extend(
            [
                "",
                "## Hash Placeholders",
                "",
            ]
        )
        for name in REQUIRED_HASH_PLACEHOLDERS:
            lines.append(f"- {name}: {getattr(self.hash_placeholders, name)}")
        lines.extend(
            [
                "",
                "## No-Claim Labels",
                "",
            ]
        )
        lines.extend(f"- {label}" for label in self.no_claim_labels)
        lines.extend(
            [
                "",
                "## Requested Surfaces",
                "",
            ]
        )
        lines.extend(f"- {surface}" for surface in self.requested_surfaces)
        lines.append("")
        return "\n".join(lines)


def build_first_research_candidate_packet() -> FirstResearchCandidatePacket:
    """Build the first narrow archive-only research candidate packet."""
    return FirstResearchCandidatePacket(
        candidate_id="FRC-001-VC-BREAKOUT-CONTINUATION",
        hypothesis_text=(
            "When a liquid BTC archive bar sequence shows 20-bar realized volatility "
            "compression followed by an upside close beyond the prior 10-bar high, the next "
            "archive evaluation window should exhibit higher net stream-a-minus-cost outcome "
            "than an always-flat baseline under the preregistered no-claim harness."
        ),
        hypothesis_family="Volatility Compression",
        scope=(
            "archive-only BTC local fixture bars; no holdout, live feed, broker, exchange, "
            "production, capital-ready, or OOS/performance surface"
        ),
        frozen_parameters=(
            FrozenParameter(
                name="compression_window_bars",
                value="20",
                rationale="Freezes the realized-volatility lookback before any evaluation run.",
            ),
            FrozenParameter(
                name="breakout_window_bars",
                value="10",
                rationale="Freezes the prior-high breakout reference before hash binding.",
            ),
            FrozenParameter(
                name="holding_window_bars",
                value="5",
                rationale="Freezes the archive evaluation holding horizon for the first packet.",
            ),
        ),
        primary_metric="net_stream_a_minus_cost_status",
        baseline_comparator="always_flat_archive_baseline",
        minimum_sample_requirement="at least 30 archive fixture candidate events before any summary",
        invalidation_condition=(
            "Reject as not ready if leakage checks fail, required hashes are missing, or sample "
            "count is below the frozen minimum."
        ),
        leakage_risks=(
            "post-hoc threshold tuning after inspecting evaluation output",
            "look-ahead from using future bars in compression or breakout labels",
            "reuse of calibration information across future holdout boundaries",
        ),
    )


def deterministic_candidate_json(packet: FirstResearchCandidatePacket) -> str:
    """Serialize a candidate packet with stable key ordering and compact separators."""
    return json.dumps(packet.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def validate_candidate_requested_surfaces(requested_surfaces: Sequence[str]) -> None:
    """Reject holdout, live, broker/exchange, and unsupported claim surfaces."""
    blocked = tuple(
        sorted(surface for surface in requested_surfaces if _surface_has_forbidden_marker(surface))
    )
    if blocked:
        raise CandidateSurfaceError(
            "Forbidden first research candidate surface: " + ", ".join(blocked)
        )


def _surface_has_forbidden_marker(surface: str) -> bool:
    normalized = _normalize_surface(surface)
    return any(marker in normalized for marker in FORBIDDEN_REQUESTED_SURFACE_MARKERS)


def _normalize_surface(value: str) -> str:
    return "".join(character if character.isalnum() else "_" for character in value.lower())


__all__ = [
    "CANONICAL_HYPOTHESIS_FAMILIES",
    "FIRST_RESEARCH_CANDIDATE_SCHEMA_VERSION",
    "FIRST_RESEARCH_NO_CLAIM_LABELS",
    "REQUIRED_HASH_PLACEHOLDERS",
    "CandidateHashPlaceholders",
    "CandidateSurfaceError",
    "FirstResearchCandidatePacket",
    "FrozenParameter",
    "build_first_research_candidate_packet",
    "deterministic_candidate_json",
    "validate_candidate_requested_surfaces",
]
