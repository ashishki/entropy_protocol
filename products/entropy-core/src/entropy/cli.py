"""CLI entry point for Entropy Protocol."""

import json
import os
from pathlib import Path
from typing import Any, NoReturn, cast

import duckdb
import typer
from sqlalchemy import create_engine, text

from entropy import __version__
from entropy.artifacts import (
    ArtifactEvidencePacket,
    ArtifactHashCompareRunner,
    ArtifactRegistryDuplicate,
    ArtifactRegistryNotFound,
    ArtifactRegistryViolation,
    ArtifactValidationError,
    ArtifactValidationResult,
    ProductBridgeProfileViolation,
    ReproducibilityManifest,
    build_artifact_evidence_packet,
    list_artifact_records,
    read_artifact_history,
    read_artifact_governance_history,
    record_artifact_governance_transition,
    register_artifact_file,
    safe_registry_record_metadata,
    show_artifact_record,
    validate_artifact_file,
    validate_artifact_profile,
)
from entropy.artifacts.governance import ArtifactGovernanceState, ArtifactGovernanceViolation

app = typer.Typer(
    help="Entropy Protocol command-line interface.",
    no_args_is_help=True,
    rich_markup_mode=None,
)

artifact_app = typer.Typer(
    help="Validate local Core artifact contracts.",
    no_args_is_help=True,
    rich_markup_mode=None,
)
evidence_app = typer.Typer(
    help="Build and inspect local artifact evidence packets.",
    no_args_is_help=True,
    rich_markup_mode=None,
)
governance_app = typer.Typer(
    help="Record and inspect local artifact governance transitions.",
    no_args_is_help=True,
    rich_markup_mode=None,
)
app.add_typer(artifact_app, name="artifact")
app.add_typer(evidence_app, name="evidence")
app.add_typer(governance_app, name="governance")


@app.callback()
def callback() -> None:
    """Operate Entropy Protocol from the command line."""


@app.command()
def version() -> None:
    """Print the installed package version."""
    typer.echo(__version__)


