from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.post_factum import (
    AUTO_REJECTED_FOR_PREDICTIVE_METRICS,
    POST_FACTUM_RISK,
    PostFactumCueEvidence,
    detect_post_factum_cues,
)
from signal_sandbox.auto_validation.results import ValidationStatus

SHA = "a" * 64
CREATED = datetime(2026, 5, 31, 12, tzinfo=UTC)


def test_detector_flags_pnl_closed_tp_and_retrospective_cues() -> None:
    for excerpt in (
        "PnL +12%",
        "позиция закрыта",
        "take profit hit",
        "перенес стоп в безубыток",
        "результат отработал",
    ):
        result = detect_post_factum_cues(
            _bundle(),
            cue_evidence=[_cue(excerpt, "cue-ref")],
            created_at_utc=CREATED,
        )

        assert result.status == ValidationStatus.FAILED
        assert POST_FACTUM_RISK in result.blocker_reasons
        assert "cue-ref" in result.evidence_ref_ids


def test_high_confidence_post_factum_rows_are_rejected_for_predictive_metrics() -> None:
    result = detect_post_factum_cues(
        _bundle(),
        cue_evidence=[_cue("сделка закрыта, PnL +8%", "closed-ref")],
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.FAILED
    assert result.blocker_reasons == [
        POST_FACTUM_RISK,
        AUTO_REJECTED_FOR_PREDICTIVE_METRICS,
    ]
    assert "win" not in " ".join(result.blocker_reasons)
    assert "loss" not in " ".join(result.blocker_reasons)


def test_mixed_predictive_and_post_factum_cues_return_uncertain_with_refs() -> None:
    result = detect_post_factum_cues(
        _bundle(),
        cue_evidence=[
            _cue("если будет вход выше 50", "plan-ref"),
            _cue("результат уже отработал", "result-ref"),
        ],
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "mixed_predictive_and_post_factum_cues" in result.blocker_reasons
    assert result.evidence_ref_ids == ["plan-ref", "result-ref"]


def test_low_confidence_post_factum_cues_return_uncertain_with_refs() -> None:
    result = detect_post_factum_cues(
        _bundle(),
        cue_evidence=[_cue("возможно позиция закрыта", "weak-ref", Decimal("0.40"))],
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "low_confidence_post_factum_cues" in result.blocker_reasons
    assert result.evidence_ref_ids == ["weak-ref"]


def test_detector_passes_when_no_post_factum_cues_are_present() -> None:
    result = detect_post_factum_cues(
        _bundle(),
        cue_evidence=[_cue("если будет вход выше 50", "plan-ref")],
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.PASSED


def _cue(
    excerpt: str,
    ref_id: str,
    confidence: Decimal = Decimal("0.95"),
) -> PostFactumCueEvidence:
    return PostFactumCueEvidence(
        evidence_ref_id=ref_id,
        excerpt=excerpt,
        confidence=confidence,
    )


def _bundle() -> AutoValidationEvidenceBundle:
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
            "evidence_refs": [
                EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
                EvidenceRef(
                    ref_id="direction-ref",
                    ref_type="text_span",
                    supports="direction",
                ),
                EvidenceRef(ref_id="entry-ref", ref_type="text_span", supports="entry"),
                EvidenceRef(ref_id="stop-ref", ref_type="text_span", supports="stop"),
                EvidenceRef(
                    ref_id="target-ref", ref_type="text_span", supports="target"
                ),
            ],
            "extracted_fields": {
                "asset": "MAGN",
                "direction": TradeDirection.LONG,
                "entry": Decimal("50"),
                "stop": Decimal("48"),
                "targets": [Decimal("52")],
                "evidence_ref_ids_by_field": {
                    "asset": ["asset-ref"],
                    "direction": ["direction-ref"],
                    "entry": ["entry-ref"],
                    "stop": ["stop-ref"],
                    "targets": ["target-ref"],
                },
            },
        }
    )
