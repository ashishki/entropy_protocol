from __future__ import annotations

from datetime import UTC, datetime

from signal_sandbox.runs import (
    ProviderRunRef,
    RunArtifactRef,
    build_compact_cache_ref,
    build_report_run_manifest,
)


def test_report_run_manifest_is_deterministic_and_records_refs() -> None:
    first = build_report_run_manifest(
        run_id="run-three-channel-v2",
        created_at_utc=datetime(2026, 5, 19, tzinfo=UTC),
        code_version="test-version",
        input_refs=[_artifact("metrics", "b" * 64), _artifact("scorecard", "a" * 64)],
        provider_refs=[_provider("binance", "BTCUSDT", "c" * 64)],
        output_refs=[_artifact("report", "d" * 64)],
    )
    second = build_report_run_manifest(
        run_id="run-three-channel-v2",
        created_at_utc=datetime(2026, 5, 19, tzinfo=UTC),
        code_version="test-version",
        input_refs=[_artifact("scorecard", "a" * 64), _artifact("metrics", "b" * 64)],
        provider_refs=[_provider("binance", "BTCUSDT", "c" * 64)],
        output_refs=[_artifact("report", "d" * 64)],
    )

    assert first.canonical_json_bytes() == second.canonical_json_bytes()
    assert first.manifest_sha256() == second.manifest_sha256()
    assert [item.name for item in first.input_refs] == ["metrics", "scorecard"]
    assert first.provider_refs[0].provider == "binance"
    assert first.output_refs[0].name == "report"


def test_run_manifest_builds_compact_cache_refs() -> None:
    ref = build_compact_cache_ref("input", "metrics", "a" * 64)

    assert ref.ref_id == "input:metrics:aaaaaaaaaaaa"
    assert ref.source_kind == "input"
    assert ref.source_name == "metrics"
    assert ref.source_sha256 == "a" * 64


def _artifact(name: str, sha256: str) -> RunArtifactRef:
    return RunArtifactRef(
        name=name,
        path=f"docs/pilot/{name}.json",
        sha256=sha256,
        version="v2",
    )


def _provider(provider: str, symbol: str, sha256: str) -> ProviderRunRef:
    return ProviderRunRef(
        provider=provider,
        symbol=symbol,
        snapshot_id=f"{provider}-{symbol}-snapshot",
        data_sha256=sha256,
    )