def check_postgres() -> dict[str, str]:
    """Check PostgreSQL connectivity without exposing connection details."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return {"name": "postgres", "status": "fail", "error": "DATABASE_URL is not set"}

    engine = create_engine(database_url)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        return {"name": "postgres", "status": "fail", "error": exc.__class__.__name__}
    finally:
        engine.dispose()

    return {"name": "postgres", "status": "ok"}


def check_duckdb() -> dict[str, str]:
    """Check embedded DuckDB availability."""
    try:
        with duckdb.connect(":memory:") as connection:
            connection.execute("SELECT 1").fetchone()
    except Exception as exc:
        return {"name": "duckdb", "status": "fail", "error": exc.__class__.__name__}

    return {"name": "duckdb", "status": "ok"}


@app.command()
def health() -> None:
    """Print machine-readable health status."""
    checks = [check_postgres(), check_duckdb()]
    failed_checks = [check for check in checks if check["status"] != "ok"]

    if failed_checks:
        payload: dict[str, Any] = {"status": "degraded", "checks": failed_checks}
        typer.echo(json.dumps(payload, sort_keys=True))
        raise typer.Exit(code=1)

    typer.echo(json.dumps({"status": "ok"}, sort_keys=True))


@artifact_app.command("validate")
def validate_artifact(path: Path, profile: str = typer.Option("generic", "--profile")) -> None:
    """Validate a local entropy-core-artifact/v1 JSON or YAML file."""
    result = _validate_artifact_file_for_profile(path, profile)
    typer.echo(json.dumps(result.model_dump(mode="json"), sort_keys=True))
    if not result.ok:
        raise typer.Exit(code=1)


@artifact_app.command("register")
def register_artifact(path: Path, profile: str = typer.Option("generic", "--profile")) -> None:
    """Validate and register a local artifact file."""
    profile_result = _validate_artifact_file_for_profile(path, profile)
    if not profile_result.ok:
        typer.echo(json.dumps(profile_result.model_dump(mode="json"), sort_keys=True))
        raise typer.Exit(code=1)

    try:
        record, event = register_artifact_file(path, _artifact_registry_dir())
    except ArtifactRegistryDuplicate:
        _echo_artifact_error("artifact_registry.duplicate", "Artifact is already registered.")
    except ArtifactRegistryViolation:
        _echo_artifact_error("artifact_registry.invalid", "Artifact could not be registered.")

    payload = {
        "ok": True,
        "artifact": safe_registry_record_metadata(record),
        "event": event.model_dump(mode="json"),
    }
    typer.echo(json.dumps(payload, sort_keys=True))


@artifact_app.command("show")
def show_artifact(artifact_id: str) -> None:
    """Show safe metadata for a registered artifact."""
    try:
        record = show_artifact_record(artifact_id, _artifact_registry_dir())
    except ArtifactRegistryNotFound:
        _echo_artifact_error("artifact_registry.not_found", "Artifact was not found.")

    typer.echo(json.dumps({"ok": True, "artifact": safe_registry_record_metadata(record)}, sort_keys=True))


@artifact_app.command("list")
def list_artifacts() -> None:
    """List registered artifact metadata."""
    artifacts = [
        safe_registry_record_metadata(record)
        for record in list_artifact_records(_artifact_registry_dir())
    ]
    typer.echo(json.dumps({"ok": True, "artifacts": artifacts}, sort_keys=True))


@artifact_app.command("history")
def artifact_history(artifact_id: str) -> None:
    """Show append-only registry events for a registered artifact."""
    try:
        events = read_artifact_history(artifact_id, _artifact_registry_dir())
    except ArtifactRegistryNotFound:
        _echo_artifact_error("artifact_registry.not_found", "Artifact was not found.")

    typer.echo(
        json.dumps(
            {"ok": True, "artifact_id": artifact_id, "events": [event.model_dump(mode="json") for event in events]},
            sort_keys=True,
        )
    )


@artifact_app.command("compare")
def compare_artifact(artifact_id: str, against: Path = typer.Option(..., "--against")) -> None:
    """Compare a rerun output against an approved local reproducibility manifest."""
    manifest = _load_manifest_or_exit(artifact_id)
    try:
        expected_path = Path(manifest.expected_output_refs[0])
        expected_payload = json.loads(expected_path.read_text(encoding="utf-8"))
        actual_payload = json.loads(against.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, IndexError):
        _echo_artifact_error(
            "artifact_reproducibility.compare_input_error",
            "Reproducibility comparison inputs could not be read.",
        )

    result = ArtifactHashCompareRunner().compare_json_output(
        manifest,
        manifest.expected_output_refs[0],
        expected_payload,
        actual_payload,
    )
    payload = {
        "ok": True,
        "artifact_id": artifact_id,
        "result": result.model_dump(mode="json"),
        "declared_nondeterminism": [
            entry.model_dump(mode="json") for entry in manifest.accepted_nondeterminism
        ],
        "non_reproducible_fields": list(manifest.non_reproducible_fields),
        "limitations": {"direct_rerun_execution": "blocked"},
    }
    typer.echo(json.dumps(payload, sort_keys=True))


@artifact_app.command("reproduce")
def reproduce_artifact(artifact_id: str) -> None:
    """Refuse direct artifact rerun execution unless a future gate approves it."""
    _load_manifest_or_exit(artifact_id)
    _echo_artifact_error(
        "artifact_reproducibility.execution_blocked",
        "Direct reproducibility command execution is not approved.",
    )


def _artifact_registry_dir() -> Path:
    return Path(os.getenv("ENTROPY_REGISTRY_DIR", "artifacts/registry"))


def _artifact_manifest_dir() -> Path:
    return Path(os.getenv("ENTROPY_REPRODUCIBILITY_MANIFEST_DIR", "artifacts/reproducibility/manifests"))


def _validate_artifact_file_for_profile(path: Path, profile: str) -> ArtifactValidationResult:
    result = validate_artifact_file(path)
    if not result.ok or result.artifact is None:
        return result
    try:
        validate_artifact_profile(result.artifact, profile)
    except ProductBridgeProfileViolation as exc:
        return ArtifactValidationResult(
            ok=False,
            errors=(
                ArtifactValidationError(
                    path="$",
                    code="artifact.profile_violation",
                    severity="P1",
                    message=str(exc),
                ),
            ),
        )
    return result


@evidence_app.command("build")
def build_evidence(artifact_id: str) -> None:
    """Build a deterministic local evidence packet for a registered artifact."""
    try:
        record = show_artifact_record(artifact_id, _artifact_registry_dir())
    except ArtifactRegistryNotFound:
        _echo_artifact_error(
            "artifact_evidence.inconsistent_prerequisites",
            "Evidence packet prerequisites are inconsistent.",
        )
    artifact = record.validation_result.artifact
    if not record.validation_result.ok or artifact is None:
        _echo_artifact_error(
            "artifact_evidence.inconsistent_prerequisites",
            "Evidence packet prerequisites are inconsistent.",
        )

    packet = build_artifact_evidence_packet(
        record,
        limitations=artifact.limitations,
        review_refs=("docs/audit/REPRODUCIBILITY_RUNNER_REVIEW.md",),
    )
    path = _artifact_evidence_dir() / f"{artifact_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(packet.to_deterministic_json() + "\n", encoding="utf-8")
    typer.echo(
        json.dumps(
            {
                "ok": True,
                "artifact_id": artifact_id,
                "path": str(path),
                "packet": _safe_evidence_summary(packet),
            },
            sort_keys=True,
        )
    )


@evidence_app.command("inspect")
def inspect_evidence(artifact_id: str) -> None:
    """Inspect safe summary fields for a local evidence packet."""
    path = _artifact_evidence_dir() / f"{artifact_id}.json"
    try:
        packet = ArtifactEvidencePacket.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        _echo_artifact_error("artifact_evidence.not_found", "Evidence packet was not found.")
    typer.echo(json.dumps({"ok": True, "packet": _safe_evidence_summary(packet)}, sort_keys=True))


@governance_app.command("transition")
def transition_governance(
    artifact_id: str,
    to_state: str = typer.Option(..., "--to"),
    approval_event_ref: str | None = typer.Option(None, "--approval-event-ref"),
    reason: str = typer.Option("local governance transition", "--reason"),
) -> None:
    """Record an append-only local governance transition event."""
    try:
        event = record_artifact_governance_transition(
            artifact_id,
            cast(ArtifactGovernanceState, to_state),
            _artifact_governance_dir(),
            approval_event_ref=approval_event_ref,
            reason=reason,
        )
    except (ArtifactGovernanceViolation, ValueError):
        _echo_artifact_error(
            "artifact_governance.invalid_transition",
            "Artifact governance transition is not allowed.",
        )

    typer.echo(json.dumps({"ok": True, "event": event.model_dump(mode="json")}, sort_keys=True))


@governance_app.command("history")
def governance_history(artifact_id: str) -> None:
    """Print deterministic append-only governance transition history."""
    events = read_artifact_governance_history(artifact_id, _artifact_governance_dir())
    typer.echo(
        json.dumps(
            {"ok": True, "artifact_id": artifact_id, "events": [event.model_dump(mode="json") for event in events]},
            sort_keys=True,
        )
    )


def _artifact_evidence_dir() -> Path:
    return Path(os.getenv("ENTROPY_EVIDENCE_DIR", "artifacts/evidence"))


def _artifact_governance_dir() -> Path:
    return Path(os.getenv("ENTROPY_GOVERNANCE_DIR", "artifacts/governance"))


def _safe_evidence_summary(packet: ArtifactEvidencePacket) -> dict[str, object]:
    return {
        "artifact_summary": packet.artifact_summary.model_dump(mode="json"),
        "registry_status": packet.registry_status.model_dump(mode="json"),
        "reproducibility_status": packet.reproducibility_status,
        "approval_state": packet.approval_state,
        "limitations": list(packet.limitations),
        "claim_boundary": list(packet.claim_boundary),
        "review_refs": list(packet.review_refs),
    }


def _load_manifest_or_exit(artifact_id: str) -> ReproducibilityManifest:
    manifest_path = _artifact_manifest_dir() / f"{artifact_id}.json"
    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        return ReproducibilityManifest.model_validate(payload)
    except (OSError, json.JSONDecodeError, ValueError):
        _echo_artifact_error(
            "artifact_reproducibility.manifest_not_found",
            "Approved local reproducibility manifest was not found.",
        )


def _echo_artifact_error(code: str, message: str) -> NoReturn:
    payload = {
        "ok": False,
        "errors": [{"code": code, "severity": "P1", "message": message, "path": "$"}],
    }
    typer.echo(json.dumps(payload, sort_keys=True))
    raise typer.Exit(code=1)


def main() -> None:
    """Run the CLI application."""
    app()
