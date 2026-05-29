from __future__ import annotations

# ruff: noqa: E501
import argparse
import base64
import hashlib
import html
import importlib
import json
import mimetypes
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from three_channel_metric_report import (
    CHANNELS,
    USER_AGENT,
    claim_type,
    detect_assets,
    detect_direction,
    fetch,
    filter_rows_by_date,
    previous_before_id,
    q,
    strip_tags,
)

DEFAULT_START_DATE = date(2026, 3, 22)
DEFAULT_END_DATE = date(2026, 5, 22)
DEFAULT_CAPTURE_DIR = Path("workspace/media/three_channel_multimodal")
DEFAULT_TRANSCRIPT_DIR = Path("docs/pilot/multimodal/transcripts")
DEFAULT_OCR_DIR = Path("docs/pilot/multimodal/ocr")
DEFAULT_MANIFEST_JSON = Path("docs/pilot/three_channel_MULTIMODAL_MEDIA_MANIFEST.json")
DEFAULT_QUEUE_JSON = Path("docs/pilot/three_channel_MULTIMODAL_PROCESSING_QUEUE.json")
DEFAULT_RR_JSON = Path("docs/pilot/three_channel_MULTIMODAL_RR_DRAFTS.json")
DEFAULT_REPORT_MD = Path("docs/pilot/three_channel_MULTIMODAL_RESEARCH_REPORT.md")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
TRANSCRIPTION_MODEL_ENV = "SIGNAL_SANDBOX_TRANSCRIPTION_MODEL"
VISION_MODEL_ENV = "SIGNAL_SANDBOX_VISION_MODEL"
DEFAULT_TRANSCRIPTION_MODEL = "whisper-1"
DEFAULT_VISION_MODEL = "gpt-4o-mini"

CDN_FILE_RE = re.compile(
    r"""(?x)
    (?P<url>
        (?:https?:)?//cdn\d*\.telesco\.pe/file/[^"'\s<>)]+
        |
        (?:https?:)?//cdn\d*\.telegram-cdn\.org/file/[^"'\s<>)]+
    )
    """
)
PHOTO_TAG_RE = re.compile(
    r"""(?xs)
    <a\b(?=[^>]*tgme_widget_message_photo_wrap)[^>]*>
    |
    <a\b(?=[^>]*tgme_widget_message_video_player)[^>]*>
    """
)
BACKGROUND_URL_RE = re.compile(r"background-image:url\(['\"]?([^'\")]+)['\"]?\)")
TEXT_DIV_RE = re.compile(
    r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>',
    flags=re.S,
)
TIME_RE = re.compile(r'<time datetime="([^"]+)"')
POST_RE_TEMPLATE = r'data-post="{channel}/(\d+)\"'
ENTRY_RE = re.compile(
    r"(?i)(?:entry|entries|вход|зона входа|точка входа|войти|открыт\w*|набор|покупк\w*|buy)\D{0,24}([0-9][0-9\s.,]{1,18})"
)
STOP_RE = re.compile(
    r"(?i)(?:stop|стоп|sl\b|инвалид|отмен[аы]|риск)\D{0,24}([0-9][0-9\s.,]{1,18})"
)
TARGET_RE = re.compile(
    r"(?i)(?:\btarget\b|\btargets\b|цель|цели|тейк|take\s*profit|\btp\d*\b|таргет)\D{0,24}([0-9][0-9\s.,]{1,18})"
)
POSITION_SIZE_RE = re.compile(
    r"(?i)(?:размер позиции|position size|риск на сделку|risk per trade|депо|портфел[ья])\D{0,24}([0-9]+(?:[.,][0-9]+)?\s*%?)"
)
EXPLICIT_RR_RE = re.compile(
    r"(?i)(?:rr|r/r|risk\s*/\s*reward|риск\s*/\s*прибыль|риск.?ревард)\D{0,12}([0-9]+(?:[.,][0-9]+)?)"
)


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


def fetch_public_posts_with_segments(
    channel: str, max_pages: int
) -> list[dict[str, Any]]:
    before_id = None
    seen: dict[int, dict[str, Any]] = {}
    for _ in range(max_pages):
        url = f"https://t.me/s/{channel}"
        if before_id is not None:
            url = f"{url}?before={before_id}"
        body = fetch_with_retry(url)
        for row in parse_page_with_media(channel, body):
            seen[row["post_id"]] = row
        next_before_id = previous_before_id(body)
        if next_before_id is None or next_before_id == before_id:
            break
        before_id = next_before_id
    return sorted(seen.values(), key=lambda row: row["post_id"])


