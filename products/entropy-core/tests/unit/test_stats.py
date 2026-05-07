"""Unit tests for statistical analysis stubs."""

from __future__ import annotations

import inspect
import math
from dataclasses import replace

import pytest

from entropy.stats import (
    HARVEY_LIU_METHOD_ID,
    STUB_REASON_CODE,
    HarveyLiuTrial,
    compute_harvey_liu_deflation,
    compute_harvey_liu_family,
    compute_n_eff,
    compute_sharpe_ci,
    compute_sharpe_estimate,
)
from entropy.stats.analysis import SharpeCIResult


def test_sharpe_ci_bounds_contain_estimate() -> None:
    returns = [0.01, 0.02, -0.005, 0.015]

    ci = compute_sharpe_ci(
        returns,
        method="analytical",
        lag=1,
        return_frequency="daily",
        policy_hash="policy",
    )
    lower, upper = ci
    sharpe_estimate = compute_sharpe_estimate(returns)

    assert isinstance(ci, SharpeCIResult)
    assert lower < sharpe_estimate < upper
    assert ci.sharpe_estimate == pytest.approx(sharpe_estimate)
    assert ci.reason_code == STUB_REASON_CODE
    assert ci.n == 4
    assert ci.lag == 1
    assert len(ci.autocorrelations) == 1
    assert len(ci.autocorrelation_hash) == 64
    assert ci.n_eff > 0
    assert ci.t_eff_years == pytest.approx(ci.n_eff / ci.annualization_factor)
    assert ci.return_frequency == "daily"
    assert ci.policy_hash == "policy"


def test_sharpe_ci_bootstrap_runs_without_error() -> None:
    returns = [0.01, 0.02, -0.005, 0.015]

    first = compute_sharpe_ci(returns, method="bootstrap", n_bootstrap=100, random_seed=7)
    second = compute_sharpe_ci(returns, method="bootstrap", n_bootstrap=100, random_seed=7)

    assert first.as_tuple() == second.as_tuple()
    assert first.lower <= first.upper
    assert first.reason_code == STUB_REASON_CODE


def test_sharpe_ci_zero_autocorrelation_15_month_example() -> None:
    target_sharpe = 0.30
    sample_stdev = 0.01
    sample_mean = target_sharpe / math.sqrt(252) * sample_stdev
    returns = [sample_mean + sample_stdev] * 157
    returns.extend([sample_mean - sample_stdev] * 157)
    returns.append(sample_mean)

    ci = compute_sharpe_ci(
        returns,
        method="analytical",
        annualization_factor=252,
        lag=0,
        policy_hash="policy",
    )

    assert ci.n == 315
    assert ci.t_eff_years == pytest.approx(1.25)
    assert ci.sharpe_estimate == pytest.approx(target_sharpe, abs=1e-12)
    assert ci.standard_error == pytest.approx(0.914, abs=0.03)
    assert ci.lower == pytest.approx(ci.sharpe_estimate - ci.standard_error)
    assert ci.upper == pytest.approx(ci.sharpe_estimate + ci.standard_error)


def test_sharpe_ci_nonzero_autocorrelation_changes_effective_years() -> None:
    returns = [0.01, 0.02, -0.005, 0.015, 0.0, 0.01]

    zero = compute_sharpe_ci(returns, lag=0)
    adjusted = compute_sharpe_ci(returns, lag=1, autocorrelations=(0.5,))

    assert adjusted.n_eff == pytest.approx(len(returns) / 1.5)
    assert adjusted.t_eff_years < zero.t_eff_years
    assert adjusted.standard_error > zero.standard_error


def test_sharpe_ci_rejects_invalid_autocorrelation_inputs() -> None:
    returns = [0.01, 0.02, -0.005, 0.015]

    with pytest.raises(ValueError, match="lag"):
        compute_sharpe_ci(returns, lag=-1)
    with pytest.raises(ValueError, match="length"):
        compute_sharpe_ci(returns, lag=2, autocorrelations=(0.1,))
    with pytest.raises(ValueError, match="nonpositive"):
        compute_sharpe_ci(returns, lag=1, autocorrelations=(-2.0,))


def test_harvey_liu_deflation_reduces_sharpe() -> None:
    docstring = inspect.getdoc(compute_harvey_liu_deflation)
    assert docstring is not None
    assert "STUB: formula pending independent reproducibility verification" in docstring

    result = compute_harvey_liu_deflation(raw_sharpe=0.35, M_total=10, sample_length=252)

    assert result.deflated_value < result.raw_value
    assert result.haircut_units > 0
    assert result.method_id == HARVEY_LIU_METHOD_ID
    assert result.reason_code == STUB_REASON_CODE


