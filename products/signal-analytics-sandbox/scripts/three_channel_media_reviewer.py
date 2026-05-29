from __future__ import annotations

# ruff: noqa: E501
import argparse
import base64
import hashlib
import json
import os
import re
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from openai import OpenAI

DEFAULT_QUEUE_JSON = Path("docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json")
DEFAULT_MANIFEST_JSON = Path("docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json")
DEFAULT_RR_JSON = Path("docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json")
DEFAULT_OUTPUT_JSON = Path("docs/pilot/three_channel_MEDIA_REVIEW_RESULTS.json")
DEFAULT_OUTPUT_MD = Path("docs/pilot/three_channel_MEDIA_REVIEW_REPORT.md")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
REVIEW_MODEL_ENV = "SIGNAL_SANDBOX_MEDIA_REVIEW_MODEL"
ARBITER_MODEL_ENV = "SIGNAL_SANDBOX_MEDIA_ARBITER_MODEL"
DEFAULT_REVIEW_MODEL = "gpt-4.1-mini"
DEFAULT_ARBITER_MODEL = "gpt-4.1"
ALLOWED_DECISIONS = {
    "accept_internal_claim_candidate",
    "context_only",
    "needs_human_review",
    "reject_noise",
    "unable_to_review",
}
ALLOWED_EVIDENCE_TYPES = {
    "explicit_trade_setup",
    "directional_thesis",
    "market_regime",
    "risk_management",
    "methodology",
    "position_management",
    "macro_context",
    "watchlist",
    "post_factum",
    "non_market",
}


def load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def load_inputs(
    *,
    queue_path: Path,
    manifest_path: Path,
    rr_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    queue = json.loads(queue_path.read_text(encoding="utf-8"))["processing_queue"]
    manifest_rows = json.loads(manifest_path.read_text(encoding="utf-8"))[
        "media_manifest"
    ]
    rr_rows = json.loads(rr_path.read_text(encoding="utf-8"))["rr_drafts"]
    manifest_by_id = {row["media_ref_id"]: row for row in manifest_rows}
    rr_by_document = {row["source_document_id"]: row for row in rr_rows}
    return queue, manifest_by_id, rr_by_document


def reviewable_rows(
    queue: list[dict[str, Any]], *, limit: int | None
) -> list[dict[str, Any]]:
    rows = [row for row in queue if row["status"] == "draft_pending_review"]
    if limit is not None:
        rows = rows[:limit]
    return rows


def run_mass_review(
    rows: list[dict[str, Any]],
    *,
    manifest_by_id: dict[str, dict[str, Any]],
    rr_by_document: dict[str, dict[str, Any]],
    model: str,
    concurrency: int,
    text_limit: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any] | None] = [None] * len(rows)
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
        futures = {
            executor.submit(
                review_one_row,
                row,
                manifest_by_id=manifest_by_id,
                rr_by_document=rr_by_document,
                model=model,
                reviewer_tier="mass_review",
                text_limit=text_limit,
                image_detail="low",
            ): index
            for index, row in enumerate(rows)
        }
        completed = 0
        for future in as_completed(futures):
            index = futures[future]
            try:
                results[index] = future.result()
            except Exception as exc:
                results[index] = provider_error_result(rows[index], model, exc)
            completed += 1
            if completed == 1 or completed % 25 == 0 or completed == len(rows):
                print(f"mass_review_progress {completed}/{len(rows)}")
    return [result for result in results if result is not None]