def fetch_with_retry(url: str, *, attempts: int = 4) -> str:
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            return fetch(url)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt == attempts:
                break
            time.sleep(min(2**attempt, 10))
    raise RuntimeError(
        f"public fetch failed after {attempts} attempts: {url}"
    ) from last_error


def parse_page_with_media(channel: str, body: str) -> list[dict[str, Any]]:
    rows = []
    pattern = re.compile(POST_RE_TEMPLATE.format(channel=re.escape(channel)))
    for match in pattern.finditer(body):
        start = max(0, body.rfind("<div", 0, match.start()))
        end = body.find("tgme_widget_message_wrap", match.end())
        if end == -1:
            end = len(body)
        segment = body[start:end]
        post_id = int(match.group(1))
        time_match = TIME_RE.search(segment)
        text_chunks = TEXT_DIV_RE.findall(segment)
        text = "\n".join(strip_tags(chunk) for chunk in text_chunks).strip()
        media_refs = extract_media_refs(channel, post_id, segment)
        rows.append(
            {
                "source_id": channel,
                "post_id": post_id,
                "timestamp_utc": time_match.group(1) if time_match else None,
                "source_url": f"https://t.me/{channel}/{post_id}",
                "source_document_id": f"{channel}:{channel}-{post_id}",
                "text": text,
                "media_refs": media_refs,
            }
        )
    return rows


def extract_media_refs(
    channel: str,
    post_id: int,
    segment: str,
) -> list[dict[str, Any]]:
    refs = []
    seen: set[str] = set()
    candidates: list[tuple[str, str]] = []
    for tag_match in PHOTO_TAG_RE.finditer(segment):
        tag = tag_match.group(0)
        bg_match = BACKGROUND_URL_RE.search(tag)
        if bg_match is None:
            continue
        modality = "video" if "tgme_widget_message_video_player" in tag else "image"
        candidates.append((bg_match.group(1), modality))
    for match in CDN_FILE_RE.finditer(segment):
        url = normalize_url(match.group("url"))
        if ".ogg" in url.lower():
            candidates.append((url, "voice"))
        elif ".mp4" in url.lower():
            candidates.append((url, "video"))

    for index, candidate in enumerate(candidates, start=1):
        raw_url, modality = candidate
        url = normalize_url(raw_url)
        if not is_supported_public_media_url(url) or url in seen:
            continue
        seen.add(url)
        refs.append(
            {
                "media_ref_id": stable_media_ref_id(channel, post_id, index, url),
                "source_id": channel,
                "post_id": post_id,
                "modality": modality,
                "original_url": url,
            }
        )
    return refs


def normalize_url(raw_url: str) -> str:
    value = html.unescape(raw_url).strip()
    if value.startswith("//"):
        value = "https:" + value
    return value


def is_supported_public_media_url(url: str) -> bool:
    if "emoji" in url or "telegram.org/img" in url:
        return False
    parsed = urllib.parse.urlparse(url)
    return parsed.scheme in {"http", "https"} and (
        parsed.netloc.endswith("telesco.pe")
        or parsed.netloc.endswith("telegram-cdn.org")
        or parsed.netloc.startswith("cdn")
    )


def infer_modality(url: str, segment: str) -> str:
    lowered = url.lower()
    if ".ogg" in lowered or "tgme_widget_message_voice" in segment:
        return "voice"
    if ".mp4" in lowered or "tgme_widget_message_video" in segment:
        return "video"
    if any(ext in lowered for ext in (".jpg", ".jpeg", ".png", ".webp")):
        return "image"
    if "tgme_widget_message_photo_wrap" in segment:
        return "image"
    return "other"


def stable_media_ref_id(channel: str, post_id: int, index: int, url: str) -> str:
    digest = hashlib.sha256(f"{channel}:{post_id}:{index}:{url}".encode()).hexdigest()
    return f"media_{digest[:16]}"


