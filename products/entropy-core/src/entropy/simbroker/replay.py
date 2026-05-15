"""Local no-capital SimBroker replay primitives."""

from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from entropy.models.market import OHLCVBar
from entropy.models.registry import FillLog
from entropy.simbroker.costs import CostModelConfig
from entropy.simbroker.fills import FillSignal, process_fill

LOCAL_REPLAY_SCOPE: Literal["local_broker_sandbox_no_capital_replay"] = (
    "local_broker_sandbox_no_capital_replay"
)
PRODUCT_HYPOTHESIS_DELTA: Literal["local_evidence_strengthened_not_confirmed"] = (
    "local_evidence_strengthened_not_confirmed"
)


class SandboxReplayScenario(BaseModel):
    """One local fixture scenario for no-capital replay."""

    scenario_id: str = Field(min_length=1)
    signal: FillSignal
    bar: OHLCVBar
    expected_mode: Literal["fixture_fill_only"] = "fixture_fill_only"

    @model_validator(mode="after")
    def symbol_must_match_signal(self) -> "SandboxReplayScenario":
        """Require scenario ids to remain traceable to the replayed signal."""
        if not self.scenario_id.strip():
            raise ValueError("scenario_id must not be blank")
        return self


class SandboxReplayResult(BaseModel):
    """Deterministic local replay result with explicit no-effect flags."""

    replay_id: str
    approval_scope: Literal["local_broker_sandbox_no_capital_replay"]
    scenario_count: int = Field(gt=0)
    fill_logs: tuple[FillLog, ...] = Field(min_length=1)
    replay_hash: str = Field(min_length=64, max_length=64)
    no_order_emission: bool
    no_broker_exchange_connection: bool
    no_credential_loading: bool
    no_capital_activation: bool
    no_holdout_access: bool
    product_hypothesis_delta: Literal["local_evidence_strengthened_not_confirmed"]


def run_no_capital_sandbox_replay(
    *,
    scenarios: tuple[SandboxReplayScenario, ...],
    cost_config: CostModelConfig,
    approval_scope: str,
) -> SandboxReplayResult:
    """Replay local sandbox scenarios without external order side effects."""
    if approval_scope != LOCAL_REPLAY_SCOPE:
        raise ValueError("approval_scope must be local_broker_sandbox_no_capital_replay")
    if not scenarios:
        raise ValueError("at least one replay scenario is required")

    scenario_ids = [scenario.scenario_id for scenario in scenarios]
    if len(set(scenario_ids)) != len(scenario_ids):
        raise ValueError("scenario_id values must be unique")

    fill_logs = tuple(
        process_fill(signal=scenario.signal, bar=scenario.bar, cost_config=cost_config)
        for scenario in scenarios
    )
    replay_hash = _replay_hash(
        approval_scope=approval_scope,
        scenarios=scenarios,
        cost_config=cost_config,
        fill_logs=fill_logs,
    )

    return SandboxReplayResult(
        replay_id="broker-sandbox-no-capital-replay-v1",
        approval_scope=LOCAL_REPLAY_SCOPE,
        scenario_count=len(scenarios),
        fill_logs=fill_logs,
        replay_hash=replay_hash,
        no_order_emission=True,
        no_broker_exchange_connection=True,
        no_credential_loading=True,
        no_capital_activation=True,
        no_holdout_access=True,
        product_hypothesis_delta=PRODUCT_HYPOTHESIS_DELTA,
    )


def _replay_hash(
    *,
    approval_scope: str,
    scenarios: tuple[SandboxReplayScenario, ...],
    cost_config: CostModelConfig,
    fill_logs: tuple[FillLog, ...],
) -> str:
    payload = {
        "approval_scope": approval_scope,
        "cost_config": cost_config.model_dump(mode="json"),
        "fill_logs": [fill_log.model_dump(mode="json") for fill_log in fill_logs],
        "scenarios": [scenario.model_dump(mode="json") for scenario in scenarios],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


__all__ = [
    "LOCAL_REPLAY_SCOPE",
    "PRODUCT_HYPOTHESIS_DELTA",
    "SandboxReplayResult",
    "SandboxReplayScenario",
    "run_no_capital_sandbox_replay",
]
