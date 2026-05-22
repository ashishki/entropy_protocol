from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import urllib.request
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

CHANNELS = ("bablos79", "nemphiscrypts", "pifagortrade")
DEFAULT_MAX_PAGES = 30
USER_AGENT = "signal-analytics-sandbox/three-channel-public-probe"

MARKET_RE = re.compile(
    r"(?i)(btc|eth|sol|bnb|xrp|crypto|крипт|битк|эфир|альт|рынок|market|"
    r"индекс|акци|фьюч|лонг|long|шорт|short|стоп|stop|тейк|take|target|"
    r"цель|позици|сделк|покуп|прода|buy|sell|вход|entry|выход|закрыл|"
    r"фикс|плеч|leverage|liquid|liq|сетап|setup|коррекц|пробо[йя])"
)
POSITION_RE = re.compile(
    r"(?i)(лонг|long|шорт|short|в позиции|позици|набрал|набираю|купил|"
    r"покупаю|докуп|продал|продаю|открыл|закрыл|закрываю|фиксир|стоп|"
    r"stop|тейк|take|target|цель|вход|entry|rr|риск|сетап|setup)"
)
EXPLICIT_FIELD_RE = re.compile(
    r"(?i)(entry|вход|стоп|stop|цель|target|тейк|take|tp\b|sl\b|rr|"
    r"риск.?ревард|плеч|safety trade|trap line|сетап|setup)"
)
DIRECTION_RE = re.compile(
    r"(?i)(лонг|long|шорт|short|рост|выраст|паден|падает|падать|выше|ниже|"
    r"пробиваем|пробой|покуп|прода|buy|sell|докуп|отскок)"
)
ASSET_RE = re.compile(
    r"(?i)(#[A-Z0-9]{2,12}|\$[A-Z]{2,12}\b|"
    r"\b(?:BTC|ETH|SOL|BNB|XRP|DOGE|ADA|TON|LINK|AVAX|SUI|PEPE|ARB|OP|"
    r"APT|NEAR|TRX|LTC|BCH|DOT|MATIC|USDT|USDC|MOEX|RTSI|SBER|GAZP|VTBR|"
    r"NVTK|CHMF|MAGN|PHOR|SPY|SPYF|NG|GOLD|CNY|SI|BR)[A-Z0-9/\-]*\b|"
    r"\b[A-Z]{2,8}USDT\b)"
)


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=25) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_tags(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value)
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def parse_page(channel: str, body: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    pattern = re.compile(r'data-post="' + re.escape(channel) + r"/(\d+)\"")
    for match in pattern.finditer(body):
        start = max(0, body.rfind("<div", 0, match.start()))
        end = body.find("tgme_widget_message_wrap", match.end())
        if end == -1:
            end = len(body)
        segment = body[start:end]
        post_id = int(match.group(1))
        time_match = re.search(r'<time datetime="([^"]+)"', segment)
        timestamp = time_match.group(1) if time_match else None
        text_chunks = re.findall(
            r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>',
            segment,
            flags=re.S,
        )
        text = "\n".join(strip_tags(chunk) for chunk in text_chunks).strip()
        rows.append(
            {
                "post_id": post_id,
                "timestamp_utc": timestamp,
                "text": text,
                "source_url": f"https://t.me/{channel}/{post_id}",
            }
        )
    return rows


def previous_before_id(body: str) -> int | None:
    match = re.search(r'<link rel="prev" href="/s/[^"?]+\?before=(\d+)"', body)
    return int(match.group(1)) if match else None


def fetch_channel(
    channel: str,
    max_pages: int,
) -> tuple[list[dict[str, Any]], list[str]]:
    seen: dict[int, dict[str, Any]] = {}
    errors: list[str] = []
    before_id: int | None = None
    pages_fetched = 0

    while pages_fetched < max_pages:
        url = f"https://t.me/s/{channel}"
        if before_id is not None:
            url = f"{url}?before={before_id}"
        try:
            body = fetch(url)
        except Exception as exc:  # noqa: BLE001 - surfaced in artifact.
            errors.append(f"{type(exc).__name__}: {exc}")
            break
        pages_fetched += 1
        for row in parse_page(channel, body):
            seen[row["post_id"]] = row
        next_before_id = previous_before_id(body)
        if next_before_id is None or next_before_id == before_id:
            break
        before_id = next_before_id

    rows = sorted(seen.values(), key=lambda item: item["post_id"])
    for row in rows:
        row["pages_fetched_for_channel"] = pages_fetched
    return rows, errors


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def clean_asset(asset: str) -> str:
    return asset.lstrip("#$").upper()


def classify(channel: str, row: dict[str, Any]) -> dict[str, Any]:
    text = row["text"]
    assets = sorted({clean_asset(match) for match in ASSET_RE.findall(text)})
    has_market = bool(MARKET_RE.search(text) or assets)
    has_position = bool(POSITION_RE.search(text))
    has_explicit = bool(EXPLICIT_FIELD_RE.search(text))
    has_direction = bool(DIRECTION_RE.search(text))

    if has_explicit and assets and has_direction:
        category = "explicit_setup_candidate"
        evaluation_path = "setup_backtest_after_operator_proxy_and_horizon_approval"
    elif has_position and assets:
        category = "position_or_trade_language_candidate"
        evaluation_path = "position_or_directional_outcome_after_operator_mapping"
    elif has_direction or assets:
        category = "directional_bias_candidate"
        evaluation_path = "fixed_horizon_directional_outcome_after_proxy_approval"
    elif has_market:
        category = "market_context_candidate"
        evaluation_path = "context_only_until_operator_defines_benchmark"
    else:
        category = "not_market_candidate"
        evaluation_path = "not_evaluable"

    return {
        "candidate_id": f"{channel}-{row['post_id']}",
        "source_id": channel,
        "post_id": row["post_id"],
        "timestamp_utc": row["timestamp_utc"],
        "source_url": row["source_url"],
        "text_sha256": text_hash(text) if text else None,
        "raw_text_chars": len(text),
        "assets": assets,
        "category": category,
        "evaluation_path": evaluation_path,
        "requires_operator_approval": category != "not_market_candidate",
        "market_data_fetch_allowed_now": False,
        "external_eligible_now": False,
        "snippet": re.sub(r"\s+", " ", text)[:260],
    }


def summarize_channel(
    channel: str,
    rows: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    errors: list[str],
) -> dict[str, Any]:
    text_rows = [row for row in rows if row["text"]]
    category_counts = Counter(candidate["category"] for candidate in candidates)
    market_candidates = [
        candidate
        for candidate in candidates
        if candidate["category"] != "not_market_candidate"
    ]
    explicit = category_counts["explicit_setup_candidate"]
    position = category_counts["position_or_trade_language_candidate"]
    directional = category_counts["directional_bias_candidate"]
    context = category_counts["market_context_candidate"]

    readiness_score = round(
        (explicit * 3 + position * 2 + directional + context * 0.25)
        / max(len(text_rows), 1),
        3,
    )
    if explicit >= 50:
        recommended_first_pass = "setup_and_directional_backtest"
    elif position >= 50:
        recommended_first_pass = "position_disclosure_and_directional_backtest"
    elif directional + position >= 40:
        recommended_first_pass = "fixed_horizon_directional_backtest"
    else:
        recommended_first_pass = "evidence_repair_before_outcomes"

    return {
        "source_id": channel,
        "public_url": f"https://t.me/s/{channel}",
        "pages_fetched": rows[0]["pages_fetched_for_channel"] if rows else 0,
        "public_rows": len(rows),
        "text_rows": len(text_rows),
        "non_text_rows": len(rows) - len(text_rows),
        "coverage_start_utc": text_rows[0]["timestamp_utc"] if text_rows else None,
        "coverage_end_utc": text_rows[-1]["timestamp_utc"] if text_rows else None,
        "market_adjacent_candidates": len(market_candidates),
        "explicit_setup_candidates": explicit,
        "position_or_trade_language_candidates": position,
        "directional_bias_candidates": directional,
        "market_context_candidates": context,
        "not_market_rows": category_counts["not_market_candidate"],
        "unique_asset_markers": sorted(
            {asset for candidate in market_candidates for asset in candidate["assets"]}
        ),
        "readiness_score": readiness_score,
        "recommended_first_pass": recommended_first_pass,
        "market_data_fetch_allowed_now": 0,
        "external_eligible_now": 0,
        "errors": errors,
    }


def render_markdown(artifact: dict[str, Any]) -> str:
    lines = [
        "# Three-Channel Public Corpus Probe",
        "",
        f"Date: {artifact['generated_at_utc']}",
        f"Status: {artifact['status']}",
        "",
        "## Boundary",
        "",
        "- Sources: public Telegram `/s/` pages only.",
        "- No private Telegram, login-walled, paywalled, or access-control "
        "bypass source was used.",
        "- This artifact does not fetch market data, compute outcomes, "
        "approve proxies, or create external claims.",
        "- Candidate labels are review queues, not investment advice and not "
        "proof of author skill.",
        "",
        "## Summary",
        "",
        "| channel | text rows | market candidates | explicit setups | "
        "position/trade language | directional bias | first pass |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for channel in artifact["channels"]:
        lines.append(
            "| `{source_id}` | {text_rows} | {market_adjacent_candidates} | "
            "{explicit_setup_candidates} | {position_or_trade_language_candidates} | "
            "{directional_bias_candidates} | `{recommended_first_pass}` |".format(
                **channel
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `pifagortrade` is the best first candidate for classic setup/"
            "directional backtesting because it has the largest number of "
            "explicit setup fields and trade-language rows.",
            "- `nemphiscrypts` is suitable for crypto directional and "
            "scenario backtesting after operator-approved BTC/ETH/alt proxy "
            "rules.",
            "- `bablos79` remains more mixed: useful rows exist, but many "
            "are context or position-management fragments, so it needs "
            "stricter operator mapping.",
            "",
            "## Operator Decisions Needed",
            "",
            "1. Approve the per-channel first-pass evaluator type: setup, "
            "directional fixed-horizon, position disclosure, or context-only.",
            "2. Approve proxy mapping rules before any market data fetch, "
            "especially Russian equities/futures for `bablos79` and "
            "BTC/ETH/alt proxies for crypto channels.",
            "3. Approve horizon rules per candidate type: immediate next "
            "close, 1d/3d/7d/30d, next disclosure, or invalid if no "
            "timestamp/asset.",
            "4. Decide whether scenario posts without explicit entry/stop/"
            "target can be evaluated as directional forecasts or kept as "
            "context only.",
            "",
            "## Top Candidates",
            "",
        ]
    )

    for channel in artifact["channels"]:
        source_id = channel["source_id"]
        lines.extend([f"### `{source_id}`", ""])
        candidates = artifact["review_samples"][source_id]
        lines.append("| candidate | timestamp | category | assets | source |")
        lines.append("|---|---|---|---|---|")
        for candidate in candidates:
            assets = ", ".join(candidate["assets"][:8]) or "-"
            row = dict(candidate)
            row["asset_list"] = assets
            lines.append(
                "| `{candidate_id}` | `{timestamp_utc}` | `{category}` | "
                "{asset_list} | [source]({source_url}) |".format(**row)
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_artifact(max_pages: int) -> dict[str, Any]:
    generated_at = (
        datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    channel_summaries: list[dict[str, Any]] = []
    review_samples: dict[str, list[dict[str, Any]]] = {}
    all_candidate_rows: dict[str, list[dict[str, Any]]] = {}

    for channel in CHANNELS:
        rows, errors = fetch_channel(channel, max_pages)
        candidates = [classify(channel, row) for row in rows if row["text"]]
        summary = summarize_channel(channel, rows, candidates, errors)
        market_candidates = [
            candidate
            for candidate in candidates
            if candidate["category"] != "not_market_candidate"
        ]
        market_candidates.sort(
            key=lambda candidate: (
                candidate["category"] != "explicit_setup_candidate",
                candidate["category"] != "position_or_trade_language_candidate",
                candidate["timestamp_utc"] or "",
            )
        )
        channel_summaries.append(summary)
        review_samples[channel] = market_candidates[:20]
        all_candidate_rows[channel] = candidates

    totals = {
        "channels": len(channel_summaries),
        "text_rows": sum(channel["text_rows"] for channel in channel_summaries),
        "market_adjacent_candidates": sum(
            channel["market_adjacent_candidates"] for channel in channel_summaries
        ),
        "explicit_setup_candidates": sum(
            channel["explicit_setup_candidates"] for channel in channel_summaries
        ),
        "position_or_trade_language_candidates": sum(
            channel["position_or_trade_language_candidates"]
            for channel in channel_summaries
        ),
        "market_data_fetch_allowed_now": 0,
        "external_eligible_now": 0,
    }

    return {
        "artifact_id": "three-channel-public-corpus-probe-2026-05-17",
        "generated_at_utc": generated_at,
        "status": "public_probe_completed_operator_mapping_required",
        "source_boundary": {
            "source_class": "telegram_public",
            "public_s_pages_only": True,
            "private_sources_used": False,
            "login_walled_sources_used": False,
            "paywalled_sources_used": False,
            "market_data_fetched": False,
            "outcomes_computed": False,
            "external_claims_created": False,
        },
        "run_config": {
            "channels": list(CHANNELS),
            "max_pages_per_channel": max_pages,
            "capture_method": "public_telegram_s_html_live_probe",
        },
        "totals": totals,
        "channels": channel_summaries,
        "review_samples": review_samples,
        "candidate_rows": all_candidate_rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES)
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.json"),
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=Path("docs/pilot/three_channel_PUBLIC_CORPUS_PROBE.md"),
    )
    args = parser.parse_args()

    artifact = build_artifact(args.max_pages)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.md_output.write_text(render_markdown(artifact), encoding="utf-8")
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.md_output}")


if __name__ == "__main__":
    main()