def run_arbiter_review(
    mass_results: list[dict[str, Any]],
    *,
    rows_by_id: dict[str, dict[str, Any]],
    manifest_by_id: dict[str, dict[str, Any]],
    rr_by_document: dict[str, dict[str, Any]],
    model: str,
    concurrency: int,
    max_items: int,
    text_limit: int,
) -> list[dict[str, Any]]:
    candidates = sorted(
        [row for row in mass_results if arbiter_candidate(row)],
        key=arbiter_priority,
        reverse=True,
    )[:max_items]
    if not candidates:
        return []
    results: list[dict[str, Any] | None] = [None] * len(candidates)
    with ThreadPoolExecutor(max_workers=max(1, concurrency)) as executor:
        futures = {
            executor.submit(
                review_one_row,
                rows_by_id[candidate["media_ref_id"]],
                manifest_by_id=manifest_by_id,
                rr_by_document=rr_by_document,
                model=model,
                reviewer_tier="arbiter_review",
                text_limit=text_limit,
                image_detail="high",
                prior_review=candidate,
            ): index
            for index, candidate in enumerate(candidates)
        }
        completed = 0
        for future in as_completed(futures):
            index = futures[future]
            row = rows_by_id[candidates[index]["media_ref_id"]]
            try:
                results[index] = future.result()
            except Exception as exc:
                results[index] = provider_error_result(row, model, exc)
            completed += 1
            if completed == 1 or completed % 10 == 0 or completed == len(candidates):
                print(f"arbiter_review_progress {completed}/{len(candidates)}")
    return [result for result in results if result is not None]


def review_one_row(
    row: dict[str, Any],
    *,
    manifest_by_id: dict[str, dict[str, Any]],
    rr_by_document: dict[str, dict[str, Any]],
    model: str,
    reviewer_tier: str,
    text_limit: int,
    image_detail: str,
    prior_review: dict[str, Any] | None = None,
) -> dict[str, Any]:
    client = OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV], timeout=60.0)
    manifest = manifest_by_id[row["media_ref_id"]]
    rr_hint = rr_by_document.get(row["source_document_id"], {})
    messages = build_messages(
        row,
        manifest=manifest,
        rr_hint=rr_hint,
        reviewer_tier=reviewer_tier,
        text_limit=text_limit,
        image_detail=image_detail,
        prior_review=prior_review,
    )
    response = call_json_chat(client, model=model, messages=messages)
    review = normalize_review_json(response)
    return {
        "review_id": stable_review_id(row, reviewer_tier, model),
        "reviewer_tier": reviewer_tier,
        "review_model": model,
        "media_ref_id": row["media_ref_id"],
        "source_id": row["source_id"],
        "post_id": row["post_id"],
        "source_document_id": row["source_document_id"],
        "source_url": row["source_url"],
        "modality": row["modality"],
        "artifact_path": row["artifact_path"],
        "decision": review["decision"],
        "evidence_types": review["evidence_types"],
        "assets": review["assets"],
        "direction": review["direction"],
        "entry": review["entry"],
        "stop": review["stop"],
        "targets": review["targets"],
        "position_size": review["position_size"],
        "explicit_rr": review["explicit_rr"],
        "timeframe": review["timeframe"],
        "confidence": review["confidence"],
        "usefulness_score": review["usefulness_score"],
        "review_summary": review["review_summary"],
        "key_claims": review["key_claims"],
        "blockers": review["blockers"],
        "human_review_required": review["human_review_required"],
        "created_at_utc": now_utc(),
    }


