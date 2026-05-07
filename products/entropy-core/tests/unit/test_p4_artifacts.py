"""Unit tests for P4 label artifact generation."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from entropy.evidence import P4ArtifactInput, generate_p4_label_artifacts
from entropy.models.market import OHLCVBar

UTC_TS = datetime(2026, 5, 5, 12, 0, tzinfo=timezone.utc)
MONDAY = datetime(2018, 1, 1, tzinfo=timezone.utc)


def make_weekday_bars(weeks: int, *, close: float = 100.0) -> list[OHLCVBar]:
    bars: list[OHLCVBar] = []
    for week_index in range(weeks):
        week_start = MONDAY + timedelta(days=7 * week_index)
        for day_index in range(5):
            bars.append(
                OHLCVBar(
                    timestamp=week_start + timedelta(days=day_index),
                    open=close,
                    high=close * 1.01,
                    low=close * 0.99,
                    close=close,
                    volume=1000.0,
                )
            )
    return bars


def test_generate_p4_label_artifacts_writes_jsonl_and_summary(tmp_path: Path) -> None:
    summary = generate_p4_label_artifacts(
        datasets={
            "SPY": P4ArtifactInput(
                symbol="SPY",
                bars=make_weekday_bars(312),
                calendar_profile="weekday",
                dataset_hash="dataset-spy",
            )
        },
        target_universe=("SPY",),
        output_dir=tmp_path,
        label_generation_ts=UTC_TS,
        required_assets=1,
        required_labeled_weeks=156,
    )

    label_path = tmp_path / "labels" / "SPY_p4_labels.jsonl"
    assert summary.gate_evidence_complete is True
    assert summary.passing_assets == 1
    assert label_path.exists()
    rows = [json.loads(line) for line in label_path.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 312
    assert rows[0]["p4_state"] == "UNLABELED"
    assert rows[-1]["p4_state"] == "mean_reverting"
    assert rows[-1]["p4_version"] == "P4-RBL-v1"
    assert rows[-1]["dataset_hash"] == "dataset-spy"
    assert rows[-1]["label_generation_ts"] == UTC_TS.isoformat()

    summary_text = (tmp_path / "P4_COVERAGE_SUMMARY.md").read_text(encoding="utf-8")
    assert "Gate evidence complete: true" in summary_text
    assert "Passing assets: 1/1" in summary_text
    assert "| SPY | weekday | dataset-spy | 1560 | 312 | 157 | true | pass |" in summary_text


def test_p4_artifact_summary_marks_insufficient_coverage(tmp_path: Path) -> None:
    summary = generate_p4_label_artifacts(
        datasets={
            "SPY": P4ArtifactInput(
                symbol="SPY",
                bars=make_weekday_bars(200),
                calendar_profile="weekday",
                dataset_hash="dataset-spy",
            )
        },
        target_universe=("SPY",),
        output_dir=tmp_path,
        label_generation_ts=UTC_TS,
        required_assets=1,
        required_labeled_weeks=156,
    )

    assert summary.gate_evidence_complete is False
    assert summary.rows[0].valid_labeled_weeks == 45
    assert summary.rows[0].reason_code == "insufficient_labeled_weeks"
    summary_text = summary.summary_path.read_text(encoding="utf-8")
    assert "Gate evidence complete: false" in summary_text


def test_p4_artifact_summary_tracks_missing_target_asset(tmp_path: Path) -> None:
    summary = generate_p4_label_artifacts(
        datasets={},
        target_universe=("SPY",),
        output_dir=tmp_path,
        label_generation_ts=UTC_TS,
        required_assets=1,
        required_labeled_weeks=156,
    )

    assert summary.gate_evidence_complete is False
    assert summary.rows[0].reason_code == "missing_dataset"
    assert summary.rows[0].artifact_path is None
    assert "missing_dataset" in summary.summary_path.read_text(encoding="utf-8")


def test_p4_artifact_rejects_duplicate_universe_symbols(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="unique"):
        generate_p4_label_artifacts(
            datasets={},
            target_universe=("SPY", "SPY"),
            output_dir=tmp_path,
            label_generation_ts=UTC_TS,
        )


def test_p4_artifact_rejects_symbol_mismatch(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="dataset symbol"):
        generate_p4_label_artifacts(
            datasets={
                "SPY": P4ArtifactInput(
                    symbol="QQQ",
                    bars=make_weekday_bars(312),
                    calendar_profile="weekday",
                    dataset_hash="dataset-qqq",
                )
            },
            target_universe=("SPY",),
            output_dir=tmp_path,
            label_generation_ts=UTC_TS,
        )
