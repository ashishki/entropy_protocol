from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from signal_sandbox.claims import (
    ClaimDirection,
    StructuredClaimType,
    extract_structured_claims,
)
from signal_sandbox.corpus import SourceDocument

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def test_false_negative_pass_reviews_all_pending_rows_without_external_approval() -> (
    None
):
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_FALSE_NEGATIVE_PASS.json").read_text(
            encoding="utf-8"
        )
    )

    summary = artifact["summary"]
    assert artifact["status"] == "internal_false_negative_pass_external_blocked"
    assert summary["false_negative_rows_reviewed"] == 5
    assert summary["extracted_rows"] == 3
    assert summary["needs_context_rows"] == 2
    assert summary["scoreable_now_rows"] == 0
    assert summary["external_delivery_approved"] is False

    statuses = {row["pass_id"]: row["result_status"] for row in artifact["decisions"]}
    assert statuses == {
        "fn-001": "extracted",
        "fn-002": "needs_context",
        "fn-003": "needs_context",
        "fn-004": "extracted",
        "fn-005": "extracted",
    }


def test_false_negative_pass_keeps_unsupported_rows_out_of_win_loss_metrics() -> None:
    artifact = json.loads(
        (PROJECT_ROOT / "docs/pilot/three_channel_FALSE_NEGATIVE_PASS.json").read_text(
            encoding="utf-8"
        )
    )

    decisions = {row["pass_id"]: row for row in artifact["decisions"]}
    assert decisions["fn-004"]["score_policy"].startswith(
        "structured_but_not_fixed_horizon_scoreable"
    )
    assert "missing_numeric_trap_line_level" in decisions["fn-004"]["blockers"]
    assert decisions["fn-005"]["structured_claim_type"] == "trade_management"
    assert "blocked_asset_token:SIGN-UP" in decisions["fn-005"]["blockers"]
    assert decisions["fn-003"]["provider"] is None


def test_extractor_covers_false_negative_alias_and_management_patterns() -> None:
    btc_long = extract_structured_claims(
        _document(
            "зона битка 90к-95к - это возможность для лонга, а не шорта.",
            document_id="fn-001",
        )
    )[0]
    management = extract_structured_claims(
        _document("КОГДА ЗАКРОЮ ЛОНГ ПО BTC? SIGN-UP", document_id="fn-005")
    )[0]
    parser_noise = extract_structured_claims(
        _document("BTCPARSER update without market claim", document_id="noise")
    )[0]

    assert btc_long.assets == ["BTC"]
    assert btc_long.direction == ClaimDirection.LONG
    assert btc_long.claim_type == StructuredClaimType.DIRECTIONAL_THESIS
    assert management.assets == ["BTC"]
    assert management.claim_type == StructuredClaimType.TRADE_MANAGEMENT
    assert "blocked_asset_token:SIGN-UP" in management.blockers
    assert parser_noise.assets == []


def test_extractor_calibration_records_false_negative_rules() -> None:
    calibration = (
        PROJECT_ROOT / "docs/pilot/three_channel_V1_EXTRACTOR_CALIBRATION.md"
    ).read_text(encoding="utf-8")

    for required in ("cal-009", "fn-001", "fn-005", "BTCPARSER", "SIGN-UP"):
        assert required in calibration


def _document(text: str, *, document_id: str) -> SourceDocument:
    return SourceDocument(
        document_id=document_id,
        capture_id=f"capture-{document_id}",
        source_id="test_channel",
        author="test_channel",
        timestamp_utc=datetime(2026, 5, 19, tzinfo=UTC),
        text=text,
        evidence_url=f"https://t.me/test/{document_id}",
        text_sha256=hashlib.sha256(text.encode()).hexdigest(),
    )