def build_media_manifest(
    posts_by_channel: dict[str, list[dict[str, Any]]],
    *,
    capture_dir: Path,
    download_media: bool,
) -> list[dict[str, Any]]:
    rows = []
    created_at = now_utc()
    for channel, posts in posts_by_channel.items():
        for post in posts:
            for index, ref in enumerate(post["media_refs"], start=1):
                downloaded = (
                    download_media_file(
                        ref,
                        post,
                        index=index,
                        capture_dir=capture_dir / channel,
                    )
                    if download_media
                    else download_skipped_row(ref)
                )
                rows.append(
                    {
                        **ref,
                        "capture_id": f"{channel}-{post['post_id']}",
                        "source_document_id": post["source_document_id"],
                        "source_url": post["source_url"],
                        "timestamp_utc": post["timestamp_utc"],
                        "download_status": downloaded["download_status"],
                        "local_path": downloaded.get("local_path"),
                        "media_sha256": downloaded.get("media_sha256"),
                        "mime_type": downloaded.get("mime_type"),
                        "bytes": downloaded.get("bytes"),
                        "error": downloaded.get("error"),
                        "created_at_utc": created_at,
                    }
                )
    return sorted(
        rows, key=lambda row: (row["source_id"], row["post_id"], row["media_ref_id"])
    )


def download_skipped_row(_ref: dict[str, Any]) -> dict[str, Any]:
    return {"download_status": "skipped_download_disabled"}


def download_media_file(
    ref: dict[str, Any],
    post: dict[str, Any],
    *,
    index: int,
    capture_dir: Path,
) -> dict[str, Any]:
    capture_dir.mkdir(parents=True, exist_ok=True)
    suffix = suffix_for_url(ref["original_url"], ref["modality"])
    local_path = (
        capture_dir
        / f"{post['source_id']}-{post['post_id']}-{index:02d}-{ref['media_ref_id']}{suffix}"
    )
    if local_path.exists():
        data = local_path.read_bytes()
        return {
            "download_status": "reused_existing",
            "local_path": str(local_path),
            "media_sha256": hashlib.sha256(data).hexdigest(),
            "mime_type": mimetypes.guess_type(str(local_path))[0]
            or "application/octet-stream",
            "bytes": len(data),
        }

    request = urllib.request.Request(
        ref["original_url"],
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=45) as response:
            data = response.read()
            mime_type = response.headers.get_content_type()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {
            "download_status": "download_failed",
            "error": type(exc).__name__,
        }
    local_path.write_bytes(data)
    return {
        "download_status": "downloaded",
        "local_path": str(local_path),
        "media_sha256": hashlib.sha256(data).hexdigest(),
        "mime_type": mime_type
        or mimetypes.guess_type(str(local_path))[0]
        or "application/octet-stream",
        "bytes": len(data),
    }


def suffix_for_url(url: str, modality: str) -> str:
    parsed = urllib.parse.urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix:
        return suffix
    return {
        "voice": ".ogg",
        "audio": ".ogg",
        "video": ".mp4",
        "image": ".jpg",
    }.get(modality, ".bin")


