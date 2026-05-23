"""Evidence appendix rendering for report and pre-client evidence rows."""

from __future__ import annotations

import json
from collections import Counter
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class EvidenceAppendixMetricRow(BaseModel):
    model_config = ConfigDict(strict=True)

    metric_id: str = Field(min_length=1)
    label: str = Field(min_length=1)
    value: str = Field(min_length=1)
    source_ref: str = Field(min_length=1)
    provider: str = Field(min_length=1)
    snapshot_id: str = Field(min_length=1)
    review_decision_id: str = Field(min_length=1)
    evidence_url: str = Field(min_length=1)


class EvidenceAppendix(BaseModel):
    model_config = ConfigDict(strict=True)

    report_id: str = Field(min_length=1)
    metric_rows: list[EvidenceAppendixMetricRow] = Field(min_length=1)


class PreclientEvidenceAppendixRow(BaseModel):
    model_config = ConfigDict(strict=True)

    row_id: str = Field(min_length=1)
    source_id: str = Field(min_length=1)
    source_url: str = Field(min_length=1)
    evidence_kind: str = Field(min_length=1)
    artifact_refs: list[str] = Field(min_length=1)
    checksum_or_text_hash: str = Field(min_length=1)
    review_status: str = Field(min_length=1)
    market_provider_status: str = Field(min_length=1)
    blockers: list[str]
    post_id: int | None = None
    media_ref_id: str | None = None
    modality: str | None = None
    evidence_types: list[str] = Field(default_factory=list)
    setup_fields: dict[str, Any] = Field(default_factory=dict)
    raw_media_included: bool = False
    private_source_required: bool = False


class PreclientEvidenceAppendixSummary(BaseModel):
    model_config = ConfigDict(strict=True)

    artifact_id: str = Field(min_length=1)
    generated_at_utc: str = Field(min_length=1)
    status: str = Field(min_length=1)
    channels: list[str] = Field(min_length=1)
    totals: dict[str, int]
    by_channel: dict[str, int]
    by_evidence_kind: dict[str, int]
    by_review_status: dict[str, int]
    by_market_provider_status: dict[str, int]
    raw_media_included: bool = False
    private_source_required: bool = False


class PreclientEvidenceAppendix(BaseModel):
    model_config = ConfigDict(strict=True)

    summary: PreclientEvidenceAppendixSummary
    rows: list[PreclientEvidenceAppendixRow] = Field(min_length=1)


def render_evidence_appendix_markdown(appendix: EvidenceAppendix) -> str:
    lines = [
        f"# Evidence Appendix: {appendix.report_id}",
        "",
        (
            "| metric_id | label | value | source_ref | provider | snapshot_id | "
            "review_decision_id | evidence_url |"
        ),
        "|---|---|---:|---|---|---|---|---|",
        *_metric_rows(appendix.metric_rows),
        "",
    ]
    return "\n".join(lines)


