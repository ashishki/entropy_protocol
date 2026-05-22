from __future__ import annotations

# ruff: noqa: E501
import argparse
import hashlib
import html
import json
import re
import statistics
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import UTC, date, datetime, timedelta
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path
from typing import Any

CHANNELS = ("bablos79", "nemphiscrypts", "pifagortrade")
MAX_PAGES = 30
PRIMARY_HORIZON = "7d"
HORIZONS = {"1d": 1, "3d": 3, "7d": 7}
USER_AGENT = "signal-analytics-sandbox/three-channel-metric-report"
ROUND = Decimal("0.000001")

CRYPTO_ASSETS = {
    "BTC": {
        "provider": "binance",
        "symbol": "BTCUSDT",
        "patterns": [r"\bBTC\b", r"\bBTCUSD\b", r"битк\w*", r"биткоин\w*"],
    },
    "ETH": {
        "provider": "binance",
        "symbol": "ETHUSDT",
        "patterns": [r"\bETH\b", r"\bETHEREUM\b", r"эфир\w*"],
    },
    "SOL": {
        "provider": "binance",
        "symbol": "SOLUSDT",
        "patterns": [r"\bSOL\b", r"\bSOLANA\b"],
    },
    "BNB": {"provider": "binance", "symbol": "BNBUSDT", "patterns": [r"\bBNB\b"]},
    "XRP": {"provider": "binance", "symbol": "XRPUSDT", "patterns": [r"\bXRP\b"]},
    "TON": {
        "provider": "binance",
        "symbol": "TONUSDT",
        "patterns": [r"\bTON\b", r"\bTONCOIN\b", r"\bTONUSDT\b"],
    },
    "AVAX": {
        "provider": "binance",
        "symbol": "AVAXUSDT",
        "patterns": [r"\bAVAX\b"],
    },
    "LINK": {
        "provider": "binance",
        "symbol": "LINKUSDT",
        "patterns": [r"\bLINK\b"],
    },
    "DOT": {"provider": "binance", "symbol": "DOTUSDT", "patterns": [r"\bDOT\b"]},
    "ARB": {"provider": "binance", "symbol": "ARBUSDT", "patterns": [r"\bARB\b"]},
    "SUI": {"provider": "binance", "symbol": "SUIUSDT", "patterns": [r"\bSUI\b"]},
    "ADA": {"provider": "binance", "symbol": "ADAUSDT", "patterns": [r"\bADA\b"]},
}

MOEX_SHARES = {
    "AFLT",
    "CBOM",
    "CHMF",
    "GAZP",
    "LENT",
    "LKOH",
    "MAGN",
    "MGNT",
    "NVTK",
    "PHOR",
    "SBER",
    "SBRF",
    "SFIN",
    "SMLT",
    "VKCO",
    "VTBR",
    "WUSH",
    "X5",
}

LONG_RE = re.compile(
    r"(?i)(лонг\w*|long\b|buy\b|bullish\b|upside\b|покуп\w*|докуп\w*|"
    r"наб[ие]ра\w*|рост\w*|раст[еи]\w*|выше|пробива\w*|пробой вверх|"
    r"отскок\w*|ид[её]м на|цель\w*)"
)
SHORT_RE = re.compile(
    r"(?i)(шорт\w*|short\b|sell\b|bearish\b|downside\b|прода\w*|"
    r"паден\w*|падать|ниже|обвал\w*|обруш\w*)"
)
NEGATE_SHORT_RE = re.compile(r"(?i)(не\s+шорт\w*|а\s+не\s+шорт\w*)")
NEGATE_LONG_RE = re.compile(r"(?i)(не\s+лонг\w*|а\s+не\s+лонг\w*)")
TRADE_FIELD_RE = re.compile(
    r"(?i)(entry|вход|стоп|stop|цель|target|тейк|take|tp\b|sl\b|лимитк|"
    r"безубыт|б/у|rr|риск)"
)
POSITION_RE = re.compile(
    r"(?i)(позици\w*|портфел\w*|держ\w*|холд\w*|набрал|открыл|закрыл|"
    r"зафикс\w*|стоп\s+перен[её]с)"
)
MARKET_RE = re.compile(
    r"(?i)(рынок|market|крипт|битк|эфир|акци|фьюч|лонг|шорт|стоп|цель|"
    r"позици|сделк|сетап|прогноз|волатильн|ликвидн|пробой|коррекц)"
)


