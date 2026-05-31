"""Asset proxy/provider eligibility validator."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from decimal import Decimal

from signal_sandbox.assets.registry import (
    AssetRegistry,
    ResolutionStatus,
    normalize_alias,
    seed_asset_registry,
)
from signal_sandbox.auto_validation.evidence import AutoValidationEvidenceBundle
from signal_sandbox.auto_validation.results import ValidationResult, ValidationStatus
from signal_sandbox.claims.provider_config import (
    ProviderProxyConfig,
    ProviderProxyStatus,
    default_provider_proxy_config,
)

PROVIDER_VALIDATOR_ID = "provider_eligibility"
PROVIDER_VALIDATOR_VERSION = "provider_eligibility.v1"


def validate_provider_eligibility(
    bundle: AutoValidationEvidenceBundle | None,
    *,
    registry: AssetRegistry | None = None,
    provider_config: ProviderProxyConfig | None = None,
    created_at_utc: datetime | None = None,
) -> ValidationResult:
    """Validate that asset alias resolves to an approved compact provider path."""

    if bundle is None or bundle.extracted_fields.asset is None:
        return _uncertain_result(
            candidate_id="unknown" if bundle is None else bundle.candidate_id,
            evidence_ref_ids=["missing-asset-ref"],
            blocker_reasons=["missing_asset_for_provider_resolution"],
            deterministic_input_sha256=_input_sha256(None, None),
            created_at_utc=created_at_utc,
        )

    asset_ref_ids = bundle.extracted_fields.evidence_ref_ids_by_field.get("asset", [])
    if not asset_ref_ids:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=["missing-asset-ref"],
            blocker_reasons=["missing_asset_evidence_ref"],
            deterministic_input_sha256=_input_sha256(bundle, None),
            created_at_utc=created_at_utc,
        )

    asset_registry = registry or seed_asset_registry()
    config = provider_config or default_provider_proxy_config()
    asset_query = bundle.extracted_fields.asset
    resolution = asset_registry.resolve_alias(
        asset_query,
        evidence="auto-validation extracted asset field",
    )

    if resolution.status == ResolutionStatus.AMBIGUOUS:
        return _uncertain_result(
            candidate_id=bundle.candidate_id,
            evidence_ref_ids=asset_ref_ids,
            blocker_reasons=["ambiguous_asset_alias"],
            deterministic_input_sha256=_input_sha256(
                bundle, resolution.normalized_query
            ),
            created_at_utc=created_at_utc,
        )

    if resolution.status == ResolutionStatus.UNRESOLVED:
        fallback_rule = config.resolve(asset_query)
        if fallback_rule.status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT:
            return _excluded_provider_gap(
                bundle=bundle,
                evidence_ref_ids=asset_ref_ids,
                blocker_reasons=["provider_proxy_needs_operator_input"],
                provider_ref=_compact_provider_ref(
                    fallback_rule.provider, fallback_rule.provider_symbol
                ),
                created_at_utc=created_at_utc,
            )
        return _excluded_provider_gap(
            bundle=bundle,
            evidence_ref_ids=asset_ref_ids,
            blocker_reasons=["unresolved_asset_alias"],
            provider_ref=None,
            created_at_utc=created_at_utc,
        )

    asset = resolution.matches[0]
    rule = config.resolve(asset.display_symbol)
    provider_ref = _compact_provider_ref(rule.provider, rule.provider_symbol)

    if rule.status == ProviderProxyStatus.NEEDS_OPERATOR_INPUT:
        return _excluded_provider_gap(
            bundle=bundle,
            evidence_ref_ids=asset_ref_ids,
            blocker_reasons=["provider_proxy_needs_operator_input"],
            provider_ref=provider_ref,
            created_at_utc=created_at_utc,
        )

    if rule.status == ProviderProxyStatus.UNSUPPORTED or not provider_ref:
        return _excluded_provider_gap(
            bundle=bundle,
            evidence_ref_ids=asset_ref_ids,
            blocker_reasons=["no_approved_provider_proxy"],
            provider_ref=provider_ref,
            created_at_utc=created_at_utc,
        )

    return ValidationResult(
        validator_id=PROVIDER_VALIDATOR_ID,
        validator_version=PROVIDER_VALIDATOR_VERSION,
        candidate_id=bundle.candidate_id,
        status=ValidationStatus.PASSED,
        confidence=Decimal("1"),
        evidence_ref_ids=sorted({*asset_ref_ids, provider_ref}),
        blocker_reasons=[],
        deterministic_input_sha256=_input_sha256(bundle, provider_ref),
        rationale="asset alias resolves to an approved compact provider/proxy ref",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _uncertain_result(
    *,
    candidate_id: str,
    evidence_ref_ids: list[str],
    blocker_reasons: list[str],
    deterministic_input_sha256: str,
    created_at_utc: datetime | None,
) -> ValidationResult:
    return ValidationResult(
        validator_id=PROVIDER_VALIDATOR_ID,
        validator_version=PROVIDER_VALIDATOR_VERSION,
        candidate_id=candidate_id,
        status=ValidationStatus.UNCERTAIN_NEEDS_HUMAN,
        confidence=Decimal("0"),
        evidence_ref_ids=evidence_ref_ids,
        blocker_reasons=blocker_reasons,
        deterministic_input_sha256=deterministic_input_sha256,
        rationale="asset/provider mapping cannot be proven automatically",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _excluded_provider_gap(
    *,
    bundle: AutoValidationEvidenceBundle,
    evidence_ref_ids: list[str],
    blocker_reasons: list[str],
    provider_ref: str | None,
    created_at_utc: datetime | None,
) -> ValidationResult:
    refs = sorted(
        {*evidence_ref_ids, *(set() if provider_ref is None else {provider_ref})}
    )
    return ValidationResult(
        validator_id=PROVIDER_VALIDATOR_ID,
        validator_version=PROVIDER_VALIDATOR_VERSION,
        candidate_id=bundle.candidate_id,
        status=ValidationStatus.EXCLUDED_PROVIDER_GAP,
        confidence=Decimal("1"),
        evidence_ref_ids=refs,
        blocker_reasons=blocker_reasons,
        deterministic_input_sha256=_input_sha256(bundle, provider_ref),
        rationale="asset evidence exists but approved provider/proxy path is absent",
        created_at_utc=created_at_utc or datetime.now(UTC),
    )


def _compact_provider_ref(
    provider: str | None, provider_symbol: str | None
) -> str | None:
    if provider is None or provider_symbol is None:
        return None
    normalized_provider = normalize_alias(provider)
    normalized_symbol = normalize_alias(provider_symbol).replace("/", "")
    return f"provider_proxy:{normalized_provider}:{normalized_symbol}"


def _input_sha256(
    bundle: AutoValidationEvidenceBundle | None,
    provider_ref_or_alias: str | None,
) -> str:
    payload = {
        "bundle_sha256": bundle.bundle_sha256() if bundle is not None else None,
        "provider_ref_or_alias": provider_ref_or_alias,
        "validator_id": PROVIDER_VALIDATOR_ID,
        "validator_version": PROVIDER_VALIDATOR_VERSION,
    }
    canonical = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
