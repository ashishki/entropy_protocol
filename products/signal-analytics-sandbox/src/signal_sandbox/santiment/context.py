"""Santiment SanAPI context artifacts for Telegram signal retrospectives."""

from __future__ import annotations

import hashlib
import json
import os
import urllib.error
import urllib.request
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from signal_sandbox.auto_validation.evidence import (
    SHA256_HEX_LENGTH,
    AutoValidationEvidenceBundle,
)

SANTIMENT_ENABLE_ENV = "SIGNAL_SANDBOX_ENABLE_SANTIMENT"
SANTIMENT_API_KEY_ENV = "SIGNAL_SANDBOX_SANTIMENT_API_KEY"
SANTIMENT_GRAPHQL_URL = "https://api.santiment.net/graphql"
SANTIMENT_USER_AGENT = (
    "signal-analytics-sandbox/0.1 (+https://github.com/ashishki/entropy_protocol)"
)
SANTIMENT_CONTEXT_SCHEMA_VERSION = "signal_santiment_context.v1"
DEFAULT_SANTIMENT_CONTEXT_METRICS = (
    "price_usd",
    "social_volume_total",
    "sentiment_weighted_total",
    "daily_active_addresses",
    "exchange_inflow_usd",
    "exchange_outflow_usd",
)


class SantimentProviderError(RuntimeError):
    """Raised when Santiment cannot return a usable provider response."""


class SantimentMetricProvider(Protocol):
    provider_id: str

    def fetch_metric_timeseries(
        self,
        *,
        metric: str,
        slug: str,
        start_utc: datetime,
        end_utc: datetime,
        interval: str,
    ) -> list[dict[str, Any]]: ...


