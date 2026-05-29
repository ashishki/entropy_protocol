from __future__ import annotations

import json
from collections import Counter, defaultdict
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
V0_PATH = PROJECT_ROOT / "docs/pilot/three_channel_METRIC_RESULTS.json"
RESULTS_PATH = PROJECT_ROOT / "docs/pilot/three_channel_V1_METRIC_RESULTS.json"
SCORECARD_PATH = PROJECT_ROOT / "docs/pilot/three_channel_V1_SCORECARD.md"

ROUNDING_QUANT = Decimal("0.000001")

REVIEWED_INCLUDED_DECISIONS = {
    ("bablos79", 10114, "LKOH"): "false_positive",
    ("bablos79", 10208, "PHOR"): "accepted",
    ("bablos79", 10217, "VTBR"): "needs_context",
    ("bablos79", 10250, "BTC"): "accepted",
    ("bablos79", 10257, "SMLT"): "needs_context",
    ("bablos79", 10332, "NVTK"): "false_positive",
    ("bablos79", 10335, "SBER"): "needs_context",
    ("nemphiscrypts", 3344, "BTC"): "accepted",
    ("nemphiscrypts", 3367, "ETH"): "needs_context",
    ("nemphiscrypts", 3372, "ETH"): "accepted",
    ("nemphiscrypts", 3376, "BTC"): "accepted",
    ("nemphiscrypts", 3387, "BTC"): "false_positive",
    ("nemphiscrypts", 3395, "BTC"): "needs_context",
    ("nemphiscrypts", 3405, "BTC"): "needs_context",
    ("pifagortrade", 2334, "BTC"): "needs_context",
    ("pifagortrade", 2379, "TON"): "false_positive",
    ("pifagortrade", 2454, "BTC"): "false_positive",
    ("pifagortrade", 2454, "ETH"): "false_positive",
    ("pifagortrade", 2498, "BTC"): "needs_context",
    ("pifagortrade", 2512, "BTC"): "needs_context",
}

FALSE_NEGATIVE_COUNTS = {
    "bablos79": 0,
    "nemphiscrypts": 2,
    "pifagortrade": 3,
}


def main() -> None:
    v0 = json.loads(V0_PATH.read_text(encoding="utf-8"))
    channel_results = []
    all_kept_claims: dict[str, list[dict[str, Any]]] = {}
    totals = Counter()

    for summary in v0["channel_summaries"]:
        source_id = summary["source_id"]
        claims = v0["evaluated_claims"][source_id]
        kept = []
        excluded = Counter()
        reviewed = Counter()
        for claim in claims:
            decision = REVIEWED_INCLUDED_DECISIONS.get(
                (source_id, claim["post_id"], claim["asset"]),
                "accepted_unreviewed",
            )
            reviewed[decision] += 1
            if decision in {"false_positive", "needs_context"}:
                excluded[f"review_{decision}"] += 1
                continue
            kept.append(claim)
        all_kept_claims[source_id] = kept
        channel_result = _channel_summary(summary, kept, excluded, reviewed)
        channel_results.append(channel_result)
        totals.update(
            {
                "public_text_rows": channel_result["public_text_rows"],
                "v1_evaluable_claims": channel_result["v1_evaluable_claims"],
                "confirmed_hits": channel_result["confirmed_hits"],
                "contradicted_misses": channel_result["contradicted_misses"],
                "review_false_negative_pending": channel_result[
                    "review_false_negative_pending"
                ],
            }
        )

    output = {
        "artifact_id": "three_channel_v1_metric_results",
        "status": "internal_v1_recompute",
        "method": {
            "source": "V0 evaluated claims plus SAS-V1-002 calibration decisions",
            "primary_horizon": "7d",
            "level_aware_rr_available": False,
            "multimodal_customer_claims_included": False,
            "bulk_market_database_used": False,
            "external_delivery_approved": False,
        },
        "totals": dict(totals),
        "channel_summaries": channel_results,
        "kept_claim_ids_by_channel": {
            channel: [claim["claim_id"] for claim in claims]
            for channel, claims in all_kept_claims.items()
        },
    }
    RESULTS_PATH.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    SCORECARD_PATH.write_text(_render_scorecard(output), encoding="utf-8")