def run_processing_queue(
    media_manifest: list[dict[str, Any]],
    *,
    enable_openai: bool,
    transcript_dir: Path,
    ocr_dir: Path,
    max_provider_items: int | None,
    provider_concurrency: int,
) -> tuple[list[dict[str, Any]], dict[str, str]]:
    load_dotenv()
    provider_state = {
        "openai_api_key": "present"
        if os.environ.get(OPENAI_API_KEY_ENV)
        else "missing",
        "transcription_model": os.environ.get(
            TRANSCRIPTION_MODEL_ENV,
            DEFAULT_TRANSCRIPTION_MODEL,
        ),
        "vision_model": os.environ.get(VISION_MODEL_ENV, DEFAULT_VISION_MODEL),
        "openai_enabled": str(enable_openai),
    }
    queue = []
    pending: list[tuple[int, dict[str, Any], str]] = []
    provider_slots = 0
    for index, row in enumerate(media_manifest):
        action = planned_media_action(row)
        result: dict[str, Any] = {
            "media_ref_id": row["media_ref_id"],
            "source_id": row["source_id"],
            "post_id": row["post_id"],
            "source_document_id": row["source_document_id"],
            "source_url": row["source_url"],
            "modality": row["modality"],
            "download_status": row["download_status"],
            "planned_action": action,
            "status": "blocked",
            "artifact_path": None,
            "extracted_text": None,
            "error": None,
        }
        if row["download_status"] not in {"downloaded", "reused_existing"}:
            result["status"] = "blocked_media_not_downloaded"
        elif action == "unsupported_video_manual_review":
            result["status"] = "blocked_video_manual_review_required"
        elif not enable_openai:
            result["status"] = "blocked_openai_disabled"
        elif not os.environ.get(OPENAI_API_KEY_ENV):
            result["status"] = "blocked_missing_openai_api_key"
        elif max_provider_items is not None and provider_slots >= max_provider_items:
            result["status"] = "blocked_provider_item_limit"
        elif action in {"transcribe_audio", "vision_ocr_image"}:
            provider_slots += 1
            pending.append((index, row, action))
        else:
            result["status"] = "blocked_unsupported_modality"
        queue.append(result)

    if pending:
        with ThreadPoolExecutor(max_workers=max(1, provider_concurrency)) as executor:
            futures = {
                executor.submit(
                    process_provider_row,
                    row,
                    action,
                    transcript_dir=transcript_dir,
                    ocr_dir=ocr_dir,
                    transcription_model=provider_state["transcription_model"],
                    vision_model=provider_state["vision_model"],
                ): index
                for index, row, action in pending
            }
            completed = 0
            for future in as_completed(futures):
                index = futures[future]
                try:
                    queue[index].update(future.result())
                except Exception as exc:
                    queue[index].update(
                        {"status": "provider_failed", "error": type(exc).__name__}
                    )
                completed += 1
                if completed == 1 or completed % 25 == 0 or completed == len(pending):
                    print(f"provider_progress {completed}/{len(pending)}")
    return queue, provider_state


def openai_client() -> Any:
    openai_module = importlib.import_module("openai")
    return openai_module.OpenAI(api_key=os.environ[OPENAI_API_KEY_ENV])


def process_provider_row(
    row: dict[str, Any],
    action: str,
    *,
    transcript_dir: Path,
    ocr_dir: Path,
    transcription_model: str,
    vision_model: str,
) -> dict[str, Any]:
    client = openai_client()
    if action == "transcribe_audio":
        return transcribe_audio_row(
            client,
            row,
            output_dir=transcript_dir,
            model=transcription_model,
        )
    if action == "vision_ocr_image":
        return vision_ocr_row(
            client,
            row,
            output_dir=ocr_dir,
            model=vision_model,
        )
    return {"status": "blocked_unsupported_modality"}


def planned_media_action(row: dict[str, Any]) -> str:
    if row["modality"] in {"voice", "audio"}:
        return "transcribe_audio"
    if row["modality"] == "image":
        return "vision_ocr_image"
    if row["modality"] == "video":
        return "unsupported_video_manual_review"
    return "unsupported_modality"


def transcribe_audio_row(
    client: Any,
    row: dict[str, Any],
    *,
    output_dir: Path,
    model: str,
) -> dict[str, Any]:
    local_path = row.get("local_path")
    if not local_path:
        return {"status": "blocked_media_not_downloaded"}
    path = Path(local_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / f"{row['media_ref_id']}.json"
    if artifact_path.exists():
        existing = json.loads(artifact_path.read_text(encoding="utf-8"))
        return {
            "status": existing.get("status", "draft_pending_review"),
            "artifact_path": str(artifact_path),
            "extracted_text": existing.get("transcript_text", ""),
        }
    try:
        with path.open("rb") as audio_file:
            response = client.audio.transcriptions.create(model=model, file=audio_file)
    except Exception as exc:
        return {"status": "provider_failed", "error": type(exc).__name__}
    text = getattr(response, "text", "").strip()
    if not text:
        return {"status": "provider_empty", "error": "empty_transcript"}
    artifact = {
        "artifact_id": row["media_ref_id"],
        "artifact_type": "audio_transcript_draft",
        "source_id": row["source_id"],
        "post_id": row["post_id"],
        "source_document_id": row["source_document_id"],
        "source_url": row["source_url"],
        "media_sha256": row.get("media_sha256"),
        "provider": "openai",
        "model": model,
        "transcript_text": text,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "status": "draft_pending_review",
        "review_required": True,
        "created_at_utc": now_utc(),
    }
    artifact_path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "status": "draft_pending_review",
        "artifact_path": str(artifact_path),
        "extracted_text": text,
    }


