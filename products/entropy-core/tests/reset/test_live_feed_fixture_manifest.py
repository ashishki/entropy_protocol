"""Live-feed fixture manifest contract tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_FIXTURE_MANIFEST.md"
BOUNDARY = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_DRY_RUN_BOUNDARY.md"


def test_live_feed_fixture_manifest_records_required_fields() -> None:
    text = MANIFEST.read_text(encoding="utf-8")

    assert "Status: LIVE_FEED_FIXTURE_MANIFEST_LOCAL_ONLY" in text
    for field in (
        "`fixture_id`",
        "`fixture_version`",
        "`source_class`",
        "`instrument_universe`",
        "`time_range_utc`",
        "`schema_version`",
        "`content_hash`",
        "`schema_hash`",
        "`replay_clock_policy`",
        "`normalization_policy`",
        "`failure_fixture_class`",
    ):
        assert field in text
    for source_class in (
        "checked_in_synthetic_market_data",
        "checked_in_historical_sample_fixture",
        "generated_failure_state_fixture",
    ):
        assert source_class in text
    for binding in (
        "content hash required: true",
        "schema hash required: true",
        "normalization policy hash required: true",
        "replay clock policy hash required: true",
        "fixture mutation allowed: false",
        "unversioned fixture allowed: false",
    ):
        assert binding in text


def test_live_feed_fixture_manifest_rejects_live_effects() -> None:
    text = MANIFEST.read_text(encoding="utf-8")

    for rejected in (
        "live credential reference: rejected",
        "raw secret material: rejected",
        "live network pull: rejected",
        "live feed connection: rejected",
        "provider activation: rejected",
        "order placement: rejected",
        "broker/exchange execution: rejected",
        "live capital action: rejected",
        "production label: rejected",
        "capital-ready label: rejected",
        "holdout read: rejected",
        "holdout unlock: rejected",
    ):
        assert rejected in text
    for blocked in (
        "network access during replay: blocked",
        "live provider lookup during replay: blocked",
        "order path during replay: blocked",
        "broker/exchange path during replay: blocked",
        "external telemetry during replay: blocked",
    ):
        assert blocked in text


def test_live_feed_fixture_manifest_binds_local_scope() -> None:
    text = MANIFEST.read_text(encoding="utf-8")

    assert "`docs/protocols/LIVE_FEED_DRY_RUN_BOUNDARY.md`" in text
    assert BOUNDARY.is_file()
    assert "phase: 11 local-only live-feed dry-run readiness" in text
    for false_state in (
        "holdout path opened: false",
        "holdout read executed: false",
        "holdout unlock requested: false",
        "orders sent: false",
        "broker/exchange connection opened: false",
        "live feed connection opened: false",
        "credentials deployed: false",
        "live capital active: false",
    ):
        assert false_state in text
