from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    ModelExtractionSpan,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.results import ValidationStatus
from signal_sandbox.auto_validation.setup_consistency import validate_setup_consistency

SHA = "a" * 64
CREATED = datetime(2026, 5, 31, 12, tzinfo=UTC)


def test_setup_validator_requires_ocr_model_or_bounding_box_level_refs() -> None:
    result = validate_setup_consistency(
        _bundle(entry_ref_type="text_span"),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "missing_ocr_or_bounding_box_level_evidence" in result.blocker_reasons


def test_setup_validator_passes_coherent_long_setup() -> None:
    result = validate_setup_consistency(_bundle(), created_at_utc=CREATED)

    assert result.status == ValidationStatus.PASSED
    assert result.blocker_reasons == []
    assert set(result.evidence_ref_ids) >= {
        "direction-ref",
        "entry-ref",
        "stop-ref",
        "target-ref",
    }


def test_setup_validator_passes_coherent_short_setup() -> None:
    result = validate_setup_consistency(
        _bundle(
            direction=TradeDirection.SHORT,
            entry=Decimal("50"),
            stop=Decimal("52"),
            targets=[Decimal("48")],
        ),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.PASSED


def test_setup_validator_fails_incoherent_level_math() -> None:
    result = validate_setup_consistency(
        _bundle(entry=Decimal("50"), stop=Decimal("51"), targets=[Decimal("52")]),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.FAILED
    assert "setup_math_inconsistent" in result.blocker_reasons


def test_setup_validator_routes_mixed_direction_to_human() -> None:
    result = validate_setup_consistency(
        _bundle(direction=TradeDirection.MIXED),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "mixed_or_unknown_trade_direction" in result.blocker_reasons


def test_setup_validator_routes_low_confidence_to_human() -> None:
    result = validate_setup_consistency(
        _bundle(model_confidence=Decimal("0.42")),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "low_confidence_level_evidence" in result.blocker_reasons


def test_setup_validator_routes_conflicting_targets_to_human() -> None:
    result = validate_setup_consistency(
        _bundle(targets=[Decimal("52"), Decimal("49")]),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "conflicting_targets" in result.blocker_reasons


def test_setup_validator_routes_missing_levels_to_human() -> None:
    result = validate_setup_consistency(
        _bundle(entry=None),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "ambiguous_or_missing_levels" in result.blocker_reasons


def _bundle(
    *,
    direction: TradeDirection = TradeDirection.LONG,
    entry: Decimal | None = Decimal("50"),
    stop: Decimal | None = Decimal("48"),
    targets: list[Decimal] | None = None,
    entry_ref_type: str = "chart_region",
    model_confidence: Decimal = Decimal("0.95"),
) -> AutoValidationEvidenceBundle:
    if targets is None:
        targets = [Decimal("52")]
    field_refs = {
        "asset": ["asset-ref"],
        "direction": ["direction-ref"],
        "stop": ["stop-ref"],
        "targets": ["target-ref"],
    }
    if entry is not None:
        field_refs["entry"] = ["entry-ref"]

    return AutoValidationEvidenceBundle.model_validate(
        {
            "candidate_id": "candidate-1",
            "source_id": "bablos79",
            "source_url": "https://t.me/s/example/1",
            "source_timestamp_utc": CREATED,
            "source_document_id": "doc-1",
            "capture_id": "capture-1",
            "source_class": SourceClass.PUBLIC,
            "text_ref_id": "text-1",
            "text_sha256": SHA,
            "media_ref_id": "media-1",
            "media_sha256": SHA,
            "chart_region_ref_ids": ["region-1"],
            "evidence_refs": [
                EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
                EvidenceRef(
                    ref_id="direction-ref",
                    ref_type="model_span",
                    supports="direction",
                ),
                EvidenceRef(
                    ref_id="entry-ref", ref_type=entry_ref_type, supports="entry"
                ),
                EvidenceRef(ref_id="stop-ref", ref_type="ocr", supports="stop"),
                EvidenceRef(ref_id="target-ref", ref_type="ocr", supports="targets"),
            ],
            "extracted_fields": {
                "asset": "MAGN",
                "direction": direction,
                "entry": entry,
                "stop": stop,
                "targets": targets,
                "evidence_ref_ids_by_field": field_refs,
            },
            "model_extraction_spans": [
                ModelExtractionSpan(
                    span_id="span-entry",
                    model_id="review-model",
                    field="entry",
                    excerpt="50",
                    evidence_ref_ids=["entry-ref"],
                    confidence=model_confidence,
                )
            ],
        }
    )