def vision_ocr_row(
    client: Any,
    row: dict[str, Any],
    *,
    output_dir: Path,
    model: str,
) -> dict[str, Any]:
    local_path = row.get("local_path")
    if not local_path:
        return {"status": "blocked_media_not_downloaded"}
    path = Path(local_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / f"{row['media_ref_id']}.json"
    if artifact_path.exists():
        existing = json.loads(artifact_path.read_text(encoding="utf-8"))
        return {
            "status": existing.get("status", "draft_pending_review"),
            "artifact_path": str(artifact_path),
            "extracted_text": existing.get("text", ""),
        }
    data_url = image_data_url(path, row.get("mime_type") or "image/jpeg")
    prompt = (
        "Extract only visible market/trading information from this Telegram image/chart. "
        "Return compact JSON with keys: visible_text, assets, directions, entry, stop, targets, "
        "position_size, explicit_rr, timeframe, risk_notes, uncertainty. "
        "Do not infer hidden chart meaning; if levels are visual-only, put them in uncertainty."
    )
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": data_url}},
                    ],
                }
            ],
            temperature=0,
        )
    except Exception as exc:
        return {"status": "provider_failed", "error": type(exc).__name__}
    text = response.choices[0].message.content.strip()
    if not text:
        return {"status": "provider_empty", "error": "empty_vision_response"}
    artifact = {
        "artifact_id": row["media_ref_id"],
        "artifact_type": "image_ocr_vision_draft",
        "source_id": row["source_id"],
        "post_id": row["post_id"],
        "source_document_id": row["source_document_id"],
        "source_url": row["source_url"],
        "media_sha256": row.get("media_sha256"),
        "provider": "openai",
        "model": model,
        "text": text,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "status": "draft_pending_review",
        "review_required": True,
        "created_at_utc": now_utc(),
    }
    artifact_path.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "status": "draft_pending_review",
        "artifact_path": str(artifact_path),
        "extracted_text": text,
    }