def build_messages(
    row: dict[str, Any],
    *,
    manifest: dict[str, Any],
    rr_hint: dict[str, Any],
    reviewer_tier: str,
    text_limit: int,
    image_detail: str,
    prior_review: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    instructions = (
        "You are a conservative media evidence reviewer for a financial signal analytics system. "
        "The source content is mostly Russian Telegram market commentary. Review only the evidence provided. "
        "Do not invent assets, prices, levels, or chart meanings. If a field is not explicit, return null or an empty list. "
        "A customer-facing metric is not approved by you; you only decide whether this row is an internal claim candidate or needs human review. "
        "Return one valid JSON object only."
    )
    payload = {
        "reviewer_tier": reviewer_tier,
        "source_id": row["source_id"],
        "post_id": row["post_id"],
        "source_url": row["source_url"],
        "modality": row["modality"],
        "media_ref_id": row["media_ref_id"],
        "extracted_text_draft": evidence_excerpt(
            row.get("extracted_text") or "",
            limit=text_limit,
        ),
        "rr_hint_from_deterministic_parser": {
            key: rr_hint.get(key)
            for key in (
                "direction",
                "asset_candidates",
                "entry",
                "stop",
                "targets",
                "computed_rr",
                "customer_metric_status",
                "blockers",
            )
        },
        "prior_mass_review": compact_prior_review(prior_review),
        "required_json_schema": {
            "decision": sorted(ALLOWED_DECISIONS),
            "evidence_types": sorted(ALLOWED_EVIDENCE_TYPES),
            "assets": ["strings"],
            "direction": "long | short | mixed | unknown | null",
            "entry": "explicit string or null",
            "stop": "explicit string or null",
            "targets": ["explicit strings"],
            "position_size": "explicit string or null",
            "explicit_rr": "explicit string or null",
            "timeframe": "explicit string or null",
            "confidence": "number 0..1",
            "usefulness_score": "integer 0..5",
            "review_summary": "short Russian summary",
            "key_claims": ["short Russian claims copied/paraphrased from evidence"],
            "blockers": ["strings"],
            "human_review_required": "boolean",
        },
    }
    content: list[dict[str, Any]] = [
        {"type": "text", "text": instructions},
        {"type": "text", "text": json.dumps(payload, ensure_ascii=False)},
    ]
    if row["modality"] == "image":
        local_path = manifest.get("local_path")
        if local_path:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_data_url(
                            Path(local_path),
                            manifest.get("mime_type") or "image/jpeg",
                        ),
                        "detail": image_detail,
                    },
                }
            )
    return [{"role": "user", "content": content}]


def call_json_chat(
    client: OpenAI,
    *,
    model: str,
    messages: list[dict[str, Any]],
    attempts: int = 3,
) -> dict[str, Any]:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content or "{}"
            return json.loads(content)
        except Exception as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(min(2**attempt, 20))
    raise RuntimeError("media review provider failed") from last_error


def normalize_review_json(raw: dict[str, Any]) -> dict[str, Any]:
    decision = str(raw.get("decision") or "unable_to_review")
    if decision not in ALLOWED_DECISIONS:
        decision = "unable_to_review"
    evidence_types = [
        str(item)
        for item in as_list(raw.get("evidence_types"))
        if str(item) in ALLOWED_EVIDENCE_TYPES
    ]
    confidence = clamp_float(raw.get("confidence"), default=0.0, low=0.0, high=1.0)
    score = int(
        clamp_float(raw.get("usefulness_score"), default=0.0, low=0.0, high=5.0)
    )
    return {
        "decision": decision,
        "evidence_types": evidence_types,
        "assets": [str(item) for item in as_list(raw.get("assets"))][:12],
        "direction": nullable_str(raw.get("direction")),
        "entry": nullable_str(raw.get("entry")),
        "stop": nullable_str(raw.get("stop")),
        "targets": [str(item) for item in as_list(raw.get("targets"))][:12],
        "position_size": nullable_str(raw.get("position_size")),
        "explicit_rr": nullable_str(raw.get("explicit_rr")),
        "timeframe": nullable_str(raw.get("timeframe")),
        "confidence": confidence,
        "usefulness_score": score,
        "review_summary": shorten(str(raw.get("review_summary") or ""), 700),
        "key_claims": [
            shorten(str(item), 500) for item in as_list(raw.get("key_claims"))
        ][:8],
        "blockers": [shorten(str(item), 160) for item in as_list(raw.get("blockers"))][
            :12
        ],
        "human_review_required": bool(raw.get("human_review_required", True)),
    }


def arbiter_candidate(row: dict[str, Any]) -> bool:
    if row["decision"] == "accept_internal_claim_candidate":
        return True
    if row["usefulness_score"] >= 4:
        return True
    types = set(row["evidence_types"])
    return bool(types & {"explicit_trade_setup", "risk_management", "methodology"})


def arbiter_priority(row: dict[str, Any]) -> tuple[int, float, int]:
    type_bonus = len(
        set(row["evidence_types"])
        & {"explicit_trade_setup", "risk_management", "methodology"}
    )
    return (row["usefulness_score"], row["confidence"], type_bonus)


