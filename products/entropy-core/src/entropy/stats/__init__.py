"""Statistics package."""

from entropy.stats.analysis import (
    CI_METHOD_ID,
    HARVEY_LIU_METHOD_ID,
    HARVEY_LIU_FAMILY_REASON_CODE,
    STUB_REASON_CODE,
    DeflatedSharpe,
    HarveyLiuTrial,
    SharpeCIResult,
    compute_harvey_liu_deflation,
    compute_harvey_liu_family,
    compute_n_eff,
    compute_sharpe_ci,
    compute_sharpe_estimate,
)

__all__ = [
    "CI_METHOD_ID",
    "HARVEY_LIU_METHOD_ID",
    "HARVEY_LIU_FAMILY_REASON_CODE",
    "STUB_REASON_CODE",
    "DeflatedSharpe",
    "HarveyLiuTrial",
    "SharpeCIResult",
    "compute_harvey_liu_deflation",
    "compute_harvey_liu_family",
    "compute_n_eff",
    "compute_sharpe_ci",
    "compute_sharpe_estimate",
]