def fetch(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_tags(value: str) -> str:
    value = re.sub(r"<br\s*/?>", "\n", value)
    value = re.sub(r"<[^>]+>", "", value)
    return html.unescape(value).strip()


def parse_page(channel: str, body: str) -> list[dict[str, Any]]:
    rows = []
    pattern = re.compile(r'data-post="' + re.escape(channel) + r"/(\d+)\"")
    for match in pattern.finditer(body):
        start = max(0, body.rfind("<div", 0, match.start()))
        end = body.find("tgme_widget_message_wrap", match.end())
        if end == -1:
            end = len(body)
        segment = body[start:end]
        post_id = int(match.group(1))
        time_match = re.search(r'<time datetime="([^"]+)"', segment)
        text_chunks = re.findall(
            r'<div class="tgme_widget_message_text[^>]*>(.*?)</div>',
            segment,
            flags=re.S,
        )
        text = "\n".join(strip_tags(chunk) for chunk in text_chunks).strip()
        rows.append(
            {
                "source_id": channel,
                "post_id": post_id,
                "timestamp_utc": time_match.group(1) if time_match else None,
                "source_url": f"https://t.me/{channel}/{post_id}",
                "text": text,
            }
        )
    return rows


def previous_before_id(body: str) -> int | None:
    match = re.search(r'<link rel="prev" href="/s/[^"?]+\?before=(\d+)"', body)
    return int(match.group(1)) if match else None


def fetch_public_rows(channel: str, max_pages: int) -> list[dict[str, Any]]:
    before_id = None
    seen: dict[int, dict[str, Any]] = {}
    for _ in range(max_pages):
        url = f"https://t.me/s/{channel}"
        if before_id is not None:
            url = f"{url}?before={before_id}"
        body = fetch(url)
        for row in parse_page(channel, body):
            seen[row["post_id"]] = row
        next_before_id = previous_before_id(body)
        if next_before_id is None or next_before_id == before_id:
            break
        before_id = next_before_id
    return sorted(seen.values(), key=lambda row: row["post_id"])


def detect_assets(text: str, *, source_id: str) -> list[dict[str, str]]:
    assets: dict[str, dict[str, str]] = {}
    for asset, config in CRYPTO_ASSETS.items():
        for pattern in config["patterns"]:
            if re.search(pattern, text, flags=re.I):
                assets[asset] = {
                    "asset": asset,
                    "provider": config["provider"],
                    "provider_symbol": config["symbol"],
                    "asset_class": "crypto",
                }
                break
    for symbol in MOEX_SHARES:
        if source_id != "bablos79" and not re.search(
            rf"(?i)#\s*{re.escape(symbol)}\b", text
        ):
            continue
        if re.search(rf"(?i)(?:#|\b){re.escape(symbol)}\b", text):
            provider_symbol = "SBER" if symbol == "SBRF" else symbol
            assets[symbol] = {
                "asset": symbol,
                "provider": "moex_iss",
                "provider_symbol": provider_symbol,
                "asset_class": "moex_share",
            }
    return sorted(assets.values(), key=lambda item: item["asset"])


def detect_direction(text: str) -> str:
    cleaned = re.sub(r"https?://\S+", " ", text)
    has_long = bool(LONG_RE.search(cleaned))
    has_short = bool(SHORT_RE.search(cleaned))
    if NEGATE_SHORT_RE.search(cleaned):
        has_short = False
    if NEGATE_LONG_RE.search(cleaned):
        has_long = False
    if has_long and has_short:
        return "mixed"
    if has_long:
        return "long"
    if has_short:
        return "short"
    return "unknown"


def claim_type(text: str) -> str:
    if TRADE_FIELD_RE.search(text):
        return "trade_setup_or_management"
    if POSITION_RE.search(text):
        return "position_disclosure_or_management"
    return "directional_thesis"


def normalize_claims(
    rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], Counter]:
    claims = []
    excluded = Counter()
    for row in rows:
        text = row["text"]
        if not text:
            excluded["no_text"] += 1
            continue
        assets = detect_assets(text, source_id=row["source_id"])
        if not (MARKET_RE.search(text) or assets):
            excluded["not_market_related"] += 1
            continue
        if not assets:
            excluded["no_supported_asset_or_proxy"] += 1
            continue
        direction = detect_direction(text)
        if direction == "unknown":
            excluded["no_direction"] += 1
            continue
        if direction == "mixed":
            excluded["mixed_direction"] += 1
            continue
        timestamp = row["timestamp_utc"]
        if timestamp is None:
            excluded["no_timestamp"] += 1
            continue
        for asset in assets:
            claim_id = stable_id(row["source_id"], row["post_id"], asset["asset"])
            claims.append(
                {
                    "claim_id": claim_id,
                    "source_id": row["source_id"],
                    "post_id": row["post_id"],
                    "source_url": row["source_url"],
                    "timestamp_utc": timestamp,
                    "asset": asset["asset"],
                    "asset_class": asset["asset_class"],
                    "provider": asset["provider"],
                    "provider_symbol": asset["provider_symbol"],
                    "direction": direction,
                    "claim_type": claim_type(text),
                    "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    "snippet": re.sub(r"\s+", " ", text)[:260],
                }
            )
    return claims, excluded


