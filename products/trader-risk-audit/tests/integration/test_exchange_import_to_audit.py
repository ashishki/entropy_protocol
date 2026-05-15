from __future__ import annotations

from pathlib import Path

from trader_risk_audit.cli import main


def test_fixture_exchange_import_feeds_audit(tmp_path: Path) -> None:
    import_dir = tmp_path / "exchange_import"
    audit_dir = tmp_path / "audit"

    import_result = main(
        [
            "exchange-import",
            "fixture",
            "--snapshot",
            "tests/fixtures/exchange/bybit_execution_synthetic.json",
            "--output-dir",
            str(import_dir),
        ]
    )
    audit_result = main(
        [
            "audit",
            "--trades",
            str(import_dir / "normalized_trades.csv"),
            "--policy",
            "tests/fixtures/policies/position_asset_policy.yaml",
            "--output-dir",
            str(audit_dir),
        ]
    )

    assert import_result == 0
    assert audit_result == 0
    assert (audit_dir / "report.md").exists()
    assert (audit_dir / "manifest.json").exists()
