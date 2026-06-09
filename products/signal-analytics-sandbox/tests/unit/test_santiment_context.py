from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from signal_sandbox.auto_validation.evidence import (
    AutoValidationEvidenceBundle,
    EvidenceRef,
    ExtractedSetupFields,
    SourceClass,
    TradeDirection,
)
from signal_sandbox.santiment import (
    SantimentContextArtifact,
    SantimentContextFeature,
    build_santiment_context_artifact,
    export_santiment_context_artifact,
    load_santiment_context_artifact,
)

SHA = "a" * 64
POSTED = datetime(2026, 5, 31, 12, tzinfo=UTC)


class FakeSantimentProvider:
    provider_id: str = "fake_santiment"

    def fetch_metric_timeseries(
        self,
        *,
        metric: str,
        slug: str,
        start_utc: datetime,
        end_utc: datetime,
        interval: str,
    ) -> list[dict[str, Any]]:
        assert slug == "bitcoin"
        assert interval == "1d"
        assert start_utc < POSTED < end_utc
        base = Decimal("100") if metric != "sentiment_weighted_total" else Decimal("1")
        return [
            {"datetime": "2026-05-30T12:00:00Z", "value": str(base)},
            {"datetime": "2026-06-01T12:00:00Z", "value": str(base + Decimal("25"))},
        ]


def test_build_santiment_context_artifact_computes_post_vs_pre_features() -> None:
    artifact = build_santiment_context_artifact(
        bundle=_bundle(),
        provider=FakeSantimentProvider(),
        metrics=("price_usd", "social_volume_total"),
        generated_at_utc=POSTED,
    )

    assert artifact.artifact_type == "santiment_context"
    assert artifact.candidate_id == "candidate-1"
    assert artifact.asset == "BTC"
    assert artifact.santiment_slug == "bitcoin"
    assert artifact.evidence_bundle_sha256 == _bundle().bundle_sha256()
    assert {series.metric for series in artifact.metric_series} == {
        "price_usd",
        "social_volume_total",
    }
    price_feature = _feature(artifact, "price_usd")
    assert price_feature.pre_window_value == Decimal("100")
    assert price_feature.post_window_value == Decimal("125")
    assert price_feature.delta_post_vs_pre == Decimal("25")
    assert price_feature.pct_change_post_vs_pre == Decimal("25.00")
    assert price_feature.interpretation == "up_price_context_after_post"
    assert len(artifact.artifact_sha256()) == 64


def test_export_santiment_context_writes_json_and_markdown(tmp_path: Path) -> None:
    artifact = build_santiment_context_artifact(
        bundle=_bundle(),
        provider=FakeSantimentProvider(),
        metrics=("social_volume_total",),
        generated_at_utc=POSTED,
    )

    export = export_santiment_context_artifact(artifact, output_dir=tmp_path)
    loaded = load_santiment_context_artifact(export.json_path)
    markdown = export.markdown_path.read_text(encoding="utf-8")

    assert export.json_path == tmp_path / "candidate-1.santiment_context.json"
    assert export.markdown_path == tmp_path / "candidate-1.santiment_context.md"
    assert json.loads(export.json_path.read_text(encoding="utf-8"))["candidate_id"]
    assert loaded.artifact_sha256() == export.artifact_sha256
    assert "social_volume_total" in markdown
    assert "santiment:bitcoin:social_volume_total" in markdown


def test_santiment_context_rejects_assets_without_slug_mapping() -> None:
    with pytest.raises(ValueError, match="no Santiment slug mapping"):
        build_santiment_context_artifact(
            bundle=_bundle(asset="MAGN"),
            provider=FakeSantimentProvider(),
            metrics=("price_usd",),
            generated_at_utc=POSTED,
        )


def _feature(
    artifact: SantimentContextArtifact, metric: str
) -> SantimentContextFeature:
    return next(feature for feature in artifact.features if feature.metric == metric)


def _bundle(asset: str = "BTC") -> AutoValidationEvidenceBundle:
    return AutoValidationEvidenceBundle(
        candidate_id="candidate-1",
        source_id="bablos79",
        source_url="https://t.me/bablos79/10450",
        source_timestamp_utc=POSTED,
        source_document_id="doc-1",
        capture_id="capture-1",
        source_class=SourceClass.PUBLIC,
        text_ref_id="text-1",
        text_sha256=SHA,
        evidence_refs=[
            EvidenceRef(ref_id="asset-ref", ref_type="text_span", supports="asset"),
            EvidenceRef(
                ref_id="direction-ref",
                ref_type="text_span",
                supports="direction",
            ),
        ],
        extracted_fields=ExtractedSetupFields(
            asset=asset,
            direction=TradeDirection.LONG,
            evidence_ref_ids_by_field={
                "asset": ["asset-ref"],
                "direction": ["direction-ref"],
            },
        ),
    )