def build_preclient_evidence_appendix(
    *,
    model_review_packet: dict[str, Any],
    media_manifest: dict[str, Any],
    processing_queue: dict[str, Any],
    media_review_results: dict[str, Any],
    metric_results: dict[str, Any],
    generated_at_utc: str,
) -> PreclientEvidenceAppendix:
    manifest_by_media = {
        str(row["media_ref_id"]): row
        for row in media_manifest.get("media_manifest", [])
        if row.get("media_ref_id")
    }
    queue_by_media = {
        str(row["media_ref_id"]): row
        for row in processing_queue.get("processing_queue", [])
        if row.get("media_ref_id")
    }
    packet_by_media = {
        str(row["media_ref_id"]): row
        for row in model_review_packet.get("review_packet", [])
        if row.get("media_ref_id")
    }
    arbiter_by_media = {
        str(row["media_ref_id"]): row
        for row in media_review_results.get("arbiter_reviews", [])
        if row.get("media_ref_id")
    }
    mass_media_refs = {
        str(row["media_ref_id"])
        for row in media_review_results.get("mass_reviews", [])
        if row.get("media_ref_id")
    }

    rows: list[PreclientEvidenceAppendixRow] = []
    for review in sorted(
        media_review_results.get("mass_reviews", []),
        key=lambda item: (
            str(item.get("source_id", "")),
            int(item.get("post_id") or 0),
            str(item.get("media_ref_id", "")),
        ),
    ):
        media_ref_id = str(review["media_ref_id"])
        manifest_row = manifest_by_media.get(media_ref_id, {})
        queue_row = queue_by_media.get(media_ref_id, {})
        packet_row = packet_by_media.get(media_ref_id)
        arbiter_row = arbiter_by_media.get(media_ref_id)
        evidence_types = _evidence_types(review, packet_row)
        rows.append(
            PreclientEvidenceAppendixRow(
                row_id=_row_id("media", review),
                source_id=str(review["source_id"]),
                source_url=str(review["source_url"]),
                post_id=int(review["post_id"]),
                media_ref_id=media_ref_id,
                modality=str(review.get("modality") or ""),
                evidence_kind=_media_evidence_kind(review, packet_row, evidence_types),
                artifact_refs=_media_artifact_refs(
                    media_ref_id=media_ref_id,
                    review=review,
                    queue_row=queue_row,
                    packet_row=packet_row,
                    arbiter_row=arbiter_row,
                ),
                checksum_or_text_hash=_checksum_or_text_hash(
                    manifest_row=manifest_row,
                    queue_row=queue_row,
                    fallback=review,
                ),
                review_status=_review_status(review, arbiter_row),
                market_provider_status=_market_provider_status(packet_row, review),
                blockers=_blockers(review, packet_row),
                evidence_types=evidence_types,
                setup_fields=_setup_fields(review, packet_row),
            )
        )

    for queue_row in sorted(
        processing_queue.get("processing_queue", []),
        key=lambda item: (
            str(item.get("source_id", "")),
            int(item.get("post_id") or 0),
            str(item.get("media_ref_id", "")),
        ),
    ):
        media_ref_id = str(queue_row.get("media_ref_id") or "")
        if media_ref_id in mass_media_refs:
            continue
        manifest_row = manifest_by_media.get(media_ref_id, {})
        rows.append(
            PreclientEvidenceAppendixRow(
                row_id=_row_id("processing", queue_row),
                source_id=str(queue_row["source_id"]),
                source_url=str(queue_row["source_url"]),
                post_id=int(queue_row["post_id"]),
                media_ref_id=media_ref_id,
                modality=str(queue_row.get("modality") or ""),
                evidence_kind="media_processing_blocker",
                artifact_refs=[
                    f"docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json#{media_ref_id}",
                    f"docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json#{media_ref_id}",
                ],
                checksum_or_text_hash=_checksum_or_text_hash(
                    manifest_row=manifest_row,
                    queue_row=queue_row,
                    fallback=queue_row,
                ),
                review_status=f"processing={queue_row.get('status')}",
                market_provider_status="not_market_validated_media_processing_blocker",
                blockers=_processing_blockers(queue_row),
            )
        )

    for channel_summary in metric_results.get("channel_summaries", []):
        source_id = str(channel_summary["source_id"])
        kept_claim_ids = metric_results.get("kept_claim_ids_by_channel", {}).get(
            source_id, []
        )
        rows.append(_text_metric_summary_row(channel_summary, kept_claim_ids))
        rows.append(_provider_gap_row(channel_summary))

    rows = sorted(
        rows,
        key=lambda row: (
            row.source_id,
            row.post_id or 0,
            row.evidence_kind,
            row.media_ref_id or row.row_id,
        ),
    )
    summary = _preclient_summary(rows, generated_at_utc)
    return PreclientEvidenceAppendix(summary=summary, rows=rows)