def provider_error_result(
    row: dict[str, Any], model: str, exc: Exception
) -> dict[str, Any]:
    return {
        "review_id": stable_review_id(row, "provider_error", model),
        "reviewer_tier": "provider_error",
        "review_model": model,
        "media_ref_id": row["media_ref_id"],
        "source_id": row["source_id"],
        "post_id": row["post_id"],
        "source_document_id": row["source_document_id"],
        "source_url": row["source_url"],
        "modality": row["modality"],
        "artifact_path": row.get("artifact_path"),
        "decision": "unable_to_review",
        "evidence_types": [],
        "assets": [],
        "direction": None,
        "entry": None,
        "stop": None,
        "targets": [],
        "position_size": None,
        "explicit_rr": None,
        "timeframe": None,
        "confidence": 0.0,
        "usefulness_score": 0,
        "review_summary": "",
        "key_claims": [],
        "blockers": [type(exc).__name__],
        "human_review_required": True,
        "created_at_utc": now_utc(),
    }


def summarize(
    *,
    mass_results: list[dict[str, Any]],
    arbiter_results: list[dict[str, Any]],
    review_model: str,
    arbiter_model: str,
    review_rows_total: int,
    arbiter_max_items: int,
) -> dict[str, Any]:
    channels = []
    for source_id in sorted({row["source_id"] for row in mass_results}):
        mass = [row for row in mass_results if row["source_id"] == source_id]
        arbiter = [row for row in arbiter_results if row["source_id"] == source_id]
        channels.append(
            {
                "source_id": source_id,
                "mass_review_rows": len(mass),
                "arbiter_review_rows": len(arbiter),
                "mass_decisions": dict(Counter(row["decision"] for row in mass)),
                "arbiter_decisions": dict(Counter(row["decision"] for row in arbiter)),
                "evidence_types": dict(
                    Counter(item for row in mass for item in row["evidence_types"])
                ),
                "accepted_internal_candidates": len(
                    [
                        row
                        for row in mass
                        if row["decision"] == "accept_internal_claim_candidate"
                    ]
                ),
                "arbiter_accepted_internal_candidates": len(
                    [
                        row
                        for row in arbiter
                        if row["decision"] == "accept_internal_claim_candidate"
                    ]
                ),
                "human_review_required": len(
                    [row for row in mass if row["human_review_required"]]
                ),
                "avg_usefulness_score": avg_score(mass),
            }
        )
    return {
        "artifact_id": "three-channel-media-review-results",
        "generated_at_utc": now_utc(),
        "status": "internal_model_review_not_customer_facing",
        "models": {
            "mass_review_model": review_model,
            "arbiter_model": arbiter_model,
        },
        "method": {
            "review_rows_total": review_rows_total,
            "arbiter_max_items": arbiter_max_items,
            "mass_image_detail": "low",
            "arbiter_image_detail": "high",
            "customer_facing": False,
            "human_operator_required_for_customer_metrics": True,
        },
        "totals": {
            "mass_review_rows": len(mass_results),
            "arbiter_review_rows": len(arbiter_results),
            "accepted_internal_candidates": len(
                [
                    row
                    for row in mass_results
                    if row["decision"] == "accept_internal_claim_candidate"
                ]
            ),
            "arbiter_accepted_internal_candidates": len(
                [
                    row
                    for row in arbiter_results
                    if row["decision"] == "accept_internal_claim_candidate"
                ]
            ),
            "needs_human_review": len(
                [row for row in mass_results if row["decision"] == "needs_human_review"]
            ),
            "context_only": len(
                [row for row in mass_results if row["decision"] == "context_only"]
            ),
            "reject_noise": len(
                [row for row in mass_results if row["decision"] == "reject_noise"]
            ),
            "unable_to_review": len(
                [row for row in mass_results if row["decision"] == "unable_to_review"]
            ),
        },
        "channel_summaries": channels,
    }


