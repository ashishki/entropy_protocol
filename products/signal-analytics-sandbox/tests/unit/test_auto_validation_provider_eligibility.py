from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.assets.registry import (
    Asset,
    AssetRegistry,
    InstrumentType,
)
from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.auto_validation.provider_eligibility import (
    validate_provider_eligibility,
)
from signal_sandbox.auto_validation.results import ValidationStatus
from signal_sandbox.claims.provider_config import (
    ProviderProxyConfig,
    ProviderProxyRule,
    ProviderProxyStatus,
)

SHA = "a" * 64
CREATED = datetime(2026, 5, 31, 12, tzinfo=UTC)


def test_provider_validator_maps_asset_alias_to_approved_provider_ref() -> None:
    result = validate_provider_eligibility(_bundle("MAGN"), created_at_utc=CREATED)

    assert result.status == ValidationStatus.PASSED
    assert "asset-ref" in result.evidence_ref_ids
    assert "provider_proxy:MOEX_ISS:MAGN" in result.evidence_ref_ids
    assert not any("history" in ref for ref in result.evidence_ref_ids)


def test_provider_validator_routes_ambiguous_alias_to_human() -> None:
    result = validate_provider_eligibility(
        _bundle("ABC"),
        registry=_ambiguous_registry(),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "ambiguous_asset_alias" in result.blocker_reasons


def test_provider_validator_excludes_unresolved_alias_as_provider_gap() -> None:
    result = validate_provider_eligibility(_bundle("UNKNOWN"), created_at_utc=CREATED)

    assert result.status == ValidationStatus.EXCLUDED_PROVIDER_GAP
    assert "unresolved_asset_alias" in result.blocker_reasons


def test_provider_validator_excludes_unapproved_proxy_semantics() -> None:
    result = validate_provider_eligibility(_bundle("BR"), created_at_utc=CREATED)

    assert result.status == ValidationStatus.EXCLUDED_PROVIDER_GAP
    assert "provider_proxy_needs_operator_input" in result.blocker_reasons


def test_provider_validator_excludes_unsupported_market_rule() -> None:
    result = validate_provider_eligibility(
        _bundle("MAGN"),
        provider_config=ProviderProxyConfig(
            rules={
                "MAGN": ProviderProxyRule(
                    symbol="MAGN",
                    asset_class="moex_share",
                    status=ProviderProxyStatus.UNSUPPORTED,
                    rationale="quote scale not approved",
                )
            }
        ),
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.EXCLUDED_PROVIDER_GAP
    assert "no_approved_provider_proxy" in result.blocker_reasons


def test_provider_validator_routes_missing_bundle_to_human() -> None:
    result = validate_provider_eligibility(
        None,
        created_at_utc=CREATED,
    )

    assert result.status == ValidationStatus.UNCERTAIN_NEEDS_HUMAN
    assert "missing_asset_for_provider_resolution" in result.blocker_reasons


def _bundle(
    asset: str,
    *,
    include_asset_ref: bool = True,
) -> AutoValidationEvidenceBundle:
    field_refs = {
        "direction": ["direction-ref"],
        "entry": ["entry-ref"],
        "stop": ["stop-ref"],
        "targets": ["target-ref"],
    }
    if include_asset_ref:
        field_refs["asset"] = ["asset-ref"]

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
            "evidence_refs": [
                EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
                EvidenceRef(
                    ref_id="direction-ref",
                    ref_type="text_span",
                    supports="direction",
                ),
                EvidenceRef(
                    ref_id="entry-ref", ref_type="chart_region", supports="entry"
                ),
                EvidenceRef(
                    ref_id="stop-ref", ref_type="chart_region", supports="stop"
                ),
                EvidenceRef(
                    ref_id="target-ref",
                    ref_type="chart_region",
                    supports="targets",
                ),
            ],
            "extracted_fields": {
                "asset": asset,
                "direction": TradeDirection.LONG,
                "entry": Decimal("50"),
                "stop": Decimal("48"),
                "targets": [Decimal("52")],
                "evidence_ref_ids_by_field": field_refs,
            },
        }
    )


def _ambiguous_registry() -> AssetRegistry:
    return AssetRegistry(
        assets=[
            Asset(
                canonical_id="US:ABC",
                instrument_type=InstrumentType.EQUITY,
                display_symbol="ABC",
                aliases=["ABC"],
                provenance="test",
            ),
            Asset(
                canonical_id="MOEX:ABC",
                instrument_type=InstrumentType.EQUITY,
                display_symbol="ABC",
                aliases=["ABC"],
                provenance="test",
            ),
        ]
    )
