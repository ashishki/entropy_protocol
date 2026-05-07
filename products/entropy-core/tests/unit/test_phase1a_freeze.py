from __future__ import annotations

import json

import pytest

from entropy.evidence.phase1a_freeze import (
    PHASE1A_ALLOWED_SYMBOLS,
    build_phase1a_archive_freeze_manifest,
)


def test_build_phase1a_archive_freeze_manifest_writes_boundary(tmp_path) -> None:
    manifest_paths = []
    for symbol in PHASE1A_ALLOWED_SYMBOLS:
        manifest_paths.append(_write_conversion_manifest(tmp_path, symbol=symbol))
    stability_path = _write_stability_manifest(tmp_path)

    result = build_phase1a_archive_freeze_manifest(
        conversion_manifest_paths=manifest_paths,
        archive_stability_manifest_path=stability_path,
        output_dir=tmp_path / "freeze",
        contract_path=tmp_path / "contract.md",
    )

    assert result.archive_only is True
    assert result.gate_claim_allowed is False
    assert result.dataset_count == 15
    assert result.symbol_count == 15
    assert len(result.manifest_hash) == 64
    payload = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert payload["split_policy"]["archive_holdout"]["read_restriction"] == (
        "forbidden_before_registration_boundary"
    )
    assert "OOS performance" in payload["forbidden_report_labels"]
    assert payload["boundary"] == "manifest_only_no_strategy_no_portfolio_no_performance_claim"
    assert "does not implement strategies" in result.summary_path.read_text(encoding="utf-8")


def test_build_phase1a_archive_freeze_manifest_rejects_wrong_window(tmp_path) -> None:
    manifest_paths = []
    for symbol in PHASE1A_ALLOWED_SYMBOLS:
        window_end = "2024-12-31T00:00:00+00:00" if symbol == "BTCUSDT" else None
        manifest_paths.append(
            _write_conversion_manifest(tmp_path, symbol=symbol, window_end=window_end)
        )
    stability_path = _write_stability_manifest(tmp_path)

    with pytest.raises(ValueError, match="2020-01-01..2025-12-31"):
        build_phase1a_archive_freeze_manifest(
            conversion_manifest_paths=manifest_paths,
            archive_stability_manifest_path=stability_path,
            output_dir=tmp_path / "freeze",
            contract_path=tmp_path / "contract.md",
        )


def _write_conversion_manifest(tmp_path, *, symbol: str, window_end: str | None = None):
    manifest_path = tmp_path / f"{symbol}_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "symbol": symbol,
                "interval": "1d",
                "first_bar_ts": "2020-01-01T00:00:00+00:00",
                "last_bar_ts": window_end or "2025-12-31T00:00:00+00:00",
                "daily_bars": 2192,
                "dataset_hash": f"{symbol}_dataset_hash",
                "combined_source_sha256": f"{symbol}_source_hash",
                "data_quality_status": "PASS",
                "parquet_path": f"/tmp/{symbol}.parquet",
            }
        ),
        encoding="utf-8",
    )
    return manifest_path


def _write_stability_manifest(tmp_path):
    manifest_path = tmp_path / "stability_manifest.json"
    manifest_path.write_text(
        json.dumps(
            {
                "archive_only": True,
                "gate_claim_allowed": False,
                "source_manifest_count": 15,
                "row_count": 32880,
                "monitored_day_count": 2192,
                "missing_symbol_days": 0,
                "unexplained_gap_count": 0,
                "packet_status": "PACKET_READY_FOR_REVIEW",
                "packet_id": "DATA-STABILITY-ARCHIVE-90D-v1",
                "symbols": list(PHASE1A_ALLOWED_SYMBOLS),
            }
        ),
        encoding="utf-8",
    )
    return manifest_path