def render_report(artifact: dict[str, Any]) -> str:
    summary = artifact["summary"]
    lines = [
        "# Three-Channel Media Reviewer Report",
        "",
        f"Date: {summary['generated_at_utc']}",
        f"Status: `{summary['status']}`",
        "",
        "## Models",
        "",
        f"- Mass reviewer: `{summary['models']['mass_review_model']}`",
        f"- Arbiter reviewer: `{summary['models']['arbiter_model']}`",
        "",
        "## Boundary",
        "",
        "- Mass reviewer checks every transcript/OCR draft row.",
        "- Arbiter reviewer checks only high-signal or disputed rows.",
        "- Image rows include the source image; voice rows use the transcript draft.",
        "- Model review is internal only and does not approve customer-facing metrics.",
        "",
        "## Totals",
        "",
    ]
    for key, value in summary["totals"].items():
        lines.append(f"- `{key}`: {value}")
    lines.extend(
        [
            "",
            "## Channel Comparison",
            "",
            "| channel | mass rows | mass accepted | arbiter accepted | needs human | context only | reject noise | avg usefulness | top evidence types | arbiter rows |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---|---:|",
        ]
    )
    for row in summary["channel_summaries"]:
        evidence = (
            ", ".join(
                f"{key}:{value}"
                for key, value in Counter(row["evidence_types"]).most_common(5)
            )
            or "-"
        )
        decisions = Counter(row["mass_decisions"])
        lines.append(
            "| `{source_id}` | {mass_review_rows} | {accepted_internal_candidates} | {arbiter_accepted_internal_candidates} | {needs_human} | {context_only} | {reject_noise} | {avg_usefulness_score} | {evidence} | {arbiter_review_rows} |".format(
                **row,
                needs_human=decisions.get("needs_human_review", 0),
                context_only=decisions.get("context_only", 0),
                reject_noise=decisions.get("reject_noise", 0),
                evidence=evidence,
            )
        )
    lines.extend(["", "## High-Signal Examples", ""])
    examples = sorted(
        [
            row
            for row in artifact["mass_reviews"]
            if row["decision"] == "accept_internal_claim_candidate"
        ],
        key=lambda row: (row["usefulness_score"], row["confidence"]),
        reverse=True,
    )[:15]
    if not examples:
        lines.append("- none")
    else:
        lines.append("| channel | post | modality | score | evidence types | summary |")
        lines.append("|---|---:|---|---:|---|---|")
        for row in examples:
            lines.append(
                "| `{source_id}` | [{post_id}]({source_url}) | {modality} | {usefulness_score} | {types} | {summary} |".format(
                    **row,
                    types=", ".join(row["evidence_types"]) or "-",
                    summary=escape_table(row["review_summary"]),
                )
            )
    lines.extend(["", "## Arbiter-Accepted Examples", ""])
    arbiter_examples = sorted(
        [
            row
            for row in artifact["arbiter_reviews"]
            if row["decision"] == "accept_internal_claim_candidate"
        ],
        key=lambda row: (row["usefulness_score"], row["confidence"]),
        reverse=True,
    )[:15]
    if not arbiter_examples:
        lines.append("- none")
    else:
        lines.append("| channel | post | modality | score | evidence types | summary |")
        lines.append("|---|---:|---|---:|---|---|")
        for row in arbiter_examples:
            lines.append(
                "| `{source_id}` | [{post_id}]({source_url}) | {modality} | {usefulness_score} | {types} | {summary} |".format(
                    **row,
                    types=", ".join(row["evidence_types"]) or "-",
                    summary=escape_table(row["review_summary"]),
                )
            )
    lines.extend(
        [
            "",
            "## Gate",
            "",
            "- Decision: `internal_research_only`.",
            "- Reason: these are model reviews, not human/operator accepted evidence.",
        ]
    )
    return "\n".join(lines) + "\n"


