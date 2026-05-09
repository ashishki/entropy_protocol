"""Simulation broker package."""

from entropy.simbroker.calibration import (
    CALIBRATION_METHOD_ID,
    NO_GATE_CLAIM,
    BidAskProvider,
    BidAskQuote,
    CalibrationAssetSummary,
    CalibrationRow,
    CalibrationSummary,
    NoOpBidAskProvider,
    build_calibration_row_from_fill,
    build_calibration_summary,
    read_calibration_rows_jsonl,
    render_calibration_summary,
    write_calibration_rows_jsonl,
)
from entropy.simbroker.costs import CostBreakdown, CostModelConfig, compute_cost
from entropy.simbroker.fills import FillSignal, process_fill
from entropy.simbroker.replay import (
    LOCAL_REPLAY_SCOPE,
    PRODUCT_HYPOTHESIS_DELTA,
    SandboxReplayResult,
    SandboxReplayScenario,
    run_no_capital_sandbox_replay,
)

__all__ = [
    "BidAskProvider",
    "BidAskQuote",
    "CALIBRATION_METHOD_ID",
    "NO_GATE_CLAIM",
    "CalibrationAssetSummary",
    "CalibrationRow",
    "CalibrationSummary",
    "CostBreakdown",
    "CostModelConfig",
    "FillSignal",
    "LOCAL_REPLAY_SCOPE",
    "NoOpBidAskProvider",
    "PRODUCT_HYPOTHESIS_DELTA",
    "SandboxReplayResult",
    "SandboxReplayScenario",
    "build_calibration_row_from_fill",
    "build_calibration_summary",
    "compute_cost",
    "process_fill",
    "read_calibration_rows_jsonl",
    "render_calibration_summary",
    "run_no_capital_sandbox_replay",
    "write_calibration_rows_jsonl",
]
