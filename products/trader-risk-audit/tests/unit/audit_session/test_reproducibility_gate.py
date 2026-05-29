from __future__ import annotations

from trader_risk_audit.audit_session.reproducibility import (
    compare_manifest_payloads,
    stable_manifest_content_hash,
)


def test_reproducibility_excludes_paths_and_timestamps() -> None:
    baseline = _manifest_payload(
        generated_at="2026-05-15T08:00:00+00:00",
        output_prefix="/tmp/private/baseline",
    )
    rerun = _manifest_payload(
        generated_at="2026-05-15T09:00:00+00:00",
        output_prefix="/tmp/private/rerun",
    )

    result = compare_manifest_payloads(baseline, rerun)

    assert stable_manifest_content_hash(baseline) == stable_manifest_content_hash(rerun)
    assert result.status == "passed"
    assert result.preview_status == "ready_for_preview"
    assert result.mismatched_artifacts == ()


def _manifest_payload(*, generated_at: str, output_prefix: str) -> dict[str, object]:
    artifacts = [
        {
            "name": "normalized_trades",
            "path": f"{output_prefix}/normalized_trades.json",
            "sha256": "1" * 64,
        },
        {
            "name": "report_markdown",
            "path": f"{output_prefix}/report.md",
            "sha256": "2" * 64,
        },
    ]
    return {
        "artifacts": artifacts,
        "command": "trader-risk-audit audit-session run",
        "command_arguments": ("--output-dir", output_prefix),
        "content_hash": "ignored_by_gate",
        "generated_at": generated_at,
        "manifest_id": "ignored",
        "package_version": "0.1.0",
    }
