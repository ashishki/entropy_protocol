# Era 0 — Specification Hardening Phase

**Status:** Proposed — awaiting human sponsor approval
**Addresses:** Audit findings F-1, F-2, F-4
**Blocks:** Phase 0 exit certification; Phase 1 evaluation

---

## Context

The Entropy Protocol has complete governance documentation but cannot be implemented. Three P0-blocking audit findings make core computations non-reproducible:

- **F-4** — P4 regime algorithm is required for Phase 0 exit but does not exist anywhere in the specification
- **F-1** — Harvey-Liu deflation formula is named (`HL-HB-v1`) but no formula, inputs, or computation steps are provided
- **F-2** — Sharpe CI is referenced (`CI-SR-ACF-v1`) but has no formula; the charter's stated ±0.15–0.20 value is incorrect by a factor of ~5× at 15 months OOS

No phase gate can be evaluated until all three are resolved.

Era 0 closes these gaps with minimal viable specifications. No new features. No scope expansion.

---

## Era 0 Definition

| Field | Value |
|---|---|
| Classification | Specification Hardening Phase |
| Prerequisite | None — begins immediately |
| Blocks | Phase 0 exit (P4), Phase 1 evaluation (HL-HB-v1, CI-SR-ACF-v1) |
| Exit condition | All three specs approved by named human sponsor and merged into core docs |

---

## Task List

| ID | Blocker | Deliverable | Finding |
|---|---|---|---|
| ERA0-1 | P4 algorithm undefined | P4-v1 spec approved | F-4 |
| ERA0-2 | Harvey-Liu formula absent | HL-HB-v1 canonical formula approved | F-1 |
| ERA0-3 | Sharpe CI formula absent | CI-SR-ACF-v1 canonical formula approved | F-2 |
| ERA0-4 | Integration | Approved specs merged into PROTOCOL_SPEC.md, GLOSSARY.md, CHARTER.md, EVOLUTION.md | — |

---

## Blocker Specs

---

### ERA0-1: P4 Weekly Regime Signal — P4-v1

**Purpose:** Produce a historically reproducible weekly regime label per asset. Required by Phase 0 exit criterion: "P4 signal producing labeled series covering ≥3 years on ≥15 of 20 target assets."

**Output states** (from PROTOCOL_SPEC.md §D): `TRENDING` | `MEAN_REVERTING` | `STRESS`

#### Inputs

| Field | Type | Definition |
|---|---|---|
| `weekly_close[a, t]` | float | Last bar close of calendar week, UTC midnight Sunday |
| `asset_list` | list | Target universe, ≥15 assets |
| `t` | date | ISO week-ending Sunday |

#### Frozen parameters (locked at P4-v1)

| Parameter | Value | Rationale |
|---|---|---|
| `fast_window` | 10 weeks | Standard trend filter |
| `slow_window` | 40 weeks | Standard trend filter |
| `trend_band` | 0.02 (2%) | Separation threshold to avoid whipsaw |
| `vol_window` | 4 weeks | Short-window realized vol |
| `vol_baseline_window` | 52 weeks | Long-window baseline vol |
| `stress_multiplier` | 2.0 | Short vol > 2× baseline → STRESS |
| `min_history` | 52 weeks | Minimum weeks to produce a valid label |

#### Computation (per asset `a`, per week `t`)

```
# Require 52 prior weekly closes; emit null label otherwise

weekly_returns[a, t] = ln(weekly_close[a, t] / weekly_close[a, t-1])

SMA_fast[a, t] = mean(weekly_close[a, t-9 : t+1])    # 10-week window, end-inclusive
SMA_slow[a, t] = mean(weekly_close[a, t-39 : t+1])   # 40-week window, end-inclusive

RV4[a, t]  = std(weekly_returns[a, t-3 : t+1]) * sqrt(52)   # annualized 4-week vol
RV52[a, t] = std(weekly_returns[a, t-51 : t+1]) * sqrt(52)  # annualized 52-week vol

# Label rule — evaluate in order; first match wins
if RV52[a, t] > 0 AND RV4[a, t] > stress_multiplier * RV52[a, t]:
    label[a, t] = STRESS
elif abs(SMA_fast[a, t] - SMA_slow[a, t]) / SMA_slow[a, t] > trend_band:
    label[a, t] = TRENDING
else:
    label[a, t] = MEAN_REVERTING
```

