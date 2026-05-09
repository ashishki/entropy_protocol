from __future__ import annotations

from pathlib import Path

import pytest

from trader_risk_audit.exchange.manifest import (
    ExchangeImportArtifact,
    ExchangeImportManifest,
    ExchangeImportManifestValidationError,
    MissingExchangeImportArtifactError,
    build_exchange_import_manifest,
    validate_exchange_import_manifest,
)


def test_import_manifest_hash_is_deterministic(tmp_path: Path) -> None:
    raw_snapshot = _write(tmp_path / "raw_snapshot.json", '{"records": []}\n')
    normalized_output = _write(
        tmp_path / "normalized_trades.csv",
        "timestamp,symbol,side,quantity,price\n",
    )

    first = build_exchange_import_manifest(
        raw_snapshot=raw_snapshot,
        normalized_trades=normalized_output,
        exchange="bybit",
        market="linear",
        symbols=("BTCUSDT",),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-02T00:00:00Z",
        generated_at="2026-05-09T10:00:00+00:00",
        package_version="1.2.3",
    )
    second = build_exchange_import_manifest(
        raw_snapshot=raw_snapshot,
        normalized_trades=normalized_output,
        exchange="bybit",
        market="linear",
        symbols=("BTCUSDT",),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-02T00:00:00Z",
        generated_at="2026-05-09T11:00:00+00:00",
        package_version="1.2.3",
    )

    assert first.content_hash == second.content_hash
    assert first.manifest_id == second.manifest_id
    assert first.generated_at != second.generated_at
    assert [artifact.name for artifact in first.artifacts] == [
        "raw_snapshot",
        "normalized_trades",
    ]
    validate_exchange_import_manifest(first)


def test_import_manifest_detects_artifact_drift(tmp_path: Path) -> None:
    raw_snapshot = _write(tmp_path / "raw_snapshot.json", '{"records": []}\n')
    normalized_output = _write(
        tmp_path / "normalized_trades.csv",
        "timestamp,symbol,side,quantity,price\n",
    )
    manifest = build_exchange_import_manifest(
        raw_snapshot=raw_snapshot,
        normalized_trades=normalized_output,
        exchange="binance",
        market="spot",
        symbols=("BTCUSDT",),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-02T00:00:00Z",
        generated_at="2026-05-09T10:00:00+00:00",
        package_version="1.2.3",
    )

    validate_exchange_import_manifest(manifest)
    raw_snapshot.write_text(
        '{"records": [{"trade_id": "changed"}]}\n',
        encoding="utf-8",
    )

    with pytest.raises(ExchangeImportManifestValidationError, match="raw_snapshot"):
        validate_exchange_import_manifest(manifest)


def test_import_manifest_detects_missing_artifacts(tmp_path: Path) -> None:
    raw_snapshot = _write(tmp_path / "raw_snapshot.json", '{"records": []}\n')
    artifact = ExchangeImportArtifact(
        name="raw_snapshot",
        path=str(raw_snapshot),
        sha256="0" * 64,
    )
    manifest = ExchangeImportManifest(
        manifest_id="fixture",
        package_version="1.2.3",
        exchange="bybit",
        market="linear",
        symbols=("BTCUSDT",),
        start_time="2026-04-01T00:00:00Z",
        end_time="2026-04-02T00:00:00Z",
        generated_at="2026-05-09T10:00:00+00:00",
        artifacts=(artifact,),
        content_hash="0" * 64,
    )

    with pytest.raises(MissingExchangeImportArtifactError, match="normalized_trades"):
        validate_exchange_import_manifest(manifest)


def _write(path: Path, content: str) -> Path:
    path.write_text(content, encoding="utf-8")
    return path
