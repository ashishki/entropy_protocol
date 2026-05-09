from __future__ import annotations

from pathlib import Path

from trader_risk_audit.artifacts.manifest import build_audit_manifest
from trader_risk_audit.storage.retention import (
    delete_manifest_artifacts,
    format_retention_list,
)


def test_retention_list_omits_raw_trade_data(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path)

    output = format_retention_list((manifest_path,))

    assert "manifest_id" in output
    assert "artifact_count" in output
    assert "2026-05-07T12:00:00+00:00" in output
    assert "report.md" in output
    assert "raw trade row secret" not in output
    assert "source,raw,values" not in output


def test_delete_dry_run_leaves_files(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path)

    result = delete_manifest_artifacts(manifest_path, dry_run=True)

    assert set(result.referenced_paths) == {
        str(path) for path in _artifact_paths(tmp_path).values()
    }
    assert result.removed_paths == ()
    assert result.missing_paths == ()
    assert all(path.exists() for path in _artifact_paths(tmp_path).values())


def test_confirmed_delete_removes_files_and_reports_missing(tmp_path: Path) -> None:
    manifest_path = _write_manifest(tmp_path)
    missing_path = _artifact_paths(tmp_path)["violations"]
    missing_path.unlink()

    result = delete_manifest_artifacts(
        manifest_path,
        dry_run=False,
        confirm_delete=True,
    )

    assert str(missing_path) in result.missing_paths
    assert str(_artifact_paths(tmp_path)["report_markdown"]) in result.removed_paths
    assert all(not path.exists() for path in _artifact_paths(tmp_path).values())


def _write_manifest(tmp_path: Path) -> Path:
    artifacts = _artifact_paths(tmp_path)
    for name, path in artifacts.items():
        path.write_text(_content_for(name), encoding="utf-8")
    manifest = build_audit_manifest(
        **artifacts,
        generated_at="2026-05-07T12:00:00+00:00",
    )
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(manifest.to_json(), encoding="utf-8")
    return manifest_path


def _artifact_paths(tmp_path: Path) -> dict[str, Path]:
    return {
        "source_export": tmp_path / "source.csv",
        "policy_file": tmp_path / "policy.yaml",
        "normalized_trades": tmp_path / "normalized.json",
        "violations": tmp_path / "violations.json",
        "attribution_summary": tmp_path / "attribution.json",
        "report_markdown": tmp_path / "report.md",
    }


def _content_for(name: str) -> str:
    if name == "source_export":
        return "raw trade row secret\nsource,raw,values\n"
    return name
