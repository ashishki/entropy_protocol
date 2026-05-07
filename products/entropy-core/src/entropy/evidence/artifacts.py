"""Phase 0 implementation evidence artifact generation."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import date, datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from entropy.db.models import Run, TrialRegistry
from entropy.walkforward.leakage import CheckStatus, LeakageReport

TASK_IDS = tuple(f"T{index:02d}" for index in range(1, 25))
DEFAULT_EVIDENCE_INDEX = Path("docs/EVIDENCE_INDEX.md")


class EvidenceCollectionError(Exception):
    """Raised when complete evidence cannot be collected."""


def generate_evaluation_report(
    trial_id: str,
    *,
    session: Session,
    net_sharpe: float | None = None,
) -> str:
    """Render a deterministic Markdown implementation-evidence report."""
    trial = session.execute(
        select(TrialRegistry).where(TrialRegistry.trial_id == trial_id)
    ).scalar_one_or_none()
    if trial is None:
        raise EvidenceCollectionError("Trial not found: " + trial_id)

    runs = tuple(
        session.execute(select(Run).where(Run.trial_id == trial_id).order_by(Run.run_id)).scalars()
    )
    net_sharpe_text = "not_computed" if net_sharpe is None else _format_float(net_sharpe)
    lines = [
        "# Phase 0 Evaluation Report",
        "",
        "Status: IMPLEMENTATION_EVIDENCE_ONLY",
        "Phase gate approval: NOT_APPROVED",
        "",
        "## Trial",
        "",
        f"- trial_id: {trial.trial_id}",
        f"- family_tag: {trial.family_tag}",
        f"- hypothesis: {trial.hypothesis}",
        f"- dataset_hash: {trial.dataset_hash}",
        f"- code_hash: {trial.code_hash}",
        f"- policy_hash: {trial.policy_hash}",
        f"- registered_at: {_iso(trial.registered_at)}",
        f"- net_sharpe: {net_sharpe_text}",
        "",
        "## Runs",
        "",
    ]
    if not runs:
        lines.append("- no_runs_registered")
    else:
        for run in runs:
            lines.extend(
                [
                    f"- run_id: {run.run_id}",
                    f"  - dataset_hash: {run.dataset_hash}",
                    f"  - code_hash: {run.code_hash}",
                    f"  - policy_hash: {run.policy_hash}",
                    f"  - is_window: {_iso(run.is_start)} -> {_iso(run.is_end)}",
                    f"  - oos_window: {_iso(run.oos_start)} -> {_iso(run.oos_end)}",
                    f"  - leakage_status: {run.leakage_status}",
                ]
            )
    lines.append("")
    return "\n".join(lines)


def collect_leakage_evidence(
    trial_id: str,
    *,
    session: Session,
    leakage_reports: Mapping[str, LeakageReport],
    evidence_index_path: Path | str = DEFAULT_EVIDENCE_INDEX,
    check_date: date | str | None = None,
) -> None:
    """Append leakage evidence rows for all registered runs of one trial."""
    runs = tuple(
        session.execute(select(Run).where(Run.trial_id == trial_id).order_by(Run.run_id)).scalars()
    )
    if not runs:
        raise EvidenceCollectionError("No runs found for trial_id: " + trial_id)

    resolved_date = check_date.isoformat() if isinstance(check_date, date) else check_date
    if resolved_date is None:
        resolved_date = date.today().isoformat()
    rows: list[str] = []
    for run in runs:
        report = leakage_reports.get(run.run_id)
        if report is None:
            raise EvidenceCollectionError("Missing LeakageReport for run_id: " + run.run_id)
        if report.overall_status is not CheckStatus.PASS:
            raise EvidenceCollectionError("LeakageReport did not pass for run_id: " + run.run_id)
        rows.append(
            "| "
            + " | ".join(
                [
                    trial_id,
                    run.run_id,
                    resolved_date,
                    report.normalization_leakage.status.value,
                    report.regime_label_lookahead.status.value,
                    report.universe_selection_bias.status.value,
                    report.within_window_optimization.status.value,
                    report.overall_status.value,
                ]
            )
            + " |"
        )

    path = Path(evidence_index_path)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(row + "\n")


def generate_phase0_gate_report(
    *,
    task_results: Mapping[str, bool],
    phase_gate_approved: bool = False,
) -> str:
    """Render deterministic task status evidence for T01-T24."""
    approval = "APPROVED" if phase_gate_approved else "NOT_APPROVED"
    lines = [
        "# Phase 0 Gate Report",
        "",
        "Status: IMPLEMENTATION_EVIDENCE_ONLY",
        f"Phase gate approval: {approval}",
        "",
        "| Task | Status |",
        "|------|--------|",
    ]
    for task_id in TASK_IDS:
        status = "PASS" if task_results.get(task_id, False) else "FAIL"
        lines.append(f"| {task_id} | {status} |")
    lines.append("")
    return "\n".join(lines)


def _iso(value: object) -> str:
    if isinstance(value, datetime | date):
        return value.isoformat()
    return str(value)


def _format_float(value: float) -> str:
    return f"{value:.12g}"


__all__ = [
    "DEFAULT_EVIDENCE_INDEX",
    "TASK_IDS",
    "EvidenceCollectionError",
    "collect_leakage_evidence",
    "generate_evaluation_report",
    "generate_phase0_gate_report",
]
