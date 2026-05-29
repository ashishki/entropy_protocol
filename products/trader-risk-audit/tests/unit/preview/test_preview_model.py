from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.audit_session.artifact_bundle import (
    build_artifact_bundle_index,
    write_artifact_bundle_index,
)
from trader_risk_audit.preview import build_preview_model, render_preview_markdown
from trader_risk_audit.reporting.claim_guard import (
    REQUIRED_DISCLAIMER,
    ensure_report_claims_valid,
)


def test_preview_model_is_redacted(tmp_path: Path) -> None:
    bundle_path = _write_bundle(tmp_path)

    model = build_preview_model(bundle_path)
    rendered_model = json.dumps(model.to_dict(), sort_keys=True)
    preview_text = render_preview_markdown(model)

    assert model.source_coverage == {
        "policy_ref": "policy.yaml",
        "source_export_ref": "trades.csv",
        "trade_count": 2,
    }
    assert model.violation_count == 2
    assert [(item.rule_type, item.count) for item in model.top_rule_categories] == [
        ("forbidden_assets", 1),
        ("max_daily_loss", 1),
    ]
    assert model.unsupported_fields == ("unsupported_rules",)
    assert "private_raw_row_marker" not in rendered_model
    assert "private_raw_row_marker" not in preview_text
    assert "trade_private_row_001" not in preview_text
    assert "BTCUSD" not in preview_text


def test_preview_claim_guard(tmp_path: Path) -> None:
    bundle_path = _write_bundle(tmp_path)

    preview_text = render_preview_markdown(build_preview_model(bundle_path))

    assert REQUIRED_DISCLAIMER in preview_text
    assert "will block orders" not in preview_text
    ensure_report_claims_valid(preview_text)


def _write_bundle(tmp_path: Path) -> Path:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    (run_dir / "normalized_trades.json").write_text(
        json.dumps(
            [
                {"note": "private_raw_row_marker", "symbol": "BTCUSD"},
                {"note": "private_raw_row_marker", "symbol": "ETHUSD"},
            ]
        ),
        encoding="utf-8",
    )
    (run_dir / "violations.json").write_text(
        json.dumps(
            [
                {
                    "rule_type": "forbidden_assets",
                    "source_row_ids": ["trade_private_row_001"],
                    "symbol": "BTCUSD",
                },
                {
                    "rule_type": "max_daily_loss",
                    "source_row_ids": ["trade_private_row_002"],
                    "symbol": "ETHUSD",
                },
            ]
        ),
        encoding="utf-8",
    )
    for artifact_name in (
        "attribution_summary.json",
        "report.md",
        "telegram_packet.txt",
        "manifest.json",
    ):
        (run_dir / artifact_name).write_text(f"{artifact_name}\n", encoding="utf-8")
    (run_dir / "run_status.json").write_text(
        json.dumps(
            {
                "artifacts": {
                    "attribution_summary": "attribution_summary.json",
                    "delivery_packet": "telegram_packet.txt",
                    "manifest": "manifest.json",
                    "normalized_trades": "normalized_trades.json",
                    "report_markdown": "report.md",
                    "violations": "violations.json",
                },
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
    limitation_register = run_dir / "unsupported_rules.md"
    limitation_register.write_text(
        "manual_review_required: private limitation text\n",
        encoding="utf-8",
    )
    bundle = build_artifact_bundle_index(
        run_dir=run_dir,
        limitation_registers=(limitation_register,),
    )
    return write_artifact_bundle_index(bundle, run_dir / "bundle_index.json")