def render_preclient_evidence_appendix_markdown(
    appendix: PreclientEvidenceAppendix,
) -> str:
    summary = appendix.summary
    lines = [
        "# Pre-Client Evidence Appendix",
        "",
        f"Date: {summary.generated_at_utc}",
        f"Status: `{summary.status}`",
        "",
        "## Boundary",
        "",
        "- This is an internal traceability artifact.",
        (
            "- It includes no raw media bytes and requires no "
            "private/authenticated source access."
        ),
        (
            "- Model-reviewed media rows are not customer-facing until "
            "human/operator review."
        ),
        "",
        "## Totals",
        "",
        *[f"- `{key}`: {value}" for key, value in sorted(summary.totals.items())],
        "",
        "## By Channel",
        "",
        *[f"- `{key}`: {value}" for key, value in summary.by_channel.items()],
        "",
        "## By Evidence Kind",
        "",
        *[f"- `{key}`: {value}" for key, value in summary.by_evidence_kind.items()],
        "",
        "## Rows",
        "",
        (
            "| channel | post | kind | media | review | market/provider | "
            "blockers | checksum/hash | source |"
        ),
        "|---|---:|---|---|---|---|---|---|---|",
        *[_preclient_row_markdown(row) for row in appendix.rows],
        "",
    ]
    return "\n".join(lines)


def _metric_rows(rows: list[EvidenceAppendixMetricRow]) -> list[str]:
    return [
        " | ".join(
            [
                f"| `{_escape(row.metric_id)}`",
                _escape(row.label),
                _escape(row.value),
                f"`{_escape(row.source_ref)}`",
                _escape(row.provider),
                f"`{_escape(row.snapshot_id)}`",
                f"`{_escape(row.review_decision_id)}`",
                f"{_escape(row.evidence_url)} |",
            ]
        )
        for row in sorted(rows, key=lambda item: item.metric_id)
    ]


def _escape(value: str) -> str:
    return value.replace("|", "\\|")


def _evidence_types(
    review: dict[str, Any],
    packet_row: dict[str, Any] | None,
) -> list[str]:
    if packet_row is not None:
        return [str(item) for item in packet_row.get("selected_evidence_types", [])]
    return [str(item) for item in review.get("evidence_types", [])]


def _media_evidence_kind(
    review: dict[str, Any],
    packet_row: dict[str, Any] | None,
    evidence_types: list[str],
) -> str:
    decision = str(review.get("decision") or "")
    if packet_row is not None and "post_factum" in evidence_types:
        return "media_post_factum"
    if packet_row is not None:
        return "media_backed_claim"
    if decision == "context_only":
        return "context_only"
    if decision == "reject_noise":
        return "rejected_noise"
    if decision == "unable_to_review":
        return "media_processing_blocker"
    return "media_review_queue"


def _media_artifact_refs(
    *,
    media_ref_id: str,
    review: dict[str, Any],
    queue_row: dict[str, Any],
    packet_row: dict[str, Any] | None,
    arbiter_row: dict[str, Any] | None,
) -> list[str]:
    refs = [
        f"docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json#{media_ref_id}",
        f"docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json#{media_ref_id}",
        f"docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json#mass:{review.get('review_id')}",
    ]
    artifact_path = str(
        review.get("artifact_path") or queue_row.get("artifact_path") or ""
    )
    if artifact_path.startswith("docs/pilot/"):
        refs.append(artifact_path)
    if arbiter_row is not None:
        refs.append(
            "docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json#"
            f"arbiter:{arbiter_row.get('review_id')}"
        )
    if packet_row is not None:
        refs.append(
            "docs/pilot/preclient_MODEL_REVIEW_PACKET.json#"
            f"{packet_row.get('packet_id')}"
        )
    return sorted(set(refs))


def _checksum_or_text_hash(
    *,
    manifest_row: dict[str, Any],
    queue_row: dict[str, Any],
    fallback: dict[str, Any],
) -> str:
    media_sha = manifest_row.get("media_sha256")
    if media_sha:
        return f"media_sha256:{media_sha}"
    text = queue_row.get("extracted_text")
    if isinstance(text, str) and text:
        return f"text_sha256:{_sha256_text(text)}"
    return f"row_sha256:{_sha256_json(fallback)}"


def _review_status(
    review: dict[str, Any],
    arbiter_row: dict[str, Any] | None,
) -> str:
    status = f"mass={review.get('decision')}"
    if arbiter_row is not None:
        status = f"{status};arbiter={arbiter_row.get('decision')}"
    return status


