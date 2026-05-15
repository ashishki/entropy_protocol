from __future__ import annotations

import json
import shutil
from pathlib import Path

from trader_risk_audit.audit_session.reproducibility import run_reproducibility_gate
from trader_risk_audit.audit_session.runner import run_audit_session


def test_reproducibility_gate_matches_hash(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    baseline_dir = tmp_path / "baseline"
    rerun_dir = tmp_path / "rerun"
    session_path = _write_session(input_dir)

    run_audit_session(
        session_path=session_path,
        policy_path="tests/fixtures/policies/position_asset_policy.yaml",
        input_dir=input_dir,
        output_dir=baseline_dir,
    )

    result = run_reproducibility_gate(
        session_path=session_path,
        policy_path="tests/fixtures/policies/position_asset_policy.yaml",
        input_dir=input_dir,
        baseline_run_dir=baseline_dir,
        rerun_dir=rerun_dir,
    )

    status = json.loads(
        (baseline_dir / "reproducibility_status.json").read_text(encoding="utf-8")
    )
    assert result.status == "passed"
    assert result.baseline_content_hash == result.rerun_content_hash
    assert result.preview_status == "ready_for_preview"
    assert status["status"] == "passed"
    assert status["artifact_refs"]["baseline_manifest"] == "manifest.json"
    assert status["artifact_refs"]["rerun_manifest"] == "rerun/manifest.json"


def test_reproducibility_mismatch_blocks_preview(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    baseline_dir = tmp_path / "baseline"
    rerun_dir = tmp_path / "rerun"
    session_path = _write_session(input_dir)

    run_audit_session(
        session_path=session_path,
        policy_path="tests/fixtures/policies/position_asset_policy.yaml",
        input_dir=input_dir,
        output_dir=baseline_dir,
    )
    _rewrite_report_hash(baseline_dir / "manifest.json", "f" * 64)

    result = run_reproducibility_gate(
        session_path=session_path,
        policy_path="tests/fixtures/policies/position_asset_policy.yaml",
        input_dir=input_dir,
        baseline_run_dir=baseline_dir,
        rerun_dir=rerun_dir,
    )

    status = json.loads(
        (baseline_dir / "reproducibility_status.json").read_text(encoding="utf-8")
    )
    assert result.status == "blocked"
    assert result.preview_status == "blocked_reproducibility"
    assert result.reason_code == "content_hash_mismatch"
    assert result.baseline_content_hash != result.rerun_content_hash
    assert "report_markdown" in result.mismatched_artifacts
    assert status["artifact_refs"] == {
        "baseline_manifest": "manifest.json",
        "rerun_manifest": "rerun/manifest.json",
    }


def _write_session(input_dir: Path) -> Path:
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(
        "tests/fixtures/trades/attribution_overlap.csv",
        input_dir / "trades.csv",
    )
    session_path = input_dir / "intake_session.json"
    session_path.write_text(
        json.dumps(
            {
                "file_references": {
                    "source_export": "trades.csv",
                },
                "policy_ref": "policy.yaml",
                "source_export_ref": "trades.csv",
                "status": "ready_for_audit",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return session_path


def _rewrite_report_hash(manifest_path: Path, replacement: str) -> None:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for artifact in manifest["artifacts"]:
        if artifact["name"] == "report_markdown":
            artifact["sha256"] = replacement
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