def stable_id(source_id: str, post_id: int, asset: str) -> str:
    digest = hashlib.sha256(f"{source_id}:{post_id}:{asset}".encode()).hexdigest()
    return f"claim_{digest[:16]}"


def fetch_binance_daily(symbol: str, start: date, end: date) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "symbol": symbol,
            "interval": "1d",
            "startTime": int(
                datetime.combine(start, datetime.min.time(), UTC).timestamp() * 1000
            ),
            "endTime": int(
                datetime.combine(
                    end + timedelta(days=1), datetime.min.time(), UTC
                ).timestamp()
                * 1000
            ),
            "limit": 1000,
        }
    )
    url = f"https://api.binance.com/api/v3/klines?{params}"
    data = json.loads(fetch(url))
    rows = []
    for row in data:
        rows.append(
            {
                "date": datetime.fromtimestamp(row[0] / 1000, UTC).date(),
                "open": Decimal(str(row[1])),
                "high": Decimal(str(row[2])),
                "low": Decimal(str(row[3])),
                "close": Decimal(str(row[4])),
                "provider_url": url,
            }
        )
    return rows


def fetch_moex_daily(symbol: str, start: date, end: date) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {"from": start.isoformat(), "till": end.isoformat(), "interval": 24}
    )
    url = (
        "https://iss.moex.com/iss/engines/stock/markets/shares/"
        f"securities/{symbol}/candles.json?{params}"
    )
    data = json.loads(fetch(url))
    candles = data["candles"]
    columns = candles["columns"]
    rows = []
    for raw in candles["data"]:
        item = dict(zip(columns, raw, strict=False))
        rows.append(
            {
                "date": datetime.fromisoformat(item["begin"]).date(),
                "open": Decimal(str(item["open"])),
                "high": Decimal(str(item["high"])),
                "low": Decimal(str(item["low"])),
                "close": Decimal(str(item["close"])),
                "provider_url": url,
            }
        )
    return rows


def fetch_price_rows(
    claims: list[dict[str, Any]],
) -> dict[tuple[str, str], list[dict[str, Any]]]:
    ranges: dict[tuple[str, str], list[date]] = defaultdict(list)
    for claim in claims:
        claim_date = parse_dt(claim["timestamp_utc"]).date()
        ranges[(claim["provider"], claim["provider_symbol"])].append(claim_date)

    price_rows: dict[tuple[str, str], list[dict[str, Any]]] = {}
    today = datetime.now(UTC).date()
    for key, dates in ranges.items():
        provider, symbol = key
        start = min(dates) - timedelta(days=2)
        end = min(max(dates) + timedelta(days=35), today)
        try:
            if provider == "binance":
                rows = fetch_binance_daily(symbol, start, end)
            elif provider == "moex_iss":
                rows = fetch_moex_daily(symbol, start, end)
            else:
                rows = []
        except Exception:
            rows = []
        price_rows[key] = sorted(rows, key=lambda row: row["date"])
    return price_rows