#### Constraints

- Label is emitted using only data available at end-of-week `t` close. No lookahead.
- All MA windows use a simple arithmetic mean. No exponential weighting.
- Missing close: if any bar in the required window is missing, emit `null` for that asset-week.
- Label is immutable once emitted for a closed week. No retroactive re-labeling.

#### Outputs (per asset-week)

```
{
  asset_id:   string,
  week_end:   ISO date (Sunday),
  label:      TRENDING | MEAN_REVERTING | STRESS | null,
  SMA_fast:   float,
  SMA_slow:   float,
  RV4:        float,
  RV52:       float,
  p4_version: "P4-v1",
  param_hash: sha256(parameter dict),
  data_hash:  sha256(input slice)
}
```

#### Vintage artifact (mandatory on every Phase gate report)

```
{
  p4_version:           "P4-v1",
  param_hash:           sha256(parameter dict),
  calibration_end_ts:   null,   # rule-based; no calibration window
  label_generation_ts:  ISO timestamp,
  dataset_hash:         sha256(input dataset)
}
```

---

### ERA0-2: Harvey-Liu Deflated Sharpe — HL-HB-v1

**Purpose:** Quantify multiplicity penalty on a strategy's net Sharpe given total trial count. Mandatory when net Sharpe < 0.40 per NN-5.

**Method base:** Bailey & López de Prado (2014), "The Deflated Sharpe Ratio."

**Rationale for method choice:** The Bailey-López de Prado DSR provides a scalar probability output (DSR ∈ (0,1)) and a haircut in interpretable Sharpe units. It accounts for the expected maximum SR under the null across M_total strategies — which is exactly what the system needs: not just a p-value threshold, but a quantified deflation relative to the search surface. Bonferroni and Holm-Bonferroni alternatives were considered but produce only a pass/fail at a fixed threshold; they do not produce the haircut-in-units output the spec requires.

#### Inputs

| Field | Type | Definition |
|---|---|---|
| `SR_hat` | float | Annualized net Sharpe (streams a+b+c; CI-SR-ACF-v1 point estimate) |
| `T` | int | Number of trading-day observations in the evaluation window |
| `M_total` | int | Total trial count from Trial Registry at evaluation date (Main + AT + RDL-*) |
| `skew` | float | Third standardized moment of bar-level returns; default `0.0` if unavailable |
| `kurt` | float | Fourth standardized moment of bar-level returns; default `3.0` if unavailable |

#### Computation

```
# Step 1 — De-annualize
SR_bar = SR_hat / sqrt(252)

# Step 2 — Standard error of bar-level Sharpe (Lo 2002)
sigma_SR = sqrt((1/T) * (1 - skew * SR_bar + (kurt - 1) / 4 * SR_bar^2))

# Step 3 — Expected maximum Sharpe under the null
# (iid, SR_true = 0 for all M_total strategies)
# Bailey-López de Prado (2014), equation (4)
gamma_em = 0.5772156649          # Euler-Mascheroni constant
z1 = Phi_inv(1 - 1 / M_total)
z2 = Phi_inv(1 - 1 / (e * M_total))   # e = 2.71828...
E_SR_max = (1 - gamma_em) * z1 + gamma_em * z2   # in sigma_SR units

# Step 4 — Deflated Sharpe probability
DSR = Phi((SR_bar - E_SR_max) / sigma_SR)
# DSR ∈ (0,1): probability the observed SR exceeds expected max under the null

# Step 5 — Haircut in annualized Sharpe units
haircut = E_SR_max * sigma_SR * sqrt(252)

# Step 6 — Deflated Sharpe in annualized units
deflated_SR = SR_hat - haircut

# Step 7 — Pass/fail
passes = (DSR > 0.95)
```