def image_data_url(path: Path, mime_type: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_rr_drafts(
    posts_by_channel: dict[str, list[dict[str, Any]]],
    processing_queue: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    media_text_by_document: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in processing_queue:
        text = (row.get("extracted_text") or "").strip()
        if row.get("status") != "draft_pending_review" or not text:
            continue
        media_text_by_document[row["source_document_id"]].append(
            {
                "media_ref_id": row["media_ref_id"],
                "modality": row["modality"],
                "text": text,
            }
        )

    drafts = []
    for channel, posts in posts_by_channel.items():
        for post in posts:
            parts = []
            if post["text"]:
                parts.append(
                    {
                        "kind": "post_text",
                        "ref": post["source_url"],
                        "text": post["text"],
                    }
                )
            parts.extend(media_text_by_document.get(post["source_document_id"], []))
            combined_text = "\n\n".join(part["text"] for part in parts if part["text"])
            if not combined_text.strip():
                continue
            assets = detect_assets(combined_text, source_id=channel)
            direction = detect_direction(combined_text)
            setup = extract_setup_fields(combined_text, direction)
            blockers = setup_blockers(setup, assets, direction, parts)
            rr_blockers = rr_blocking_reasons(blockers)
            drafts.append(
                {
                    "source_id": channel,
                    "post_id": post["post_id"],
                    "source_document_id": post["source_document_id"],
                    "source_url": post["source_url"],
                    "timestamp_utc": post["timestamp_utc"],
                    "evidence_parts": [
                        {
                            "kind": part.get("kind", part.get("modality", "media")),
                            "ref": part.get("ref", part.get("media_ref_id", "")),
                        }
                        for part in parts
                    ],
                    "asset_candidates": assets,
                    "direction": direction,
                    "claim_type": claim_type(combined_text),
                    "entry": decimal_to_str(setup.get("entry")),
                    "stop": decimal_to_str(setup.get("stop")),
                    "targets": [decimal_to_str(item) for item in setup["targets"]],
                    "position_size": setup.get("position_size"),
                    "explicit_rr": decimal_to_str(setup.get("explicit_rr")),
                    "computed_rr": decimal_to_str(setup.get("computed_rr")),
                    "rr_status": (
                        "rr_ready_internal_draft" if not rr_blockers else "rr_blocked"
                    ),
                    "customer_metric_status": customer_metric_status(blockers),
                    "blockers": blockers,
                    "rr_blockers": rr_blockers,
                    "snippet": re.sub(r"\s+", " ", combined_text)[:320],
                }
            )
    return sorted(drafts, key=lambda row: (row["source_id"], row["post_id"]))


def extract_setup_fields(text: str, direction: str) -> dict[str, Any]:
    field_text = strip_urls(text)
    entry = first_decimal(ENTRY_RE, field_text)
    stop = first_decimal(STOP_RE, field_text)
    targets = [
        value for value in all_decimals(TARGET_RE, field_text) if value is not None
    ]
    explicit_rr = first_decimal(EXPLICIT_RR_RE, field_text)
    computed_rr = compute_rr(direction, entry, stop, targets[0] if targets else None)
    return {
        "entry": entry,
        "stop": stop,
        "targets": targets,
        "position_size": first_group(POSITION_SIZE_RE, text),
        "explicit_rr": explicit_rr,
        "computed_rr": computed_rr,
    }


def strip_urls(text: str) -> str:
    return re.sub(r"https?://\S+", " ", text)


def setup_blockers(
    setup: dict[str, Any],
    assets: list[dict[str, str]],
    direction: str,
    parts: list[dict[str, str]],
) -> list[str]:
    blockers = []
    if not assets:
        blockers.append("missing_supported_asset")
    if direction not in {"long", "short"}:
        blockers.append("missing_single_direction")
    if setup.get("entry") is None:
        blockers.append("missing_entry")
    if setup.get("stop") is None:
        blockers.append("missing_stop")
    if not setup.get("targets"):
        blockers.append("missing_target")
    if setup.get("position_size") is None:
        blockers.append("position_size_missing")
    if setup.get("computed_rr") is None and setup.get("explicit_rr") is None:
        blockers.append("rr_not_computable")
    if any(part.get("kind") != "post_text" for part in parts):
        blockers.append("media_review_required_before_customer_metrics")
    return blockers


def rr_blocking_reasons(blockers: list[str]) -> list[str]:
    non_rr_blockers = {
        "position_size_missing",
        "media_review_required_before_customer_metrics",
    }
    return [blocker for blocker in blockers if blocker not in non_rr_blockers]


def customer_metric_status(blockers: list[str]) -> str:
    if "media_review_required_before_customer_metrics" in blockers:
        return "blocked_media_review_required"
    if blockers:
        return "blocked_missing_setup_fields"
    return "eligible_after_external_gate"


def first_decimal(pattern: re.Pattern[str], text: str) -> Decimal | None:
    match = pattern.search(text)
    if match is None:
        return None
    return parse_decimal(match.group(1))


def all_decimals(pattern: re.Pattern[str], text: str) -> list[Decimal]:
    values = []
    for match in pattern.finditer(text):
        value = parse_decimal(match.group(1))
        if value is not None:
            values.append(value)
    return values


def first_group(pattern: re.Pattern[str], text: str) -> str | None:
    match = pattern.search(text)
    if match is None:
        return None
    return re.sub(r"\s+", " ", match.group(1)).strip()


def parse_decimal(raw: str) -> Decimal | None:
    value = re.sub(r"\s+", "", raw).replace(",", ".")
    value = re.sub(r"[^0-9.%-]", "", value).rstrip("%")
    if not value or value.count(".") > 1:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None


def compute_rr(
    direction: str,
    entry: Decimal | None,
    stop: Decimal | None,
    target: Decimal | None,
) -> Decimal | None:
    if (
        direction not in {"long", "short"}
        or entry is None
        or stop is None
        or target is None
    ):
        return None
    if direction == "long":
        risk = entry - stop
        reward = target - entry
    else:
        risk = stop - entry
        reward = entry - target
    if risk <= 0 or reward <= 0:
        return None
    return q(reward / risk)


def decimal_to_str(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return str(q(value))


def summarize_artifacts(
    posts_by_channel: dict[str, list[dict[str, Any]]],
    media_manifest: list[dict[str, Any]],
    processing_queue: list[dict[str, Any]],
    rr_drafts: list[dict[str, Any]],
    provider_state: dict[str, str],
    *,
    start_date: date | None,
    end_date: date | None,
    max_pages: int,
) -> dict[str, Any]:
    channels = []
    for channel in CHANNELS:
        posts = posts_by_channel[channel]
        media_rows = [row for row in media_manifest if row["source_id"] == channel]
        queue_rows = [row for row in processing_queue if row["source_id"] == channel]
        drafts = [row for row in rr_drafts if row["source_id"] == channel]
        channels.append(
            {
                "source_id": channel,
                "posts": len(posts),
                "text_rows": len([row for row in posts if row["text"]]),
                "posts_with_media": len([row for row in posts if row["media_refs"]]),
                "media_rows": len(media_rows),
                "media_by_modality": dict(
                    Counter(row["modality"] for row in media_rows)
                ),
                "download_status_counts": dict(
                    Counter(row["download_status"] for row in media_rows)
                ),
                "processing_status_counts": dict(
                    Counter(row["status"] for row in queue_rows)
                ),
                "rr_drafts": len(drafts),
                "rr_ready": len(
                    [
                        row
                        for row in drafts
                        if row["rr_status"] == "rr_ready_internal_draft"
                    ]
                ),
                "rr_blockers": dict(
                    Counter(blocker for row in drafts for blocker in row["blockers"])
                ),
            }
        )
    return {
        "artifact_id": "three-channel-multimodal-research",
        "generated_at_utc": now_utc(),
        "status": "internal_multimodal_research_draft",
        "method": {
            "source_method": "public_telegram_s_html",
            "max_pages_per_channel": max_pages,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "raw_media_dir": str(DEFAULT_CAPTURE_DIR),
            "customer_facing": False,
            "media_claim_policy": "draft_pending_review_only_until_human_operator_acceptance",
        },
        "provider_state": provider_state,
        "totals": {
            "posts": sum(row["posts"] for row in channels),
            "text_rows": sum(row["text_rows"] for row in channels),
            "posts_with_media": sum(row["posts_with_media"] for row in channels),
            "media_rows": len(media_manifest),
            "draft_transcript_or_ocr_rows": len(
                [
                    row
                    for row in processing_queue
                    if row["status"] == "draft_pending_review"
                ]
            ),
            "rr_drafts": len(rr_drafts),
            "rr_ready": len(
                [
                    row
                    for row in rr_drafts
                    if row["rr_status"] == "rr_ready_internal_draft"
                ]
            ),
        },
        "channel_summaries": channels,
    }


def render_report(
    summary: dict[str, Any],
    *,
    manifest_path: Path,
    queue_path: Path,
    rr_path: Path,
) -> str:
    lines = [
        "# Three-Channel Multimodal Research Report",
        "",
        f"Date: {summary['generated_at_utc']}",
        f"Status: `{summary['status']}`",
        "",
        "## Boundary",
        "",
        "- Sources: public Telegram `/s/` HTML only.",
        "- Media scope: public image/voice/audio refs visible in those pages.",
        "- Raw media is stored under `workspace/` and is not intended for git commit.",
        "- Transcript/OCR rows are `draft_pending_review`; they are not customer-facing metrics until human/operator accepted.",
        "- RR fields are populated only from extracted evidence text; missing entry/stop/target/size remains explicit blocker.",
        "",
        "## Artifacts",
        "",
        f"- Media manifest JSON: `{manifest_path}`",
        f"- Processing queue JSON: `{queue_path}`",
        f"- RR draft JSON: `{rr_path}`",
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
            "| channel | posts | text rows | posts with media | media rows | media by modality | draft transcript/OCR | RR drafts | RR ready | top RR blockers |",
            "|---|---:|---:|---:|---:|---|---:|---:|---:|---|",
        ]
    )
    for channel in summary["channel_summaries"]:
        draft_count = channel["processing_status_counts"].get("draft_pending_review", 0)
        blockers = (
            ", ".join(
                f"{key}:{value}"
                for key, value in Counter(channel["rr_blockers"]).most_common(5)
            )
            or "-"
        )
        modalities = (
            ", ".join(
                f"{key}:{value}"
                for key, value in sorted(channel["media_by_modality"].items())
            )
            or "-"
        )
        lines.append(
            "| `{source_id}` | {posts} | {text_rows} | {posts_with_media} | {media_rows} | {modalities} | {draft_count} | {rr_drafts} | {rr_ready} | {blockers} |".format(
                **channel,
                modalities=modalities,
                draft_count=draft_count,
                blockers=blockers,
            )
        )
    lines.extend(
        [
            "",
            "## What This Means",
            "",
            "- The previous two-month run measured text-only directional calls. This run adds media intake and draft extraction.",
            "- A channel can have many useful media notes while still producing few RR-ready trades if author posts theses, regimes, screenshots, or voice commentary without explicit entry/stop/target.",
            "- `rr_ready` is intentionally strict for internal quant review: it requires supported asset, single direction, entry, stop, target, and computable or explicit RR.",
            "- Missing position size and media-review status are tracked separately because they matter for paid/customer-facing use but should not erase an otherwise measurable RR setup.",
            "- `position_size_missing` is tracked separately because most public calls do not reveal actual allocation.",
            "",
            "## Gate",
            "",
            "- Decision: `internal_research_only`.",
            "- Reason: transcript/OCR needs human/operator acceptance before any paid/customer-facing metric.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def now_utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=40)
    parser.add_argument(
        "--start-date", type=date.fromisoformat, default=DEFAULT_START_DATE
    )
    parser.add_argument("--end-date", type=date.fromisoformat, default=DEFAULT_END_DATE)
    parser.add_argument("--capture-dir", type=Path, default=DEFAULT_CAPTURE_DIR)
    parser.add_argument("--manifest-json", type=Path, default=DEFAULT_MANIFEST_JSON)
    parser.add_argument("--queue-json", type=Path, default=DEFAULT_QUEUE_JSON)
    parser.add_argument("--rr-json", type=Path, default=DEFAULT_RR_JSON)
    parser.add_argument("--report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--transcript-dir", type=Path, default=DEFAULT_TRANSCRIPT_DIR)
    parser.add_argument("--ocr-dir", type=Path, default=DEFAULT_OCR_DIR)
    parser.add_argument("--no-download-media", action="store_true")
    parser.add_argument("--enable-openai", action="store_true")
    parser.add_argument("--max-provider-items", type=int, default=None)
    parser.add_argument("--provider-concurrency", type=int, default=4)
    args = parser.parse_args()

    start = time.monotonic()
    raw_posts = {
        channel: fetch_public_posts_with_segments(channel, args.max_pages)
        for channel in CHANNELS
    }
    posts_by_channel = {
        channel: filter_rows_by_date(rows, args.start_date, args.end_date)
        for channel, rows in raw_posts.items()
    }
    media_manifest = build_media_manifest(
        posts_by_channel,
        capture_dir=args.capture_dir,
        download_media=not args.no_download_media,
    )
    processing_queue, provider_state = run_processing_queue(
        media_manifest,
        enable_openai=args.enable_openai,
        transcript_dir=args.transcript_dir,
        ocr_dir=args.ocr_dir,
        max_provider_items=args.max_provider_items,
        provider_concurrency=args.provider_concurrency,
    )
    rr_drafts = build_rr_drafts(posts_by_channel, processing_queue)
    summary = summarize_artifacts(
        posts_by_channel,
        media_manifest,
        processing_queue,
        rr_drafts,
        provider_state,
        start_date=args.start_date,
        end_date=args.end_date,
        max_pages=args.max_pages,
    )
    summary["runtime_seconds"] = round(time.monotonic() - start, 3)

    write_json(
        args.manifest_json, {"summary": summary, "media_manifest": media_manifest}
    )
    write_json(
        args.queue_json, {"summary": summary, "processing_queue": processing_queue}
    )
    write_json(args.rr_json, {"summary": summary, "rr_drafts": rr_drafts})
    args.report_md.parent.mkdir(parents=True, exist_ok=True)
    args.report_md.write_text(
        render_report(
            summary,
            manifest_path=args.manifest_json,
            queue_path=args.queue_json,
            rr_path=args.rr_json,
        ),
        encoding="utf-8",
    )
    print(f"Wrote {args.manifest_json}")
    print(f"Wrote {args.queue_json}")
    print(f"Wrote {args.rr_json}")
    print(f"Wrote {args.report_md}")


if __name__ == "__main__":
    main()