class SantimentMetricPoint(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    datetime_utc: datetime
    value: Decimal | None = None

    @field_validator("datetime_utc", mode="before")
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        return _coerce_datetime(value)

    @field_validator("value", mode="before")
    @classmethod
    def _coerce_decimal(cls, value: object) -> Decimal | None:
        if value is None:
            return None
        try:
            return Decimal(str(value))
        except (InvalidOperation, ValueError) as exc:
            raise ValueError("metric value must be decimal-compatible") from exc


class SantimentMetricSeries(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    metric: str = Field(min_length=1)
    slug: str = Field(min_length=1)
    interval: str = Field(min_length=1)
    points: list[SantimentMetricPoint] = Field(default_factory=list)
    provider_ref: str = Field(min_length=1)

    def data_sha256(self) -> str:
        payload = self.model_dump(mode="json", exclude_none=True)
        canonical = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class SantimentContextFeature(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    feature_id: str = Field(min_length=1)
    metric: str = Field(min_length=1)
    post_value: Decimal | None = None
    pre_window_value: Decimal | None = None
    post_window_value: Decimal | None = None
    delta_post_vs_pre: Decimal | None = None
    pct_change_post_vs_pre: Decimal | None = None
    interpretation: str = Field(min_length=1)


class SantimentContextArtifact(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    artifact_type: str = "santiment_context"
    schema_version: str = SANTIMENT_CONTEXT_SCHEMA_VERSION
    candidate_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    asset: str = Field(min_length=1)
    santiment_slug: str = Field(min_length=1)
    provider_id: str = Field(min_length=1)
    post_timestamp_utc: datetime
    window_start_utc: datetime
    window_end_utc: datetime
    interval: str = Field(min_length=1)
    evidence_bundle_sha256: str = Field(
        min_length=SHA256_HEX_LENGTH, max_length=SHA256_HEX_LENGTH
    )
    metric_series: list[SantimentMetricSeries] = Field(min_length=1)
    features: list[SantimentContextFeature] = Field(default_factory=list)
    blocker_reasons: list[str] = Field(default_factory=list)
    generated_at_utc: datetime

    @field_validator(
        "post_timestamp_utc",
        "window_start_utc",
        "window_end_utc",
        "generated_at_utc",
        mode="before",
    )
    @classmethod
    def _coerce_datetime(cls, value: object) -> datetime:
        return _coerce_datetime(value)

    @field_validator("evidence_bundle_sha256")
    @classmethod
    def _validate_sha256(cls, value: str) -> str:
        if any(char not in "0123456789abcdef" for char in value):
            raise ValueError("evidence_bundle_sha256 must be lowercase hexadecimal")
        return value

    @model_validator(mode="after")
    def _validate_window(self) -> SantimentContextArtifact:
        if self.window_start_utc > self.post_timestamp_utc:
            raise ValueError("window_start_utc must not be after post timestamp")
        if self.window_end_utc <= self.post_timestamp_utc:
            raise ValueError("window_end_utc must be after post timestamp")
        return self

    def canonical_json(self) -> str:
        payload = self.model_dump(mode="json", exclude_none=True)
        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    def artifact_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json().encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SantimentContextExport:
    json_path: Path
    markdown_path: Path
    artifact_sha256: str


class SantimentGraphQLClient:
    """Small SanAPI GraphQL client for deterministic metric pulls."""

    provider_id = "santiment_sanapi"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        endpoint: str = SANTIMENT_GRAPHQL_URL,
        timeout_seconds: int = 30,
    ) -> None:
        self.api_key = api_key or os.environ.get(SANTIMENT_API_KEY_ENV)
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds

    def fetch_metric_timeseries(
        self,
        *,
        metric: str,
        slug: str,
        start_utc: datetime,
        end_utc: datetime,
        interval: str,
    ) -> list[dict[str, Any]]:
        query = """
        query MetricTimeseries(
          $metric: String!
          $slug: String!
          $from: DateTime!
          $to: DateTime!
          $interval: interval!
        ) {
          getMetric(metric: $metric) {
            timeseriesDataJson(
              slug: $slug
              from: $from
              to: $to
              interval: $interval
            )
          }
        }
        """
        payload = {
            "query": query,
            "variables": {
                "metric": metric,
                "slug": slug,
                "from": _iso_z(start_utc),
                "to": _iso_z(end_utc),
                "interval": interval,
            },
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SANTIMENT_USER_AGENT,
        }
        if self.api_key:
            headers["Authorization"] = f"Apikey {self.api_key}"
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request, timeout=self.timeout_seconds
            ) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except (OSError, TimeoutError, urllib.error.URLError) as exc:
            raise SantimentProviderError("santiment_provider_unavailable") from exc

        if response_payload.get("errors"):
            raise SantimentProviderError("santiment_graphql_error")
        try:
            data = response_payload["data"]["getMetric"]["timeseriesDataJson"]
        except (KeyError, TypeError) as exc:
            raise SantimentProviderError("santiment_response_shape_error") from exc
        if isinstance(data, str):
            data = json.loads(data)
        if not isinstance(data, list):
            raise SantimentProviderError("santiment_timeseries_not_list")
        return data


def build_santiment_context_artifact(
    *,
    bundle: AutoValidationEvidenceBundle,
    provider: SantimentMetricProvider,
    slug_map: Mapping[str, str] | None = None,
    metrics: tuple[str, ...] = DEFAULT_SANTIMENT_CONTEXT_METRICS,
    lookback_days: int = 7,
    forward_days: int = 7,
    interval: str = "1d",
    generated_at_utc: datetime | None = None,
) -> SantimentContextArtifact:
    if bundle.extracted_fields.asset is None:
        raise ValueError("Santiment context requires extracted asset")

    asset = bundle.extracted_fields.asset.upper()
    santiment_slug = (slug_map or default_santiment_slug_map()).get(asset)
    if santiment_slug is None:
        raise ValueError(f"no Santiment slug mapping for asset: {asset}")

    start_utc = bundle.source_timestamp_utc - timedelta(days=lookback_days)
    end_utc = bundle.source_timestamp_utc + timedelta(days=forward_days)
    series = [
        _fetch_series(
            provider=provider,
            metric=metric,
            slug=santiment_slug,
            start_utc=start_utc,
            end_utc=end_utc,
            interval=interval,
        )
        for metric in metrics
    ]
    features = [
        feature
        for metric_series in series
        if (feature := _series_feature(metric_series, bundle.source_timestamp_utc))
        is not None
    ]
    blockers = [
        f"missing_santiment_points:{metric_series.metric}"
        for metric_series in series
        if not metric_series.points
    ]
    return SantimentContextArtifact(
        candidate_id=bundle.candidate_id,
        source_id=bundle.source_id,
        source_url=bundle.source_url,
        asset=asset,
        santiment_slug=santiment_slug,
        provider_id=provider.provider_id,
        post_timestamp_utc=bundle.source_timestamp_utc,
        window_start_utc=start_utc,
        window_end_utc=end_utc,
        interval=interval,
        evidence_bundle_sha256=bundle.bundle_sha256(),
        metric_series=series,
        features=features,
        blocker_reasons=blockers,
        generated_at_utc=generated_at_utc or datetime.now(UTC),
    )


def export_santiment_context_artifact(
    artifact: SantimentContextArtifact,
    *,
    output_dir: Path,
    stem: str | None = None,
) -> SantimentContextExport:
    artifact_stem = _artifact_stem(stem or artifact.candidate_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{artifact_stem}.santiment_context.json"
    markdown_path = output_dir / f"{artifact_stem}.santiment_context.md"
    json_path.write_text(artifact.canonical_json() + "\n", encoding="utf-8")
    markdown_path.write_text(
        render_santiment_context_markdown(artifact), encoding="utf-8"
    )
    return SantimentContextExport(
        json_path=json_path,
        markdown_path=markdown_path,
        artifact_sha256=artifact.artifact_sha256(),
    )


def load_santiment_context_artifact(path: Path) -> SantimentContextArtifact:
    return SantimentContextArtifact.model_validate_json(
        path.read_text(encoding="utf-8")
    )


def render_santiment_context_markdown(artifact: SantimentContextArtifact) -> str:
    lines = [
        "# Santiment Context Artifact",
        "",
        f"Candidate: `{artifact.candidate_id}`",
        f"Source: `{artifact.source_id}`",
        f"Asset: `{artifact.asset}` / `{artifact.santiment_slug}`",
        f"Provider: `{artifact.provider_id}`",
        f"Post timestamp: `{_iso_z(artifact.post_timestamp_utc)}`",
        f"Window: `{_iso_z(artifact.window_start_utc)}` to "
        f"`{_iso_z(artifact.window_end_utc)}`",
        f"Artifact SHA-256: `{artifact.artifact_sha256()}`",
        "",
        "## Features",
        "",
        "| feature | metric | pre | post | delta | pct_change | interpretation |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for feature in artifact.features:
        lines.append(
            "| "
            + " | ".join(
                [
                    feature.feature_id,
                    feature.metric,
                    _decimal_text(feature.pre_window_value),
                    _decimal_text(feature.post_window_value),
                    _decimal_text(feature.delta_post_vs_pre),
                    _decimal_text(feature.pct_change_post_vs_pre),
                    feature.interpretation,
                ]
            )
            + " |"
        )
    if not artifact.features:
        lines.append("| none | none |  |  |  |  | no comparable metric points |")
    lines.extend(["", "## Metric Refs", ""])
    for series in artifact.metric_series:
        lines.append(
            f"- `{series.provider_ref}`: {len(series.points)} points, "
            f"sha256 `{series.data_sha256()}`"
        )
    if artifact.blocker_reasons:
        lines.extend(["", "## Blockers", ""])
        lines.extend(f"- `{reason}`" for reason in artifact.blocker_reasons)
    lines.append("")
    return "\n".join(lines)


def default_santiment_slug_map() -> dict[str, str]:
    return {
        "ARB": "arbitrum",
        "AVAX": "avalanche",
        "BTC": "bitcoin",
        "DOT": "polkadot-new",
        "ETH": "ethereum",
        "SOL": "solana",
        "SUI": "sui",
        "TON": "toncoin",
    }


def santiment_env_enabled() -> bool:
    return os.environ.get(SANTIMENT_ENABLE_ENV, "").strip() == "1"


def _fetch_series(
    *,
    provider: SantimentMetricProvider,
    metric: str,
    slug: str,
    start_utc: datetime,
    end_utc: datetime,
    interval: str,
) -> SantimentMetricSeries:
    rows = provider.fetch_metric_timeseries(
        metric=metric,
        slug=slug,
        start_utc=start_utc,
        end_utc=end_utc,
        interval=interval,
    )
    return SantimentMetricSeries(
        metric=metric,
        slug=slug,
        interval=interval,
        points=[
            SantimentMetricPoint.model_validate(
                {
                    "datetime_utc": _row_datetime(row),
                    "value": row.get("value"),
                }
            )
            for row in rows
        ],
        provider_ref=f"santiment:{slug}:{metric}:{_iso_z(start_utc)}:{_iso_z(end_utc)}",
    )


def _series_feature(
    series: SantimentMetricSeries,
    post_timestamp_utc: datetime,
) -> SantimentContextFeature | None:
    pre = _nearest_value_before(series.points, post_timestamp_utc)
    post = _nearest_value_after(series.points, post_timestamp_utc)
    if pre is None and post is None:
        return None
    delta = None if pre is None or post is None else post - pre
    pct_change = None
    if pre is not None and pre != Decimal("0") and post is not None:
        pct_change = ((post - pre) / pre) * Decimal("100")
    return SantimentContextFeature(
        feature_id=f"{series.metric}:post_vs_pre",
        metric=series.metric,
        pre_window_value=pre,
        post_window_value=post,
        delta_post_vs_pre=delta,
        pct_change_post_vs_pre=pct_change,
        interpretation=_interpret_metric(series.metric, delta, pct_change),
    )


def _nearest_value_before(
    points: list[SantimentMetricPoint], timestamp_utc: datetime
) -> Decimal | None:
    candidates = [
        point
        for point in points
        if point.value is not None and point.datetime_utc <= timestamp_utc
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda point: point.datetime_utc).value


def _nearest_value_after(
    points: list[SantimentMetricPoint], timestamp_utc: datetime
) -> Decimal | None:
    candidates = [
        point
        for point in points
        if point.value is not None and point.datetime_utc >= timestamp_utc
    ]
    if not candidates:
        return None
    return min(candidates, key=lambda point: point.datetime_utc).value


def _row_datetime(row: Mapping[str, Any]) -> object:
    value = row.get("datetime") or row.get("datetime_utc")
    if value is None:
        raise ValueError("Santiment metric row missing datetime")
    return value


def _interpret_metric(
    metric: str, delta: Decimal | None, pct_change: Decimal | None
) -> str:
    if delta is None:
        return "insufficient_pre_or_post_points"
    direction = "up" if delta > 0 else "down" if delta < 0 else "flat"
    if metric.startswith("social_") or metric.startswith("sentiment_"):
        return f"{direction}_social_context_after_post"
    if metric.startswith("exchange_"):
        return f"{direction}_exchange_flow_context_after_post"
    if metric == "price_usd":
        return f"{direction}_price_context_after_post"
    if pct_change is not None:
        return f"{direction}_metric_context_after_post"
    return f"{direction}_context_after_post"


def _coerce_datetime(value: object) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
    if isinstance(value, str):
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=UTC)
    raise ValueError("timestamp fields must be datetime or ISO-8601 strings")


def _iso_z(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _decimal_text(value: Decimal | None) -> str:
    if value is None:
        return ""
    return format(value.normalize(), "f")


def _artifact_stem(value: str) -> str:
    if not value or Path(value).name != value or value in {".", ".."}:
        raise ValueError("artifact stem must be a single file-name component")
    return value