#### Outputs

```
{
  deflated_SR:  float,   # annualized; can be negative
  haircut:      float,   # annualized Sharpe units
  DSR:          float,   # probability ∈ (0,1)
  passes:       bool,    # DSR > 0.95
  E_SR_max:     float,   # for audit (bar-level sigma units)
  sigma_SR:     float,   # for audit (bar-level)
  M_total:      int,
  T:            int,
  method_id:    "HL-HB-v1"
}
```

#### Reporting rule

Every evaluation report must include `{SR_hat, deflated_SR, haircut, DSR, M_total, T}`. Raw Sharpe alone is not sufficient.

#### Correction to existing Phase 1 exit criterion

The current spec states "Harvey-Liu haircut < 0.05 Sharpe units" as a Phase 1 exit requirement. This threshold is inconsistent with the formula.

At T = 315 trading days (15 months) and M_total = 10:
- `sigma_SR` ≈ 0.056 (bar-level)
- `E_SR_max` ≈ 1.75 (expected max of 10 standard normals)
- `haircut` = 1.75 × 0.056 × √252 ≈ **1.55 annualized Sharpe units**

The 0.05 threshold is unreachable at any realistic M_total and T. The operative Phase 1 exit test is `passes = True` (DSR > 0.95). The "haircut < 0.05" line in PROTOCOL_SPEC.md §F and CHARTER.md must be replaced.

---

### ERA0-3: Sharpe Confidence Interval — CI-SR-ACF-v1

**Purpose:** Compute the 68% autocorrelation-consistent confidence interval for net Sharpe. Mandatory on all evaluation outputs.

**Method base:** Newey-West (1987) HAC estimator; Lo (2002) base Sharpe SE formula.

**Rationale for method choice:** Lo (2002) provides the standard SE formula for Sharpe ratios under non-normality. Newey-West with Bartlett kernel is the canonical HAC estimator for autocorrelation-consistent variance. The lag window `L = floor(T^(1/3))` follows Andrews (1991) and is the standard data-driven rule requiring no preregistration judgment per evaluation window.

#### Inputs

| Field | Type | Definition |
|---|---|---|
| `r` | float[T] | Bar-level net returns (streams a+b+c) in chronological order |
| `frequency` | enum | `"4H"` or `"1D"` |

**Derived constants:**

| `frequency` | `bars_per_year` |
|---|---|
| `"1D"` | 252 |
| `"4H"` | 1512 (= 252 × 6) |

#### Computation

```
T = len(r)

# Step 1 — Annualized Sharpe estimate
SR_bar = mean(r) / std(r, ddof=1)
SR_hat = SR_bar * sqrt(bars_per_year)

# Step 2 — Lag window (Andrews 1991 / Newey-West rule)
L = max(2, floor(T ^ (1/3)))

# Step 3 — Sample autocorrelations of returns
rho[q] = Pearson_corr(r[0 : T-q], r[q : T])   for q = 1..L

# Step 4 — Bartlett-weighted autocorrelation sum (Newey-West kernel)
NW_adj = 1 + 2 * sum_{q=1}^{L} (1 - q / (L + 1)) * rho[q]
NW_adj = max(NW_adj, 1.0)   # floor: cannot reduce SE below iid baseline

# Step 5 — Base SE (Lo 2002, bar-level)
SE_base = sqrt((1 + 0.5 * SR_bar^2) / T)

# Step 6 — Autocorrelation-consistent SE (bar-level)
SE_AC = SE_base * sqrt(NW_adj)

# Step 7 — Annualized SE
SE_annual = SE_AC * sqrt(bars_per_year)

# Step 8 — 68% CI (one standard error, two-sided)
CI_lower = SR_hat - SE_annual
CI_upper = SR_hat + SE_annual
```

#### Outputs

