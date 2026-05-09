"""Live-feed observability packet tests."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PACKET = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_OBSERVABILITY_PACKET.md"
ADAPTER = PROJECT_ROOT / "docs" / "protocols" / "LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md"


def test_observability_packet_records_required_fields() -> None:
    text = PACKET.read_text(encoding="utf-8")

    assert "Status: LIVE_FEED_OBSERVABILITY_PACKET_LOCAL_ONLY" in text
    for field in (
        "`dry_run_id`",
        "`fixture_id`",
        "`fixture_content_hash`",
        "`adapter_contract`",
        "`parser_message_count`",
        "`normalized_message_count`",
        "`parse_failure_count`",
        "`normalization_failure_count`",
        "`clock_skew_failure_count`",
        "`replay_order_failure_count`",
        "`idempotence_failure_count`",
        "`dropped_message_count`",
        "`redaction_policy_hash`",
        "`timestamp_utc`",
    ):
        assert field in text
    for counter in (
        "parse failures counted: true",
        "normalization failures counted: true",
        "clock skew failures counted: true",
        "replay order failures counted: true",
        "idempotence failures counted: true",
        "dropped messages counted: true",
        "external effect attempts counted: true",
    ):
        assert counter in text


def test_observability_packet_rejects_sensitive_and_external_effects() -> None:
    text = PACKET.read_text(encoding="utf-8")

    for false_state in (
        "credential values logged: false",
        "raw secrets logged: false",
        "raw API keys logged: false",
        "provider tokens logged: false",
        "raw holdout path logged: false",
        "holdout data logged: false",
        "orders emitted: false",
        "capital action emitted: false",
        "broker/exchange telemetry emitted: false",
        "live feed telemetry emitted: false",
        "network sockets opened: false",
        "live feed connection opened: false",
        "orders sent: false",
        "live capital active: false",
        "holdout read executed: false",
    ):
        assert false_state in text
    assert "external telemetry emission: blocked" in text


def test_observability_packet_records_limitations() -> None:
    text = PACKET.read_text(encoding="utf-8")

    assert "`docs/protocols/LIVE_FEED_ADAPTER_DRY_RUN_CONTRACT.md`" in text
    assert ADAPTER.is_file()
    assert "observability mode: local dry run" in text
    assert "log destination: local artifact only" in text
    assert "metrics destination: local artifact only" in text
    for rejected in (
        "production readiness: rejected",
        "capital-ready conclusion: rejected",
        "broker/exchange readiness: rejected",
        "OOS/performance conclusion: rejected",
        "credentialed deployment readiness: rejected",
        "holdout access: rejected",
    ):
        assert rejected in text