def test_harvey_liu_family_holm_bonferroni_worked_example() -> None:
    trials = _harvey_trials()

    results = compute_harvey_liu_family(trials)
    by_id = {result.trial_id: result for result in results}

    assert tuple(result.trial_id for result in results) == ("A", "B", "C")
    assert by_id["A"].method_id == HARVEY_LIU_METHOD_ID
    assert by_id["A"].M_total == 3
    assert by_id["A"].family_tag == "main-at-rdl-family"
    assert by_id["A"].family_membership == ("A", "B", "C")
    assert by_id["A"].sorted_rank == 1
    assert by_id["B"].sorted_rank == 2
    assert by_id["C"].sorted_rank == 3
    assert by_id["A"].p_value == pytest.approx(0.0808, abs=5e-4)
    assert by_id["A"].adjusted_p_value == pytest.approx(0.242, abs=5e-3)
    assert by_id["B"].adjusted_p_value == pytest.approx(0.317, abs=5e-3)
    assert by_id["C"].adjusted_p_value == pytest.approx(0.345, abs=5e-3)
    assert by_id["A"].deflated_value == pytest.approx(0.175, abs=5e-3)
    assert by_id["B"].deflated_value == pytest.approx(0.119, abs=5e-3)
    assert by_id["C"].deflated_value == pytest.approx(0.100, abs=5e-3)
    assert by_id["A"].haircut_units == pytest.approx(0.175, abs=5e-3)
    assert by_id["A"].code_hash == "code-hash"
    assert by_id["A"].policy_hash == "policy-hash"
    assert by_id["A"].reason_code != STUB_REASON_CODE


def test_harvey_liu_family_rejects_invalid_family_inputs() -> None:
    trials = _harvey_trials()

    with pytest.raises(ValueError, match="M_total"):
        compute_harvey_liu_family(trials, M_total=4)
    with pytest.raises(ValueError, match="duplicate"):
        compute_harvey_liu_family((trials[0], trials[0]))
    with pytest.raises(ValueError, match="family_tag"):
        compute_harvey_liu_family((trials[0], _replace_harvey_trial(trials[1], family_tag="")))
    with pytest.raises(ValueError, match="one family_tag"):
        compute_harvey_liu_family(
            (trials[0], _replace_harvey_trial(trials[1], family_tag="other-family"))
        )
    with pytest.raises(ValueError, match="positive"):
        compute_harvey_liu_family(
            (trials[0], _replace_harvey_trial(trials[1], se_sharpe_annual=0.0))
        )
    with pytest.raises(ValueError, match="code_hash"):
        compute_harvey_liu_family((trials[0], _replace_harvey_trial(trials[1], code_hash="")))
    with pytest.raises(ValueError, match="policy_hash"):
        compute_harvey_liu_family((trials[0], _replace_harvey_trial(trials[1], policy_hash="")))


def test_n_eff_formula_k3_worked_example() -> None:
    assert compute_n_eff(k=6, rho_avg=0.30) == pytest.approx(2.4, abs=1e-10)


def test_n_eff_single_factor() -> None:
    assert compute_n_eff(k=1, rho_avg=-0.75) == 1.0
    assert compute_n_eff(k=1, rho_avg=0.0) == 1.0
    assert compute_n_eff(k=1, rho_avg=0.90) == 1.0


def _harvey_trials() -> tuple[HarveyLiuTrial, HarveyLiuTrial, HarveyLiuTrial]:
    return (
        HarveyLiuTrial(
            trial_id="A",
            family_tag="main-at-rdl-family",
            raw_sharpe_annual=0.35,
            se_sharpe_annual=0.25,
            sample_length=252,
            return_frequency="daily",
            code_hash="code-hash",
            policy_hash="policy-hash",
        ),
        HarveyLiuTrial(
            trial_id="B",
            family_tag="main-at-rdl-family",
            raw_sharpe_annual=0.25,
            se_sharpe_annual=0.25,
            sample_length=252,
            return_frequency="daily",
            code_hash="code-hash",
            policy_hash="policy-hash",
        ),
        HarveyLiuTrial(
            trial_id="C",
            family_tag="main-at-rdl-family",
            raw_sharpe_annual=0.10,
            se_sharpe_annual=0.25,
            sample_length=252,
            return_frequency="daily",
            code_hash="code-hash",
            policy_hash="policy-hash",
        ),
    )


def _replace_harvey_trial(trial: HarveyLiuTrial, **updates: object) -> HarveyLiuTrial:
    return replace(trial, **updates)
