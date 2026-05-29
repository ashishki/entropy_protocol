"""Deterministic report run manifests."""

from __future__ import annotations

import hashlib
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RunArtifactRef(BaseModel):
    model_config = ConfigDict(strict=True)

    name: str = Field(min_length=1)
    path: str = Field(min_length=1)
    sha256: str = Field(min_length=64, max_length=64)
    version: str = Field(default="")


class ProviderRunRef(BaseModel):
    model_config = ConfigDict(strict=True)

    provider: str = Field(min_length=1)
    symbol: str = Field(min_length=1)
    snapshot_id: str = Field(min_length=1)
    data_sha256: str = Field(min_length=64, max_length=64)


class CompactCacheRef(BaseModel):
    model_config = ConfigDict(strict=True)

    ref_id: str = Field(min_length=1)
    source_kind: str = Field(min_length=1)
    source_name: str = Field(min_length=1)
    source_sha256: str = Field(min_length=64, max_length=64)


class ReportRunManifest(BaseModel):
    model_config = ConfigDict(strict=True)

    run_id: str = Field(min_length=1)
    created_at_utc: datetime
    code_version: str = Field(min_length=1)
    input_refs: list[RunArtifactRef] = Field(min_length=1)
    provider_refs: list[ProviderRunRef] = Field(default_factory=list)
    output_refs: list[RunArtifactRef] = Field(min_length=1)
    cache_refs: list[CompactCacheRef] = Field(min_length=1)

    def canonical_json_bytes(self) -> bytes:
        return self.model_dump_json(by_alias=True).encode("utf-8")

    def manifest_sha256(self) -> str:
        return hashlib.sha256(self.canonical_json_bytes()).hexdigest()


def build_report_run_manifest(
    *,
    run_id: str,
    created_at_utc: datetime,
    code_version: str,
    input_refs: list[RunArtifactRef],
    provider_refs: list[ProviderRunRef],
    output_refs: list[RunArtifactRef],
) -> ReportRunManifest:
    ordered_inputs = sorted(input_refs, key=lambda item: (item.name, item.path))
    ordered_providers = sorted(
        provider_refs, key=lambda item: (item.provider, item.symbol, item.snapshot_id)
    )
    ordered_outputs = sorted(output_refs, key=lambda item: (item.name, item.path))
    cache_refs = [
        *[
            build_compact_cache_ref("input", item.name, item.sha256)
            for item in ordered_inputs
        ],
        *[
            build_compact_cache_ref(
                "provider",
                f"{item.provider}:{item.symbol}:{item.snapshot_id}",
                item.data_sha256,
            )
            for item in ordered_providers
        ],
        *[
            build_compact_cache_ref("output", item.name, item.sha256)
            for item in ordered_outputs
        ],
    ]
    return ReportRunManifest(
        run_id=run_id,
        created_at_utc=created_at_utc,
        code_version=code_version,
        input_refs=ordered_inputs,
        provider_refs=ordered_providers,
        output_refs=ordered_outputs,
        cache_refs=cache_refs,
    )


def build_compact_cache_ref(
    source_kind: str,
    source_name: str,
    source_sha256: str,
) -> CompactCacheRef:
    return CompactCacheRef(
        ref_id=f"{source_kind}:{source_name}:{source_sha256[:12]}",
        source_kind=source_kind,
        source_name=source_name,
        source_sha256=source_sha256,
    )
