"""Statistical helper stubs for Phase 0 foundation work."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from math import erf, sqrt
from random import Random
from statistics import StatisticsError, mean, stdev
from typing import Literal, Sequence

CI_METHOD_ID = "CI-SR-ACF-v1"
HARVEY_LIU_METHOD_ID = "HL-HB-v1"
STUB_REASON_CODE = "stub_pending_formula_verification"
HARVEY_LIU_FAMILY_REASON_CODE = "family_workflow_verified"


@dataclass(frozen=True)
class SharpeCIResult:
    """Sharpe confidence interval output with canonical report metadata."""

    lower: float
    upper: float
    sharpe_estimate: float
    standard_error: float
    n: int
    lag: int
    autocorrelations: tuple[float, ...]
    autocorrelation_hash: str
    n_eff: float
    t_eff_years: float
    annualization_factor: int
    return_frequency: str
    policy_hash: str
    method_id: str = CI_METHOD_ID
    reason_code: str = STUB_REASON_CODE

    def as_tuple(self) -> tuple[float, float]:
        return (self.lower, self.upper)

    def __iter__(self):
        return iter(self.as_tuple())


@dataclass(frozen=True)
class DeflatedSharpe:
    """Harvey-Liu deflation output."""

    raw_value: float
    deflated_value: float
    haircut_units: float
    method_id: str
    M_total: int
    sample_length: int
    p_value: float
    adjusted_p_value: float
    trial_id: str = ""
    family_tag: str = ""
    family_membership: tuple[str, ...] = field(default_factory=tuple)
    sorted_rank: int = 0
    se_sharpe_annual: float = 0.0
    return_frequency: str = ""
    code_hash: str = ""
    policy_hash: str = ""
    reason_code: str = STUB_REASON_CODE


@dataclass(frozen=True)
class HarveyLiuTrial:
    """Single family member for the `HL-HB-v1` workflow."""

    trial_id: str
    family_tag: str
    raw_sharpe_annual: float
    se_sharpe_annual: float
    sample_length: int
    return_frequency: str
    code_hash: str
    policy_hash: str


def compute_sharpe_estimate(
    returns: Sequence[float],
    *,
    annualization_factor: int = 252,
) -> float:
    """Compute a simple annualized Sharpe point estimate from supplied returns."""
    _validate_returns(returns)
    sample_stdev = stdev(returns)
    if sample_stdev == 0:
        raise ValueError("returns must have nonzero sample standard deviation")
    return mean(returns) / sample_stdev * sqrt(annualization_factor)


def compute_sharpe_ci(
    returns: Sequence[float],
    *,
    method: Literal["analytical", "bootstrap"] = "analytical",
    annualization_factor: int = 252,
    return_frequency: str = "daily",
    lag: int = 0,
    autocorrelations: Sequence[float] | None = None,
    policy_hash: str = "policy_hash_not_supplied",
    n_bootstrap: int = 1000,
    random_seed: int = 0,
) -> SharpeCIResult:
    """Return provisional 68% Sharpe CI bounds using `CI-SR-ACF-v1`.

    The analytical path implements the canonical autocorrelation-adjusted report
    fields. The bootstrap path remains deterministic scaffold output for API and
    evidence-surface development only.
    """
    _validate_returns(returns)
    estimate = compute_sharpe_estimate(returns, annualization_factor=annualization_factor)
    resolved_autocorrelations = _resolve_autocorrelations(returns, lag, autocorrelations)
    n_eff = _compute_autocorrelation_adjusted_n_eff(len(returns), resolved_autocorrelations)
    t_eff_years = n_eff / annualization_factor
    standard_error = sqrt((1 + estimate**2 / 2) / t_eff_years)
    if method == "analytical":
        return SharpeCIResult(
            lower=estimate - standard_error,
            upper=estimate + standard_error,
            sharpe_estimate=estimate,
            standard_error=standard_error,
            n=len(returns),
            lag=lag,
            autocorrelations=resolved_autocorrelations,
            autocorrelation_hash=_hash_autocorrelations(resolved_autocorrelations),
            n_eff=n_eff,
            t_eff_years=t_eff_years,
            annualization_factor=annualization_factor,
            return_frequency=return_frequency,
            policy_hash=policy_hash,
        )
    if method == "bootstrap":
        if n_bootstrap <= 0:
            raise ValueError("n_bootstrap must be positive")
        estimates = _bootstrap_sharpe_estimates(
            returns,
            annualization_factor=annualization_factor,
            n_bootstrap=n_bootstrap,
            random_seed=random_seed,
        )
        lower = _quantile(estimates, 0.16)
        upper = _quantile(estimates, 0.84)
        if lower == upper:
            lower, upper = min(lower, estimate), max(upper, estimate)
        return SharpeCIResult(
            lower=lower,
            upper=upper,
            sharpe_estimate=estimate,
            standard_error=standard_error,
            n=len(returns),
            lag=lag,
            autocorrelations=resolved_autocorrelations,
            autocorrelation_hash=_hash_autocorrelations(resolved_autocorrelations),
            n_eff=n_eff,
            t_eff_years=t_eff_years,
            annualization_factor=annualization_factor,
            return_frequency=return_frequency,
            policy_hash=policy_hash,
        )
    raise ValueError("method must be 'analytical' or 'bootstrap'")


def compute_harvey_liu_deflation(
    *,
    raw_sharpe: float,
    M_total: int,
    sample_length: int,
    annualization_factor: int = 252,
) -> DeflatedSharpe:
    """STUB: formula pending independent reproducibility verification.

    This skeleton follows the documented `HL-HB-v1` shape for Phase 0 API
    development. It is not phase-gate proof and must not be used for OOS claims.
    """
    if M_total < 1:
        raise ValueError("M_total must be at least 1")
    if sample_length < 2:
        raise ValueError("sample_length must be at least 2")
    t_eff_years = sample_length / annualization_factor
    standard_error = sqrt((1 + raw_sharpe**2 / 2) / t_eff_years)
    z_value = raw_sharpe / standard_error
    p_value = 1 - _normal_cdf(z_value)
    adjusted_p_value = min(1.0, M_total * p_value)
    deflated_z = _inverse_normal_cdf(1 - adjusted_p_value)
    deflated_value = deflated_z * standard_error
    return DeflatedSharpe(
        raw_value=raw_sharpe,
        deflated_value=deflated_value,
        haircut_units=raw_sharpe - deflated_value,
        method_id=HARVEY_LIU_METHOD_ID,
        M_total=M_total,
        sample_length=sample_length,
        p_value=p_value,
        adjusted_p_value=adjusted_p_value,
    )


def compute_harvey_liu_family(
    trials: Sequence[HarveyLiuTrial],
    *,
    M_total: int | None = None,
) -> tuple[DeflatedSharpe, ...]:
    """Compute `HL-HB-v1` family deflation with Holm-Bonferroni adjustment.

    The input must be the full family table for one decision family. `M_total`
    must match the family membership count, which blocks accidental gate/report
    use when any family member p-value is missing.
    """
    if not trials:
        raise ValueError("at least one Harvey-Liu trial is required")
    resolved_M_total = len(trials) if M_total is None else M_total
    if resolved_M_total != len(trials):
        raise ValueError("M_total must equal family membership count")

    _validate_harvey_liu_trials(trials)
    family_membership = tuple(trial.trial_id for trial in trials)
    p_values_by_trial_id = {
        trial.trial_id: 1 - _normal_cdf(trial.raw_sharpe_annual / trial.se_sharpe_annual)
        for trial in trials
    }
    sorted_trial_ids = sorted(
        p_values_by_trial_id,
        key=lambda trial_id: (p_values_by_trial_id[trial_id], trial_id),
    )
    adjusted_by_trial_id: dict[str, float] = {}
    rank_by_trial_id: dict[str, int] = {}
    monotonic_adjusted_p = 0.0
    for zero_based_rank, trial_id in enumerate(sorted_trial_ids):
        rank = zero_based_rank + 1
        holm_multiplier = resolved_M_total - zero_based_rank
        holm_p = min(1.0, holm_multiplier * p_values_by_trial_id[trial_id])
        monotonic_adjusted_p = max(monotonic_adjusted_p, holm_p)
        adjusted_by_trial_id[trial_id] = monotonic_adjusted_p
        rank_by_trial_id[trial_id] = rank

    return tuple(
        _build_harvey_liu_result(
            trial,
            M_total=resolved_M_total,
            family_membership=family_membership,
            p_value=p_values_by_trial_id[trial.trial_id],
            adjusted_p_value=adjusted_by_trial_id[trial.trial_id],
            sorted_rank=rank_by_trial_id[trial.trial_id],
        )
        for trial in trials
    )


def compute_n_eff(*, k: int, rho_avg: float) -> float:
    """Compute the documented K3 effective factor count estimator."""
    if k < 1:
        raise ValueError("k must be at least 1")
    if k == 1:
        return 1.0
    denominator = 1 + (k - 1) * rho_avg
    if denominator <= 0:
        raise ValueError("rho_avg produces a nonpositive denominator")
    return k / denominator


def _validate_returns(returns: Sequence[float]) -> None:
    if len(returns) < 2:
        raise ValueError("at least two returns are required")


def _resolve_autocorrelations(
    returns: Sequence[float],
    lag: int,
    supplied_autocorrelations: Sequence[float] | None,
) -> tuple[float, ...]:
    if lag < 0:
        raise ValueError("lag must be nonnegative")
    if lag >= len(returns):
        raise ValueError("lag must be smaller than return count")
    if supplied_autocorrelations is not None:
        if len(supplied_autocorrelations) != lag:
            raise ValueError("autocorrelations length must equal lag")
        return tuple(float(value) for value in supplied_autocorrelations)
    return tuple(_sample_autocorrelation(returns, current_lag) for current_lag in range(1, lag + 1))


def _sample_autocorrelation(returns: Sequence[float], lag: int) -> float:
    if lag <= 0:
        raise ValueError("lag must be positive")
    if lag >= len(returns):
        raise ValueError("lag must be smaller than return count")
    average = mean(returns)
    denominator = sum((value - average) ** 2 for value in returns)
    if denominator == 0:
        raise ValueError("returns must have nonzero variance")
    numerator = sum(
        (returns[index] - average) * (returns[index - lag] - average)
        for index in range(lag, len(returns))
    )
    return numerator / denominator


def _compute_autocorrelation_adjusted_n_eff(
    sample_size: int,
    autocorrelations: Sequence[float],
) -> float:
    lag = len(autocorrelations)
    denominator = 1 + 2 * sum(
        (1 - (index + 1) / (lag + 1)) * rho for index, rho in enumerate(autocorrelations)
    )
    if denominator <= 0:
        raise ValueError("autocorrelation adjustment produced nonpositive n_eff denominator")
    n_eff = sample_size / denominator
    if n_eff <= 0:
        raise ValueError("n_eff must be positive")
    return n_eff


def _validate_harvey_liu_trials(trials: Sequence[HarveyLiuTrial]) -> None:
    seen_trial_ids: set[str] = set()
    family_tags: set[str] = set()
    for trial in trials:
        if not trial.trial_id.strip():
            raise ValueError("trial_id must not be blank")
        if trial.trial_id in seen_trial_ids:
            raise ValueError("duplicate trial_id in Harvey-Liu family")
        seen_trial_ids.add(trial.trial_id)
        if not trial.family_tag.strip():
            raise ValueError("family_tag must not be blank")
        family_tags.add(trial.family_tag)
        if trial.se_sharpe_annual <= 0:
            raise ValueError("se_sharpe_annual must be positive")
        if trial.sample_length < 2:
            raise ValueError("sample_length must be at least 2")
        if not trial.return_frequency.strip():
            raise ValueError("return_frequency must not be blank")
        if not trial.code_hash.strip():
            raise ValueError("code_hash must not be blank")
        if not trial.policy_hash.strip():
            raise ValueError("policy_hash must not be blank")
    if len(family_tags) != 1:
        raise ValueError("Harvey-Liu trials must share one family_tag")


def _build_harvey_liu_result(
    trial: HarveyLiuTrial,
    *,
    M_total: int,
    family_membership: tuple[str, ...],
    p_value: float,
    adjusted_p_value: float,
    sorted_rank: int,
) -> DeflatedSharpe:
    deflated_z = _inverse_normal_cdf(1 - adjusted_p_value)
    deflated_value = deflated_z * trial.se_sharpe_annual
    return DeflatedSharpe(
        raw_value=trial.raw_sharpe_annual,
        deflated_value=deflated_value,
        haircut_units=trial.raw_sharpe_annual - deflated_value,
        method_id=HARVEY_LIU_METHOD_ID,
        M_total=M_total,
        sample_length=trial.sample_length,
        p_value=p_value,
        adjusted_p_value=adjusted_p_value,
        trial_id=trial.trial_id,
        family_tag=trial.family_tag,
        family_membership=family_membership,
        sorted_rank=sorted_rank,
        se_sharpe_annual=trial.se_sharpe_annual,
        return_frequency=trial.return_frequency,
        code_hash=trial.code_hash,
        policy_hash=trial.policy_hash,
        reason_code=HARVEY_LIU_FAMILY_REASON_CODE,
    )


def _hash_autocorrelations(autocorrelations: Sequence[float]) -> str:
    payload = json.dumps(
        [f"{value:.17g}" for value in autocorrelations],
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _bootstrap_sharpe_estimates(
    returns: Sequence[float],
    *,
    annualization_factor: int,
    n_bootstrap: int,
    random_seed: int,
) -> list[float]:
    rng = Random(random_seed)
    estimates: list[float] = []
    sample_size = len(returns)
    for _ in range(n_bootstrap):
        sample = [returns[rng.randrange(sample_size)] for _ in range(sample_size)]
        try:
            estimates.append(
                compute_sharpe_estimate(sample, annualization_factor=annualization_factor)
            )
        except (StatisticsError, ValueError):
            estimates.append(0.0)
    estimates.sort()
    return estimates


def _quantile(values: Sequence[float], q: float) -> float:
    if not values:
        raise ValueError("values must not be empty")
    if q < 0 or q > 1:
        raise ValueError("q must be in [0, 1]")
    index = q * (len(values) - 1)
    lower_index = int(index)
    upper_index = min(lower_index + 1, len(values) - 1)
    weight = index - lower_index
    return values[lower_index] * (1 - weight) + values[upper_index] * weight


def _normal_cdf(value: float) -> float:
    return 0.5 * (1 + erf(value / sqrt(2)))


def _inverse_normal_cdf(probability: float) -> float:
    if probability <= 0:
        return float("-inf")
    if probability >= 1:
        return float("inf")

    # Peter J. Acklam's rational approximation, sufficient for deterministic
    # Phase 0 worked examples without adding a SciPy dependency.
    a = (
        -3.969683028665376e01,
        2.209460984245205e02,
        -2.759285104469687e02,
        1.383577518672690e02,
        -3.066479806614716e01,
        2.506628277459239e00,
    )
    b = (
        -5.447609879822406e01,
        1.615858368580409e02,
        -1.556989798598866e02,
        6.680131188771972e01,
        -1.328068155288572e01,
    )
    c = (
        -7.784894002430293e-03,
        -3.223964580411365e-01,
        -2.400758277161838e00,
        -2.549732539343734e00,
        4.374664141464968e00,
        2.938163982698783e00,
    )
    d = (
        7.784695709041462e-03,
        3.224671290700398e-01,
        2.445134137142996e00,
        3.754408661907416e00,
    )
    low = 0.02425
    high = 1 - low
    if probability < low:
        q = sqrt(-2 * _ln(probability))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
            (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
        )
    if probability <= high:
        q = probability - 0.5
        r = q * q
        return (
            (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5])
            * q
            / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)
        )
    q = sqrt(-2 * _ln(1 - probability))
    return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / (
        (((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1
    )


def _ln(value: float) -> float:
    from math import log

    return log(value)


__all__ = [
    "CI_METHOD_ID",
    "HARVEY_LIU_METHOD_ID",
    "HARVEY_LIU_FAMILY_REASON_CODE",
    "STUB_REASON_CODE",
    "DeflatedSharpe",
    "HarveyLiuTrial",
    "SharpeCIResult",
    "compute_harvey_liu_family",
    "compute_harvey_liu_deflation",
    "compute_n_eff",
    "compute_sharpe_ci",
    "compute_sharpe_estimate",
]