def _channel_summary(
    v0_summary: dict[str, Any],
    kept: list[dict[str, Any]],
    excluded: Counter[str],
    reviewed: Counter[str],
) -> dict[str, Any]:
    source_id = v0_summary["source_id"]
    evaluable_kept = [
        claim for claim in kept if claim["metrics"]["7d"].get("status") == "evaluated"
    ]
    returns = [
        _metric_decimal(claim, "directional_return_pct") for claim in evaluable_kept
    ]
    mfes = [
        _metric_decimal(claim, "max_favorable_excursion_pct")
        for claim in evaluable_kept
    ]
    maes = [
        _metric_decimal(claim, "max_adverse_excursion_pct") for claim in evaluable_kept
    ]
    hits = sum(
        1 for claim in evaluable_kept if claim["metrics"]["7d"].get("hit") is True
    )
    misses = sum(
        1 for claim in evaluable_kept if claim["metrics"]["7d"].get("hit") is False
    )
    providers = Counter(claim["provider"] for claim in evaluable_kept)
    provider_symbols = defaultdict(set)
    for claim in evaluable_kept:
        provider_symbols[claim["provider"]].add(claim["provider_symbol"])
    v1_count = len(evaluable_kept)
    return {
        "source_id": source_id,
        "public_text_rows": v0_summary["public_text_rows"],
        "v0_evaluable_claims": v0_summary["primary_evaluable_claims"],
        "v1_evaluable_claims": v1_count,
        "confirmed_hits": hits,
        "contradicted_misses": misses,
        "primary_hit_rate": _pct(hits, v1_count),
        "avg_directional_return_pct": _avg(returns),
        "avg_mfe_pct": _avg(mfes),
        "avg_mae_pct": _avg(maes),
        "rr_available_count": 0,
        "provider_coverage": {
            provider: {
                "claim_count": count,
                "symbols": sorted(provider_symbols[provider]),
            }
            for provider, count in sorted(providers.items())
        },
        "exclusion_counts": {
            **v0_summary["excluded_counts"],
            **dict(excluded),
            "review_false_negative_pending": FALSE_NEGATIVE_COUNTS[source_id],
            "unreviewed_media_excluded": 0,
        },
        "review_decision_counts": dict(reviewed),
        "delta_from_v0": {
            "evaluable_claims": v1_count - v0_summary["primary_evaluable_claims"],
            "confirmed_hits": hits - v0_summary["confirmed_hits"],
            "contradicted_misses": misses - v0_summary["contradicted_misses"],
        },
        "review_false_negative_pending": FALSE_NEGATIVE_COUNTS[source_id],
    }


def _metric_decimal(claim: dict[str, Any], key: str) -> Decimal:
    return Decimal(str(claim["metrics"]["7d"][key]))


def _avg(values: list[Decimal]) -> str:
    if not values:
        return "0.000000"
    return _round(sum(values) / Decimal(len(values)))


def _pct(numerator: int, denominator: int) -> str:
    if denominator == 0:
        return "0.000000"
    return _round((Decimal(numerator) / Decimal(denominator)) * Decimal("100"))


def _round(value: Decimal) -> str:
    return str(value.quantize(ROUNDING_QUANT, rounding=ROUND_HALF_EVEN))


def _render_scorecard(output: dict[str, Any]) -> str:
    lines = [
        "# Three-Channel V1 Scorecard",
        "",
        "Date: 2026-05-19",
        "Status: internal_v1_recompute_not_external_ready",
        "",
        "## Method",
        "",
        "- V1 applies `SAS-V1-002` review decisions to V0 evaluated claims.",
        "- Reviewed false positives and `needs_context` rows are excluded.",
        "- Reviewed false negatives are counted as pending extraction, "
        "not wins/losses.",
        "- No unreviewed media claim is included.",
        "- No bulk market-history database is used.",
        "",
        "## Channel Scorecard",
        "",
        "| Channel | Coverage | Extraction quality | Outcome quality | "
        "Risk quality | Evidence limitations |",
        "|---|---:|---|---|---|---|",
    ]
    for row in output["channel_summaries"]:
        excluded = row["exclusion_counts"].get("review_false_positive", 0) + row[
            "exclusion_counts"
        ].get("review_needs_context", 0)
        lines.append(
            "| {source_id} | {v1}/{v0} evaluable | reviewed fp/context "
            "exclusions: {excluded} | hit rate {hit_rate}%, avg return "
            "{avg}% | RR rows {rr} | false negatives pending {fn}; "
            "media excluded |".format(
                source_id=f"`{row['source_id']}`",
                v1=row["v1_evaluable_claims"],
                v0=row["v0_evaluable_claims"],
                excluded=excluded,
                hit_rate=row["primary_hit_rate"],
                avg=row["avg_directional_return_pct"],
                rr=row["rr_available_count"],
                fn=row["review_false_negative_pending"],
            )
        )
    lines.extend(
        [
            "",
            "## External Boundary",
            "",
            "This scorecard is internal. Customer-facing use still requires "
            "the V1 external-ready gate.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    main()