def _market_provider_status(
    packet_row: dict[str, Any] | None,
    review: dict[str, Any],
) -> str:
    if packet_row is not None:
        rr_status = packet_row.get("setup_fields", {}).get("deterministic_rr_status")
        if rr_status == "rr_ready_internal_draft":
            return "rr_ready_internal_draft_market_recompute_required"
        if rr_status == "rr_blocked":
            return "rr_blocked"
        return "market_validation_pending_operator_review"
    decision = str(review.get("decision") or "")
    if decision in {"context_only", "reject_noise"}:
        return "not_market_claim"
    if decision == "unable_to_review":
        return "market_validation_blocked_by_media_review"
    return "not_market_validated_media_review_only"


def _blockers(
    review: dict[str, Any],
    packet_row: dict[str, Any] | None,
) -> list[str]:
    if packet_row is not None:
        return sorted({str(item) for item in packet_row.get("blockers", [])})
    blockers = {str(item) for item in review.get("blockers", [])}
    if review.get("human_review_required") is True:
        blockers.add("human_operator_review_required")
    if not blockers:
        blockers.add("no_market_claim")
    return sorted(blockers)


def _setup_fields(
    review: dict[str, Any],
    packet_row: dict[str, Any] | None,
) -> dict[str, Any]:
    if packet_row is not None:
        return dict(packet_row.get("setup_fields", {}))
    return {
        "assets": review.get("assets"),
        "direction": review.get("direction"),
        "entry": review.get("entry"),
        "stop": review.get("stop"),
        "targets": review.get("targets"),
        "position_size": review.get("position_size"),
        "explicit_rr": review.get("explicit_rr"),
        "timeframe": review.get("timeframe"),
    }


def _processing_blockers(queue_row: dict[str, Any]) -> list[str]:
    blockers = {
        str(queue_row.get("status") or "processing_blocked"),
        str(queue_row.get("planned_action") or "manual_review_required"),
        "human_operator_review_required",
    }
    error = queue_row.get("error")
    if error:
        blockers.add(str(error))
    return sorted(blockers)


def _text_metric_summary_row(
    channel_summary: dict[str, Any],
    kept_claim_ids: list[str],
) -> PreclientEvidenceAppendixRow:
    source_id = str(channel_summary["source_id"])
    row_payload = {
        "channel_summary": channel_summary,
        "kept_claim_ids": kept_claim_ids,
    }
    return PreclientEvidenceAppendixRow(
        row_id=_row_id("text_metric", row_payload),
        source_id=source_id,
        source_url=(
            "artifact://docs/pilot/three_channel_V1_METRIC_RESULTS.json"
            f"#channel={source_id}"
        ),
        evidence_kind="text_only_claim_metric_summary",
        artifact_refs=[
            f"docs/pilot/three_channel_V1_METRIC_RESULTS.json#channel={source_id}"
        ],
        checksum_or_text_hash=f"row_sha256:{_sha256_json(row_payload)}",
        review_status=_text_review_status(channel_summary),
        market_provider_status=_provider_coverage_status(channel_summary),
        blockers=_text_summary_blockers(channel_summary),
        setup_fields={
            "v1_evaluable_claims": channel_summary.get("v1_evaluable_claims"),
            "confirmed_hits": channel_summary.get("confirmed_hits"),
            "contradicted_misses": channel_summary.get("contradicted_misses"),
            "primary_hit_rate": channel_summary.get("primary_hit_rate"),
            "kept_claim_ids": kept_claim_ids,
        },
    )


def _provider_gap_row(channel_summary: dict[str, Any]) -> PreclientEvidenceAppendixRow:
    source_id = str(channel_summary["source_id"])
    gap_count = int(
        channel_summary.get("exclusion_counts", {}).get(
            "no_supported_asset_or_proxy", 0
        )
    )
    row_payload = {
        "source_id": source_id,
        "no_supported_asset_or_proxy": gap_count,
        "provider_coverage": channel_summary.get("provider_coverage", {}),
    }
    return PreclientEvidenceAppendixRow(
        row_id=_row_id("provider_gap", row_payload),
        source_id=source_id,
        source_url=(
            "artifact://docs/pilot/three_channel_V1_METRIC_RESULTS.json"
            f"#provider_gap={source_id}"
        ),
        evidence_kind="provider_gap",
        artifact_refs=[
            f"docs/pilot/three_channel_V1_METRIC_RESULTS.json#provider_gap={source_id}"
        ],
        checksum_or_text_hash=f"row_sha256:{_sha256_json(row_payload)}",
        review_status="v1_exclusion_summary",
        market_provider_status=f"provider_gap:no_supported_asset_or_proxy={gap_count}",
        blockers=[
            f"no_supported_asset_or_proxy={gap_count}",
            "provider_gap_is_exclusion_not_author_loss",
        ],
        setup_fields={
            "provider_coverage": channel_summary.get("provider_coverage", {}),
            "exclusion_counts": channel_summary.get("exclusion_counts", {}),
        },
    )