```
{
  SR_hat:        float,                 # annualized
  CI_68:         [CI_lower, CI_upper],  # annualized
  SE_annual:     float,
  L:             int,    # lag window used
  NW_adj:        float,  # autocorrelation adjustment factor (≥ 1.0)
  T:             int,
  bars_per_year: int,
  method_id:     "CI-SR-ACF-v1"
}
```

#### Reference computation (for audit verification)

At T = 315 trading days, iid returns, SR_hat = 0.35:

```
L       = floor(315 ^ (1/3)) = floor(6.80) = 6
NW_adj  = 1.0   (no autocorrelation)
SE_base = sqrt(1 / 315)      = 0.0563  (bar-level)
SE_annual = 0.0563 * sqrt(252) = 0.894
CI_68   = [0.35 − 0.894, 0.35 + 0.894] = [−0.544, 1.244]
```

#### Correction to existing charter claim

The CHARTER.md and PROTOCOL_SPEC.md state the CI at 15 months OOS is approximately ±0.15–0.20. The correct value under this formula is **±0.89** (iid case) and potentially wider if returns exhibit positive autocorrelation.

The ±0.15–0.20 value would require approximately T = 252/(0.17)² ≈ **8,700 trading days (34 years)** of data to achieve with iid returns.

Consequence: K1 (kill if net Sharpe < 0.28 after 15 months) is operating on a metric whose 68% CI spans [−0.54, 1.24] at the kill evaluation point. This does not make K1 invalid — K1 uses the point estimate, not the CI — but all planning language implying precision at 15 months must be removed.

---

## Era 0 Exit Criteria

All of the following must be satisfied before Phase 0 exit certification is valid:

| # | Criterion | Verification |
|---|---|---|
| 1 | P4-v1 spec approved by named human sponsor | Confirmation logged in EVOLUTION.md as closed decision |
| 2 | HL-HB-v1 spec approved by named human sponsor | Same |
| 3 | CI-SR-ACF-v1 spec approved by named human sponsor | Same |
| 4 | PROTOCOL_SPEC.md §D updated: P4-v1 algorithm text present | Reviewer confirms |
| 5 | PROTOCOL_SPEC.md §F updated: "haircut < 0.05" replaced with "passes = True (DSR > 0.95)" | Reviewer confirms |
| 6 | GLOSSARY.md updated: HL-HB-v1 and CI-SR-ACF-v1 entries contain formula text | Reviewer confirms |
| 7 | CHARTER.md updated: ±0.15–0.20 CI claim removed; "haircut < 0.05" exit criterion replaced | Reviewer confirms |
| 8 | EVOLUTION.md updated: decisions 12, 13, 14 added (one per blocker, with alternatives rejected) | Reviewer confirms |

**No implementation work begins until all exit criteria are met. Spec approval precedes build.**

---

## Files to Modify (ERA0-4)

| File | Section | Required change |
|---|---|---|
| `docs/core/PROTOCOL_SPEC.md` | §D Regime Signal Governance | Add P4-v1 algorithm block |
| `docs/core/PROTOCOL_SPEC.md` | §F Phase 1 exit criteria | Replace "haircut < 0.05" with "passes = True (DSR > 0.95)" |
| `docs/core/GLOSSARY.md` | Deflated Sharpe (Harvey-Liu) | Replace placeholder with HL-HB-v1 full formula |
| `docs/core/GLOSSARY.md` | Net Sharpe CI reference | Replace placeholder with CI-SR-ACF-v1 full formula |
| `docs/core/CHARTER.md` | Phase 1 metrics table | Replace "haircut < 0.05" row; add DSR > 0.95 |
| `docs/core/CHARTER.md` | Any ±0.15–0.20 CI language | Remove or replace with correct ±0.89 reference |
| `docs/core/EVOLUTION.md` | Closed decisions summary | Add decisions 12 (P4-v1), 13 (HL-HB-v1), 14 (CI-SR-ACF-v1) |
