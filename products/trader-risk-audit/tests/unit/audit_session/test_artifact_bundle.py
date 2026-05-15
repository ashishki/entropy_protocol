from __future__ import annotations

import json
from pathlib import Path

import pytest

from trader_risk_audit.audit_session.artifact_bundle import (
    BundleValidationError,
    MissingBundleArtifactError,
    build_artifact_bundle_index,
    validate_artifact_bundle_index,
    write_artifact_bundle_index,
)


def test_bundle_index_records_safe_refs(tmp_path: Path) -> None:
    run_dir = _write_complete_run(tmp_path, private_marker="raw_private_row_marker")
    limitation_register = run_dir / "unsupported_rules.md"
    limitation_register.write_text(
        "manual_review_required: unsupported leverage column\n",
        encoding="utf-8",
    )

    bundle = build_artifact_bundle_index(
        run_dir=run_dir,
        limitation_registers=(limitation_register,),
    )
    bundle_path = write_artifact_bundle_index(bundle, run_dir / "bundle_index.json")
    payload = json.loads(bundle_path.read_text(encoding="utf-8"))
    serialized = json.dumps(payload, sort_keys=True)

    assert payload["status"] == "complete"
    assert payload["input_refs"] == {
        "policy": "policy.yaml",
        "source_export": "trades.csv",
    }
    assert {artifact["name"] for artifact in payload["artifacts"]} == {
        "attribution_summary",
        "delivery_packet",
        "manifest",
        "normalized_trades",
        "report_markdown",
        "run_status",
        "violations",
    }
    assert payload["limitation_registers"][0]["ref"] == "unsupported_rules.md"
    assert payload["preview_state"] == {"ref": None, "status": "not_generated"}
    assert str(tmp_path) not in serialized
    assert "raw_private_row_marker" not in serialized


def test_bundle_validation_catches_drift(tmp_path: Path) -> None:
    run_dir = _write_complete_run(tmp_path, private_marker="private")
    bundle = build_artifact_bundle_index(run_dir=run_dir)
    bundle_path = write_artifact_bundle_index(bundle, run_dir / "bundle_index.json")

    (run_dir / "report.md").write_text("changed report\n", encoding="utf-8")
    with pytest.raises(BundleValidationError, match="report_markdown"):
        validate_artifact_bundle_index(bundle_path)

    (run_dir / "report.md").unlink()
    with pytest.raises(MissingBundleArtifactError, match="report_markdown"):
        validate_artifact_bundle_index(bundle_path)


def _write_complete_run(tmp_path: Path, *, private_marker: str) -> Path:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    artifacts = {
        "normalized_trades": "normalized_trades.json",
        "violations": "violations.json",
        "attribution_summary": "attribution_summary.json",
        "report_markdown": "report.md",
        "delivery_packet": "telegram_packet.txt",
        "manifest": "manifest.json",
    }
    for name, ref in artifacts.items():
        content = f"{name}\n"
        if name == "normalized_trades":
            content = f"{private_marker}\n"
        (run_dir / ref).write_text(content, encoding="utf-8")
    (run_dir / "run_status.json").write_text(
        json.dumps(
            {
                "artifacts": artifacts,
                "intake_session_id": "intake_test",
                "policy_ref": "policy.yaml",
                "reason_code": None,
                "source_export_ref": "trades.csv",
                "status": "complete",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return run_dir