def _preclient_summary(
    rows: list[PreclientEvidenceAppendixRow],
    generated_at_utc: str,
) -> PreclientEvidenceAppendixSummary:
    by_channel = Counter(row.source_id for row in rows)
    by_kind = Counter(row.evidence_kind for row in rows)
    by_review = Counter(row.review_status for row in rows)
    by_market = Counter(row.market_provider_status for row in rows)
    return PreclientEvidenceAppendixSummary(
        artifact_id="preclient-evidence-appendix",
        generated_at_utc=generated_at_utc,
        status="internal_traceability_appendix",
        channels=sorted(by_channel),
        totals={
            "rows": len(rows),
            "channels": len(by_channel),
            "rows_with_blockers": sum(1 for row in rows if row.blockers),
            "raw_media_rows": sum(1 for row in rows if row.raw_media_included),
            "private_source_rows": sum(
                1 for row in rows if row.private_source_required
            ),
        },
        by_channel=dict(sorted(by_channel.items())),
        by_evidence_kind=dict(sorted(by_kind.items())),
        by_review_status=dict(sorted(by_review.items())),
        by_market_provider_status=dict(sorted(by_market.items())),
    )


def _text_review_status(channel_summary: dict[str, Any]) -> str:
    decisions = channel_summary.get("review_decision_counts", {})
    parts = [f"{key}={value}" for key, value in sorted(decisions.items())]
    return "text_v1_review_decisions:" + ",".join(parts)


def _provider_coverage_status(channel_summary: dict[str, Any]) -> str:
    coverage = channel_summary.get("provider_coverage", {})
    if not coverage:
        return "provider_coverage:none"
    parts = [
        f"{provider}={details.get('claim_count', 0)}"
        for provider, details in sorted(coverage.items())
    ]
    return "provider_coverage:" + ",".join(parts)


def _text_summary_blockers(channel_summary: dict[str, Any]) -> list[str]:
    exclusions = channel_summary.get("exclusion_counts", {})
    blockers = [
        f"{key}={value}"
        for key, value in sorted(exclusions.items())
        if int(value) > 0 and key.startswith("review_")
    ]
    if int(exclusions.get("no_supported_asset_or_proxy", 0)) > 0:
        blockers.append("provider_gap_summary_in_separate_row")
    return blockers


def _preclient_row_markdown(row: PreclientEvidenceAppendixRow) -> str:
    blockers = ", ".join(row.blockers[:4])
    if len(row.blockers) > 4:
        blockers = f"{blockers}, +{len(row.blockers) - 4}"
    checksum = row.checksum_or_text_hash
    if len(checksum) > 24:
        checksum = f"{checksum[:24]}..."
    post = "-" if row.post_id is None else str(row.post_id)
    media = "-" if row.media_ref_id is None else row.media_ref_id
    return " | ".join(
        [
            f"| `{_escape(row.source_id)}`",
            post,
            f"`{_escape(row.evidence_kind)}`",
            f"`{_escape(media)}`",
            _escape(row.review_status),
            _escape(row.market_provider_status),
            _escape(blockers),
            f"`{_escape(checksum)}`",
            f"{_escape(row.source_url)} |",
        ]
    )


def _row_id(prefix: str, payload: dict[str, Any]) -> str:
    return f"preclient_appendix_{prefix}_{_sha256_json(payload)[:16]}"


def _sha256_json(value: Any) -> str:
    return _sha256_text(json.dumps(value, ensure_ascii=False, sort_keys=True))


def _sha256_text(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()
