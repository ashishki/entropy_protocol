from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.validation.open_source_case import (
    validate_open_source_case_pack,
)


def test_case_pack_contract_requires_core_artifacts(tmp_path: Path) -> None:
    case_dir = _write_case_pack(tmp_path)
    (case_dir / "output" / "report_reviewed.md").unlink()

    result = validate_open_source_case_pack(case_dir)

    assert not result.ok
    assert _issue_codes(result) == {"missing_reviewed_report"}


def test_case_pack_contract_rejects_private_or_secret_markers(tmp_path: Path) -> None:
    case_dir = _write_case_pack(tmp_path)
    fake_token = "sk" + "-ant-test-token"
    (case_dir / "source.md").write_text(
        "\n".join(
            [
                "# Source",
                f"api_key: {fake_token}",
                "telegram_handle: @real_private_user",
                "private_account_id: live-123",
            ]
        ),
        encoding="utf-8",
    )

    result = validate_open_source_case_pack(case_dir)

    assert not result.ok
    assert {"secret_marker", "private_marker"}.issubset(_issue_codes(result))


def _write_case_pack(tmp_path: Path) -> Path:
    case_dir = tmp_path / "case_001"
    output_dir = case_dir / "output"
    output_dir.mkdir(parents=True)
    for relative_path, content in {
        "source.md": "# Source\nnot_customer_evidence: true\n",
        "policy.yaml": "schema_version: 1\n",
        "trades.csv": "timestamp,symbol,side,quantity,price,fees,account_id\n",
        "output/report.md": "# Report\n",
        "output/report_reviewed.md": "# Reviewed Report\n",
        "output/violations.json": "[]\n",
        "output/attribution_summary.json": "{}\n",
    }.items():
        (case_dir / relative_path).write_text(content, encoding="utf-8")
    manifest = {
        "artifacts": [
            {"name": "source_export", "path": str(case_dir / "trades.csv")},
            {"name": "policy_file", "path": str(case_dir / "policy.yaml")},
            {
                "name": "normalized_trades",
                "path": str(output_dir / "normalized_trades.json"),
            },
            {"name": "violations", "path": str(output_dir / "violations.json")},
            {
                "name": "attribution_summary",
                "path": str(output_dir / "attribution_summary.json"),
            },
            {"name": "report_markdown", "path": str(output_dir / "report.md")},
        ]
    }
    (output_dir / "normalized_trades.json").write_text("[]\n", encoding="utf-8")
    (output_dir / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "reproducibility_status.json").write_text(
        json.dumps(
            {
                "status": "passed",
                "baseline_content_hash": "a" * 64,
                "rerun_content_hash": "a" * 64,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return case_dir


def _issue_codes(result) -> set[str]:
    return {issue.code for issue in result.issues}
