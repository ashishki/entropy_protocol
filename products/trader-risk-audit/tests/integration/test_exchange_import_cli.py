from __future__ import annotations

import json
from pathlib import Path

from trader_risk_audit.cli import main


def test_fixture_exchange_import_writes_expected_artifacts(tmp_path: Path) -> None:
    output_dir = tmp_path / "exchange_import"

    result = main(
        [
            "exchange-import",
            "fixture",
            "--snapshot",
            "tests/fixtures/exchange/bybit_execution_synthetic.json",
            "--output-dir",
            str(output_dir),
        ]
    )

    assert result == 0
    assert {path.name for path in output_dir.iterdir()} == {
        "import_manifest.json",
        "normalized_trades.csv",
        "raw_snapshot.json",
    }
    raw_snapshot = json.loads(
        (output_dir / "raw_snapshot.json").read_text(encoding="utf-8")
    )
    manifest = json.loads(
        (output_dir / "import_manifest.json").read_text(encoding="utf-8")
    )
    artifacts = {artifact["name"]: artifact for artifact in manifest["artifacts"]}

    assert raw_snapshot["exchange"] == "bybit"
    assert raw_snapshot["market"] == "linear"
    assert raw_snapshot["symbols"] == ["BTCUSDT"]
    assert set(artifacts) == {"raw_snapshot", "normalized_trades"}
    assert artifacts["raw_snapshot"]["sha256"]
    assert artifacts["normalized_trades"]["sha256"]


def test_fixture_exchange_import_is_deterministic(tmp_path: Path) -> None:
    first_output = tmp_path / "first"
    second_output = tmp_path / "second"

    first_result = _run_fixture_import(first_output)
    second_result = _run_fixture_import(second_output)

    first_manifest = json.loads(
        (first_output / "import_manifest.json").read_text(encoding="utf-8")
    )
    second_manifest = json.loads(
        (second_output / "import_manifest.json").read_text(encoding="utf-8")
    )

    assert first_result == 0
    assert second_result == 0
    assert (first_output / "normalized_trades.csv").read_text(encoding="utf-8") == (
        second_output / "normalized_trades.csv"
    ).read_text(encoding="utf-8")
    assert first_manifest["content_hash"] == second_manifest["content_hash"]


def _run_fixture_import(output_dir: Path) -> int:
    return main(
        [
            "exchange-import",
            "fixture",
            "--snapshot",
            "tests/fixtures/exchange/binance_my_trades_synthetic.json",
            "--output-dir",
            str(output_dir),
        ]
    )