def image_data_url(path: Path, mime_type: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def nullable_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.lower() == "null":
        return None
    return shorten(text, 120)


def clamp_float(value: Any, *, default: float, low: float, high: float) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return max(low, min(high, parsed))


def avg_score(rows: list[dict[str, Any]]) -> str | None:
    if not rows:
        return None
    return f"{sum(row['usefulness_score'] for row in rows) / len(rows):.3f}"


def stable_review_id(row: dict[str, Any], reviewer_tier: str, model: str) -> str:
    digest = hashlib.sha256(
        f"{row['media_ref_id']}:{reviewer_tier}:{model}".encode()
    ).hexdigest()
    return f"media_review_{digest[:16]}"


def shorten(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def evidence_excerpt(text: str, *, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    head_limit = min(1400, max(500, limit // 2))
    parts = [text[:head_limit]]
    keyword_re = re.compile(
        r"(?i)(стоп|цель|тейк|target|entry|вход|rr|risk|лонг|шорт|покуп|прода|"
        r"позици|рынок|нефть|газ|биткоин|btc|eth|магнит|аэрофлот|сбер)"
    )
    seen_ranges: list[tuple[int, int]] = [(0, head_limit)]
    for match in keyword_re.finditer(text):
        start = max(0, match.start() - 280)
        end = min(len(text), match.end() + 360)
        if any(abs(start - seen_start) < 120 for seen_start, _ in seen_ranges):
            continue
        seen_ranges.append((start, end))
        parts.append(text[start:end])
        excerpt = " ... ".join(parts)
        if len(excerpt) >= limit:
            return excerpt[: limit - 1].rstrip() + "…"
    return (" ... ".join(parts))[: limit - 1].rstrip() + "…"


def compact_prior_review(review: dict[str, Any] | None) -> dict[str, Any] | None:
    if review is None:
        return None
    return {
        key: review.get(key)
        for key in (
            "decision",
            "evidence_types",
            "assets",
            "direction",
            "entry",
            "stop",
            "targets",
            "position_size",
            "explicit_rr",
            "confidence",
            "usefulness_score",
            "review_summary",
            "blockers",
        )
    }


def escape_table(value: str) -> str:
    return value.replace("|", "\\|")


def now_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue-json", type=Path, default=DEFAULT_QUEUE_JSON)
    parser.add_argument("--manifest-json", type=Path, default=DEFAULT_MANIFEST_JSON)
    parser.add_argument("--rr-json", type=Path, default=DEFAULT_RR_JSON)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--review-model", default=None)
    parser.add_argument("--arbiter-model", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--arbiter-max-items", type=int, default=35)
    parser.add_argument("--review-concurrency", type=int, default=3)
    parser.add_argument("--arbiter-concurrency", type=int, default=1)
    parser.add_argument("--text-limit", type=int, default=3500)
    args = parser.parse_args()

    load_dotenv()
    review_model = args.review_model or os.environ.get(
        REVIEW_MODEL_ENV,
        DEFAULT_REVIEW_MODEL,
    )
    arbiter_model = args.arbiter_model or os.environ.get(
        ARBITER_MODEL_ENV,
        DEFAULT_ARBITER_MODEL,
    )
    if not os.environ.get(OPENAI_API_KEY_ENV):
        raise RuntimeError(f"{OPENAI_API_KEY_ENV} is required")

    queue, manifest_by_id, rr_by_document = load_inputs(
        queue_path=args.queue_json,
        manifest_path=args.manifest_json,
        rr_path=args.rr_json,
    )
    rows = reviewable_rows(queue, limit=args.limit)
    mass_results = run_mass_review(
        rows,
        manifest_by_id=manifest_by_id,
        rr_by_document=rr_by_document,
        model=review_model,
        concurrency=args.review_concurrency,
        text_limit=args.text_limit,
    )
    rows_by_id = {row["media_ref_id"]: row for row in rows}
    arbiter_results = run_arbiter_review(
        mass_results,
        rows_by_id=rows_by_id,
        manifest_by_id=manifest_by_id,
        rr_by_document=rr_by_document,
        model=arbiter_model,
        concurrency=args.arbiter_concurrency,
        max_items=args.arbiter_max_items,
        text_limit=args.text_limit,
    )
    summary = summarize(
        mass_results=mass_results,
        arbiter_results=arbiter_results,
        review_model=review_model,
        arbiter_model=arbiter_model,
        review_rows_total=len(rows),
        arbiter_max_items=args.arbiter_max_items,
    )
    artifact = {
        "summary": summary,
        "mass_reviews": mass_results,
        "arbiter_reviews": arbiter_results,
    }
    write_json(args.output_json, artifact)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(render_report(artifact), encoding="utf-8")
    print(f"Wrote {args.output_json}")
    print(f"Wrote {args.output_md}")


if __name__ == "__main__":
    main()
