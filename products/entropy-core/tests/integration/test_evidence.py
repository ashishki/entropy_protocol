"""Integration tests for Phase 0 evidence artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pytest
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from entropy.db.models import Base, Run
from entropy.evidence import (
    TASK_IDS,
    EvidenceCollectionError,
    collect_leakage_evidence,
    generate_evaluation_report,
    generate_phase0_gate_report,
)
from entropy.models.registry import TrialSpec
from entropy.registry.write import register_trial
from entropy.walkforward.leakage import (
    CheckStatus,
    LeakageCheckResult,
    LeakageReport,
)

UTC_TS = datetime(2026, 5, 5, 12, 0, tzinfo=timezone.utc)


def prepare_evidence_tables(postgres_connection: Connection) -> None:
    Base.metadata.create_all(postgres_connection)


def make_trial_spec(trial_id: str = "trial-evidence") -> TrialSpec:
    return TrialSpec(
        trial_id=trial_id,
        family_tag="phase0",
        hypothesis="Evidence report reproducibility.",
        dataset_hash="dataset-sha",
        code_hash="code-sha",
        policy_hash="policy-sha",
        parameter_lock={"window": 12},
        registered_at=UTC_TS,
    )


def insert_trial_and_run(session: Session, *, trial_id: str = "trial-evidence") -> str:
    register_trial(session, make_trial_spec(trial_id))
    run_id = trial_id + "-run"
    session.add(
        Run(
            run_id=run_id,
            trial_id=trial_id,
            dataset_hash="dataset-sha",
            code_hash="code-sha",
            policy_hash="policy-sha",
            simbroker_version="simbroker-0.1.0",
            is_start=datetime(2026, 1, 1, tzinfo=timezone.utc),
            is_end=datetime(2026, 1, 10, tzinfo=timezone.utc),
            oos_start=datetime(2026, 1, 11, tzinfo=timezone.utc),
            oos_end=datetime(2026, 1, 20, tzinfo=timezone.utc),
            embargo_bars=1,
            leakage_status="PASS",
        )
    )
    session.flush()
    return run_id


def passing_report() -> LeakageReport:
    result = LeakageCheckResult(status=CheckStatus.PASS, description="pass")
    return LeakageReport(
        normalization_leakage=result,
        regime_label_lookahead=result,
        universe_selection_bias=result,
        within_window_optimization=result,
    )


def test_evaluation_report_contains_all_required_fields(postgres_connection: Connection) -> None:
    prepare_evidence_tables(postgres_connection)
    with Session(bind=postgres_connection) as session:
        insert_trial_and_run(session)

        report = generate_evaluation_report("trial-evidence", session=session)

    assert "trial_id: trial-evidence" in report
    assert "dataset_hash: dataset-sha" in report
    assert "code_hash: code-sha" in report
    assert "policy_hash: policy-sha" in report
    assert "is_window: 2026-01-01T00:00:00+00:00 -> 2026-01-10T00:00:00+00:00" in report
    assert "oos_window: 2026-01-11T00:00:00+00:00 -> 2026-01-20T00:00:00+00:00" in report
    assert "leakage_status: PASS" in report
    assert "net_sharpe: not_computed" in report
    assert "Phase gate approval: NOT_APPROVED" in report


def test_evaluation_report_is_reproducible(postgres_connection: Connection) -> None:
    prepare_evidence_tables(postgres_connection)
    with Session(bind=postgres_connection) as session:
        insert_trial_and_run(session)

        first = generate_evaluation_report("trial-evidence", session=session)
        second = generate_evaluation_report("trial-evidence", session=session)

    assert first == second


def test_leakage_evidence_appends_to_index(
    postgres_connection: Connection,
    tmp_path: Path,
) -> None:
    prepare_evidence_tables(postgres_connection)
    evidence_index = tmp_path / "EVIDENCE_INDEX.md"
    evidence_index.write_text("# Evidence\n", encoding="utf-8")
    with Session(bind=postgres_connection) as session:
        run_id = insert_trial_and_run(session)

        collect_leakage_evidence(
            "trial-evidence",
            session=session,
            leakage_reports={run_id: passing_report()},
            evidence_index_path=evidence_index,
            check_date="2026-05-05",
        )

    evidence_text = evidence_index.read_text(encoding="utf-8")
    assert (
        "| trial-evidence | trial-evidence-run | 2026-05-05 | PASS | PASS | PASS | PASS | PASS |"
        in evidence_text
    )


def test_leakage_evidence_raises_for_missing_report(postgres_connection: Connection) -> None:
    prepare_evidence_tables(postgres_connection)
    with Session(bind=postgres_connection) as session:
        insert_trial_and_run(session)

        with pytest.raises(EvidenceCollectionError, match="Missing LeakageReport"):
            collect_leakage_evidence(
                "trial-evidence",
                session=session,
                leakage_reports={},
            )


def test_phase0_gate_report_lists_all_tasks() -> None:
    task_results = {task_id: True for task_id in TASK_IDS}

    report = generate_phase0_gate_report(task_results=task_results)

    for task_id in TASK_IDS:
        assert f"| {task_id} | PASS |" in report
    assert "T01" in report
    assert "T24" in report
    assert "Phase gate approval: NOT_APPROVED" in report
