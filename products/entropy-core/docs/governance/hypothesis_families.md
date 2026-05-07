# Entropy Protocol — Hypothesis Families

**Version:** 1.0
**Last updated:** 2026-03-16
**Purpose:** Define the canonical hypothesis families used to classify experiments and control multiplicity risk.

---

## Why Family Assignment Is Mandatory

Hypothesis family assignment prevents the Trial Registry from behaving like one undifferentiated pool of ideas.

It is required because:
- related ideas compound multiplicity risk
- repeated variants of the same idea can hide effective trial count
- family-level review makes research concentration visible
- promotion decisions are more defensible when a candidate is evaluated against its true comparison set

Every registered experiment must declare one primary family.

---

## Canonical Families

### Funding Signals

Signals based on borrow cost, perpetual funding, basis pressure, or financing stress.

### Volatility Compression

Signals based on realized-vol contraction, range compression, breakout setup structure, or pre-expansion conditions.

### Structure Levels

Signals based on prior highs/lows, VWAP, session levels, monthly or weekly reference levels, or other explicit price structure markers.

### Regime-Conditioned Signals

Signals whose expected behavior depends on regime state, including trending, mean-reverting, stress, or other governed regime labels.

### Liquidity / Flow Signals

Signals based on exchange flows, stablecoin flows, onchain transfer pressure, order-flow imbalance, or related liquidity proxies.

---

## Family Governance Rules

- Family assignment happens before registration.
- A new variant in an existing family still counts as a new trial.
- Reclassifying a hypothesis after results are observed is prohibited.
- If a proposal spans multiple families, one primary family must be declared and the secondary linkage noted in the registry.

## Hypothesis Budget

To prevent uncontrolled expansion of the research surface, the governance baseline budget is:
- maximum 3 new hypotheses per week
- maximum 1 active hypothesis per family

These limits apply to net-new experiments entering active evaluation.

If a team wants to exceed the baseline budget, the exception must be logged with explicit rationale and linked to the Trial Registry.

The budget exists to:
- constrain multiplicity growth
- force prioritization across related ideas
- reduce hidden search pressure from AI-assisted ideation
- keep the evaluation surface operationally reviewable

---

## Review Use

Family tags are used to:
- monitor concentration of research effort
- detect repeated testing of near-equivalent ideas
- support Harvey-Liu-aware multiplicity review
- keep the RDL and main evaluation protocol aligned on what kind of evidence is being generated

---

## Canonical Family Names as Authoritative Scope References

The five canonical family names defined above are the authoritative identifiers used as `scope` values in Research Portfolio Monitor (RPM) Attention Signal (ATT) conditions and in the RPM family status table. RPM displays are organized by these names.

Any change to a canonical family name requires a corresponding update to all ATT condition entries in the RPM configuration document. Family definitions here govern; the RPM inherits from them.

See: `products/entropy-core/docs/governance/research_portfolio_monitor.md`