def evaluate_claim(
    claim: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    if not rows:
        return {**claim, "evaluation_status": "no_provider_rows", "metrics": {}}
    post_date = parse_dt(claim["timestamp_utc"]).date()
    entry = next((row for row in rows if row["date"] >= post_date), None)
    if entry is None:
        return {**claim, "evaluation_status": "no_entry_row", "metrics": {}}

    metrics = {}
    for horizon, days in HORIZONS.items():
        horizon_date = post_date + timedelta(days=days)
        if rows[-1]["date"] < horizon_date:
            metrics[horizon] = {"status": "insufficient_future_window"}
            continue
        window = [row for row in rows if entry["date"] <= row["date"] <= horizon_date]
        if len(window) < 2:
            metrics[horizon] = {"status": "insufficient_window_rows"}
            continue
        exit_row = window[-1]
        raw_return = pct(exit_row["close"], entry["close"])
        highs = [row["high"] for row in window]
        lows = [row["low"] for row in window]
        if claim["direction"] == "short":
            directional_return = -raw_return
            mfe = pct(entry["close"], min(lows))
            mae = pct(entry["close"], max(highs))
        else:
            directional_return = raw_return
            mfe = pct(max(highs), entry["close"])
            mae = pct(min(lows), entry["close"])
        metrics[horizon] = {
            "status": "evaluated",
            "entry_date": entry["date"].isoformat(),
            "entry_close": str(q(entry["close"])),
            "exit_date": exit_row["date"].isoformat(),
            "exit_close": str(q(exit_row["close"])),
            "raw_return_pct": str(q(raw_return)),
            "directional_return_pct": str(q(directional_return)),
            "max_favorable_excursion_pct": str(q(abs(mfe))),
            "max_adverse_excursion_pct": str(q(-abs(mae))),
            "hit": directional_return > 0,
        }

    status = (
        "evaluated"
        if metrics.get(PRIMARY_HORIZON, {}).get("status") == "evaluated"
        else "no_primary_horizon"
    )
    return {
        **claim,
        "evaluation_status": status,
        "primary_horizon": PRIMARY_HORIZON,
        "metrics": metrics,
        "provider_confirmation": {
            "provider": claim["provider"],
            "provider_symbol": claim["provider_symbol"],
            "rows_available": len(rows),
            "range_start": rows[0]["date"].isoformat(),
            "range_end": rows[-1]["date"].isoformat(),
            "provider_url": rows[0]["provider_url"],
        },
    }


def pct(later: Decimal, earlier: Decimal) -> Decimal:
    if earlier == 0:
        return Decimal("0")
    return ((later - earlier) / earlier) * Decimal("100")


def q(value: Decimal) -> Decimal:
    return value.quantize(ROUND, rounding=ROUND_HALF_EVEN)


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def summarize(
    rows_by_channel: dict[str, list[dict[str, Any]]],
    claims_by_channel: dict[str, list[dict[str, Any]]],
    evaluated_by_channel: dict[str, list[dict[str, Any]]],
    excluded_by_channel: dict[str, Counter],
) -> list[dict[str, Any]]:
    summaries = []
    for channel in CHANNELS:
        claims = claims_by_channel[channel]
        evaluated = evaluated_by_channel[channel]
        primary = [
            claim
            for claim in evaluated
            if claim["metrics"].get(PRIMARY_HORIZON, {}).get("status") == "evaluated"
        ]
        hits = [
            claim
            for claim in primary
            if claim["metrics"][PRIMARY_HORIZON]["hit"] is True
        ]
        returns = [
            Decimal(claim["metrics"][PRIMARY_HORIZON]["directional_return_pct"])
            for claim in primary
        ]
        mfe = [
            Decimal(claim["metrics"][PRIMARY_HORIZON]["max_favorable_excursion_pct"])
            for claim in primary
        ]
        mae = [
            Decimal(claim["metrics"][PRIMARY_HORIZON]["max_adverse_excursion_pct"])
            for claim in primary
        ]
        summaries.append(
            {
                "source_id": channel,
                "public_text_rows": len(
                    [r for r in rows_by_channel[channel] if r["text"]]
                ),
                "normalized_claims": len(claims),
                "primary_evaluable_claims": len(primary),
                "confirmed_hits": len(hits),
                "contradicted_misses": len(primary) - len(hits),
                "primary_hit_rate": ratio(len(hits), len(primary)),
                "avg_directional_return_pct": avg_decimal(returns),
                "median_directional_return_pct": median_decimal(returns),
                "avg_mfe_pct": avg_decimal(mfe),
                "avg_mae_pct": avg_decimal(mae),
                "coverage_evaluable_rate": ratio(len(primary), len(claims)),
                "excluded_counts": dict(excluded_by_channel[channel]),
                "provider_counts": dict(Counter(c["provider"] for c in primary)),
                "asset_counts": dict(
                    Counter(c["asset"] for c in primary).most_common(12)
                ),
            }
        )
    return summaries


def ratio(numerator: int, denominator: int) -> str | None:
    if denominator == 0:
        return None
    return str(q((Decimal(numerator) / Decimal(denominator)) * Decimal("100")))


def avg_decimal(values: list[Decimal]) -> str | None:
    if not values:
        return None
    return str(q(sum(values) / Decimal(len(values))))


def median_decimal(values: list[Decimal]) -> str | None:
    if not values:
        return None
    return str(q(Decimal(str(statistics.median(values)))))


def render_report(artifact: dict[str, Any]) -> str:
    lines = [
        "# Three-Channel Metric Report V0",
        "",
        f"Date: {artifact['generated_at_utc']}",
        f"Status: {artifact['status']}",
        "",
        "## Boundary",
        "",
        "- Sources: public Telegram `/s/` pages only.",
        "- Market validation: open/public daily OHLCV windows via Binance public klines and MOEX ISS candles.",
        "- Storage posture: no bulk market-history database; this run stores only compact per-claim metrics and provider confirmation metadata.",
        "- Primary comparison horizon: `7d` directional return after the public post timestamp using the first available daily candle on/after the post date.",
        "- This is historical research, not investment advice or a future-profit claim.",
        "",
        "## V0 Evaluation Rules",
        "",
        "- Included rows must have public timestamp, supported asset/proxy, and single long/short direction.",
        "- Supported V0 providers: Binance public daily klines for crypto and MOEX ISS daily candles for supported MOEX shares.",
        "- Unsupported assets, missing direction, mixed direction, media-only rows, and non-market rows are excluded from performance but retained in coverage counts.",
        "- Multi-asset posts are evaluated as asset-level claims, so one post may produce more than one measured row.",
        "",
        "## Channel Comparison",
        "",
        "| channel | text rows | normalized claims | 7d evaluable | confirmed | contradicted | hit rate | avg directional 7d return | avg MFE | avg MAE |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in artifact["channel_summaries"]:
        lines.append(
            "| `{source_id}` | {public_text_rows} | {normalized_claims} | "
            "{primary_evaluable_claims} | {confirmed_hits} | {contradicted_misses} | "
            "{primary_hit_rate} | {avg_directional_return_pct} | {avg_mfe_pct} | "
            "{avg_mae_pct} |".format(
                **{
                    key: value if value is not None else "-"
                    for key, value in summary.items()
                }
            )
        )
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `primary_hit_rate` counts whether the price moved in the stated direction over the 7-day window.",
            "- `avg_directional_return_pct` is the conditional return of a simple direction-only position: long keeps raw return, short flips the sign.",
            "- `avg_mfe_pct` and `avg_mae_pct` show favorable/adverse excursion during the same 7-day window.",
            "- Unevaluable rows are not treated as failures; they remain in coverage and exclusion counts.",
            "",
            "## Exclusions",
            "",
        ]
    )
    for summary in artifact["channel_summaries"]:
        lines.append(f"### `{summary['source_id']}`")
        if summary["excluded_counts"]:
            for key, value in sorted(summary["excluded_counts"].items()):
                lines.append(f"- `{key}`: {value}")
        else:
            lines.append("- none")
        lines.append("")

    for title, selector in (
        ("Confirmed Examples", True),
        ("Contradicted Examples", False),
    ):
        lines.extend([f"## {title}", ""])
        for channel in CHANNELS:
            examples = [
                claim
                for claim in artifact["evaluated_claims"][channel]
                if claim["metrics"].get(PRIMARY_HORIZON, {}).get("status")
                == "evaluated"
                and claim["metrics"][PRIMARY_HORIZON]["hit"] is selector
            ][:5]
            lines.extend([f"### `{channel}`", ""])
            if not examples:
                lines.append("- none")
                lines.append("")
                continue
            lines.append(
                "| post | asset | direction | 7d directional return | evidence |"
            )
            lines.append("|---|---|---|---:|---|")
            for claim in examples:
                metric = claim["metrics"][PRIMARY_HORIZON]
                lines.append(
                    "| `{post_id}` | `{asset}` | `{direction}` | {ret} | [source]({source_url}) |".format(
                        **claim,
                        ret=metric["directional_return_pct"],
                    )
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_artifact(max_pages: int) -> dict[str, Any]:
    generated_at = (
        datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    rows_by_channel = {
        channel: fetch_public_rows(channel, max_pages) for channel in CHANNELS
    }
    claims_by_channel = {}
    excluded_by_channel = {}
    for channel, rows in rows_by_channel.items():
        claims, excluded = normalize_claims(rows)
        claims_by_channel[channel] = claims
        excluded_by_channel[channel] = excluded

    all_claims = [claim for claims in claims_by_channel.values() for claim in claims]
    price_rows = fetch_price_rows(all_claims)
    evaluated_by_channel = {}
    for channel, claims in claims_by_channel.items():
        evaluated_by_channel[channel] = [
            evaluate_claim(
                claim,
                price_rows.get((claim["provider"], claim["provider_symbol"]), []),
            )
            for claim in claims
        ]

    channel_summaries = summarize(
        rows_by_channel,
        claims_by_channel,
        evaluated_by_channel,
        excluded_by_channel,
    )
    totals = {
        "public_text_rows": sum(
            summary["public_text_rows"] for summary in channel_summaries
        ),
        "normalized_claims": sum(
            summary["normalized_claims"] for summary in channel_summaries
        ),
        "primary_evaluable_claims": sum(
            summary["primary_evaluable_claims"] for summary in channel_summaries
        ),
        "confirmed_hits": sum(
            summary["confirmed_hits"] for summary in channel_summaries
        ),
        "contradicted_misses": sum(
            summary["contradicted_misses"] for summary in channel_summaries
        ),
    }
    return {
        "artifact_id": "three-channel-metric-results-v0-2026-05-17",
        "generated_at_utc": generated_at,
        "status": "historical_metric_results_v0_open_public_data",
        "method": {
            "source_method": "public_telegram_s_html",
            "max_pages_per_channel": max_pages,
            "primary_horizon": PRIMARY_HORIZON,
            "horizons": list(HORIZONS),
            "providers": ["binance_public_klines", "moex_iss_candles"],
            "timestamp_basis": "first_available_daily_candle_on_or_after_public_post_date",
            "bulk_market_database_used": False,
            "investment_advice": False,
        },
        "totals": totals,
        "channel_summaries": channel_summaries,
        "evaluated_claims": evaluated_by_channel,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-pages", type=int, default=MAX_PAGES)
    parser.add_argument(
        "--json-output",
        type=Path,
        default=Path("docs/pilot/three_channel_METRIC_RESULTS.json"),
    )
    parser.add_argument(
        "--md-output",
        type=Path,
        default=Path("docs/pilot/three_channel_METRIC_REPORT.md"),
    )
    args = parser.parse_args()
    artifact = build_artifact(args.max_pages)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(
        json.dumps(artifact, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.md_output.write_text(render_report(artifact), encoding="utf-8")
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.md_output}")


if __name__ == "__main__":
    main()
