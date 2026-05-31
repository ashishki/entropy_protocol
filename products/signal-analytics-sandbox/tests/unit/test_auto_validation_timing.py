from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    MarketWindowRef,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.results import ValidationStatus
from signal_sandbox.auto_validation.timing import (
    FAILED_POST_FACTUM_OR_LATE,
    TimingOutcomeEvidence,
    TimingOutcomeKind,
    validate_pre_outcome_timing,
)

SHA = "a" * 64
MARKET_SHA = "b" * 64
CREATED = datetime(2026, 5, 31, 12, tzinfo=UTC)


def test_timing_validator_passes_when_source_precedes_outcome_evidence() -> None:
    bundle = _bundle(source_timestamp=CREATED)
    result = validate_pre_outcome_timing(
        bundle,
        outcome_evidence=[
            _outcome(observed_at=CREATED + timedelta(hours=2)),
        ],
        approved_providers={"moex"},
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.PASSED
    assert result.confidence == Decimal("1")
    assert "source-ts-ref" in result.evidence_ref_ids
    assert "market-window-1" in result.evidence_ref_ids
    assert "outcome-ref" in result.evidence_ref_ids


def test_timing_validator_fails_when_outcome_was_reached_before_source() -> None:
    bundle = _bundle(source_timestamp=CREATED)
    result = validate_pre_outcome_timing(
        bundle,
        outcome_evidence=[
            _outcome(observed_at=CREATED - timedelta(minutes=5)),
        ],
        approved_providers={"moex"},
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.FAILED
    assert result.blocker_reasons == [FAILED_POST_FACTUM_OR_LATE]


def test_timing_validator_routes_missing_market_data_to_human() -> None:
    result = validate_pre_outcome_timing(
        _bundle(source_timestamp=CREATED, market_windows=[]),
        outcome_evidence=[],
        approved_providers={"moex"},
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "missing_market_data" in result.blocker_reasons


def test_timing_validator_routes_unsupported_provider_to_human() -> None:
    result = validate_pre_outcome_timing(
        _bundle(source_timestamp=CREATED, provider="unsupported"),
        outcome_evidence=[_outcome(observed_at=CREATED + timedelta(hours=1))],
        approved_providers={"moex"},
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "unsupported_provider_or_market_window" in result.blocker_reasons


def test_timing_validator_routes_missing_source_timestamp_ref_to_human() -> None:
    result = validate_pre_outcome_timing(
        _bundle(source_timestamp=CREATED, include_source_timestamp_ref=False),
        outcome_evidence=[_outcome(observed_at=CREATED + timedelta(hours=1))],
        approved_providers={"moex"},
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "missing_source_timestamp_evidence_ref" in result.blocker_reasons


def test_timing_validator_routes_missing_bundle_to_human() -> None:
    result = validate_pre_outcome_timing(
        None,
        outcome_evidence=[],
        approved_providers={"moex"},
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "missing_evidence_bundle_or_source_timestamp" in result.blocker_reasons


def _outcome(observed_at: datetime) -> TimingOutcomeEvidence:
    return TimingOutcomeEvidence(
        market_window_ref_id="market-window-1",
        evidence_ref_id="outcome-ref",
        outcome_kind=TimingOutcomeKind.TARGET_TOUCH,
        observed_at_utc=observed_at,
    )


def _bundle(
    *,
    source_timestamp: datetime,
    provider: str = "moex",
    market_windows: list[MarketWindowRef] | None = None,
    include_source_timestamp_ref: bool = True,
) -> AutoValidationEvidenceBundle:
    evidence_refs = [
        EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
        EvidenceRef(ref_id="direction-ref", ref_type="text_span", supports="direction"),
        EvidenceRef(ref_id="entry-ref", ref_type="chart_region", supports="entry"),
        EvidenceRef(ref_id="stop-ref", ref_type="chart_region", supports="stop"),
        EvidenceRef(ref_id="target-ref", ref_type="chart_region", supports="targets"),
        EvidenceRef(
            ref_id="outcome-ref",
            ref_type="market_window",
            supports="target_touch",
        ),
    ]
    if include_source_timestamp_ref:
        evidence_refs.append(
            EvidenceRef(
                ref_id="source-ts-ref",
                ref_type="source_document",
                supports="source_timestamp",
            )
        )

    return AutoValidationEvidenceBundle.model_validate(
        {
            "candidate_id": "candidate-1",
            "source_id": "bablos79",
            "source_url": "https://t.me/s/example/1",
            "source_timestamp_utc": source_timestamp,
            "source_document_id": "doc-1",
            "capture_id": "capture-1",
            "source_class": SourceClass.PUBLIC,
            "text_ref_id": "text-1",
            "text_sha256": SHA,
            "media_ref_id": "media-1",
            "media_sha256": SHA,
            "chart_region_ref_ids": ["region-1"],
            "evidence_refs": evidence_refs,
            "extracted_fields": {
                "asset": "MAGN",
                "direction": TradeDirection.LONG,
                "entry": Decimal("50.10"),
                "stop": Decimal("48.90"),
                "targets": [Decimal("52.40")],
                "evidence_ref_ids_by_field": {
                    "asset": ["asset-ref"],
                    "direction": ["direction-ref"],
                    "entry": ["entry-ref"],
                    "stop": ["stop-ref"],
                    "targets": ["target-ref"],
                },
            },
            "market_window_refs": (
                [
                    MarketWindowRef(
                        ref_id="market-window-1",
                        provider=provider,
                        symbol="MAGN",
                        window_start_utc=source_timestamp,
                        window_end_utc=source_timestamp + timedelta(hours=4),
                        data_sha256=MARKET_SHA,
                    )
                ]
                if market_windows is None
                else market_windows
            ),
        }
    )
