# Entropy Protocol Audit Questions Resolution Report

## Critical Questions

**Q-ID: A-01**

**Short restatement**  
Define a complete, reproducible **P4 weekly regime overlay algorithm** (inputs → model/thresholds → calibration → versioning → immutable labels).

**Context from the system**  
P4 is part of the regime-signal hierarchy (P1–P4) that gates routing/sizing decisions in the Portfolio Layer and is explicitly required for Phase gating evidence (Phase 0→1 and Phase 1→2). It is also a dependency for **RDL-2 (Market State Labeler)**, which references a “P4 prereg spec” that does not exist as a canonical artifact. fileciteturn0file5 fileciteturn0file0 fileciteturn0file1 fileciteturn0file2 fileciteturn0file3

**Analysis**  
The concern is **valid and gate-blocking**: multiple audit artifacts independently converge on “P4 required, algorithm undefined,” which makes regime-span claims non-reproducible and creates a governance hole large enough to invalidate Phase certification. Architecturally, P4 is not “just another model”; it is a **governance-critical labeler** whose outputs are used (a) to satisfy the “≥2 regimes” spanning requirement and (b) to justify operational changes in later phases. When the labeler is undefined, *any* later assertion that “we spanned ≥2 regimes” becomes contestable because the regime taxonomy itself is unstable. fileciteturn0file3 fileciteturn0file1 fileciteturn0file2 fileciteturn0file0

Interaction with invariants: the Phase gate invariant for P4’s historical regime series is explicitly marked non-verifiable when the algorithm is undefined, and drift tooling flags this as a P0 failure. This is not a “documentation nit”; it is a **missing state transition input** to multiple gates. fileciteturn0file2 fileciteturn0file3

Attack surfaces: the primary adversarial failure mode is **ex post regime relabeling**—even unintentionally—where labels are chosen/tuned after seeing Phase 1 performance so that (i) the system “spans two regimes” or (ii) the attribution narrative is made coherent (“stress regime explains drawdown”) without being falsifiable. The audit’s adversarial framing correctly treats this as a silent-failure route: results can look internally consistent while being structurally non-reproducible. fileciteturn0file4

Governance implications: P4 must be treated like a *consensus rule* (in distributed-systems terms), not like a research notebook. Without a versioned, immutable procedure, you cannot later prove that Phase transitions were made under consistent criteria, nor can you audit RDL-2 outputs that depend on regime semantics. fileciteturn0file5 fileciteturn0file1

**Possible Outcomes**  
A) False concern: not plausible (P4 is explicitly gate-critical).  
B) Real risk but mitigated: not supported (no canonical algorithm exists).  
C) **Real architectural gap**.  
D) Requires spec clarification: also true, but the deeper issue is absence of an implementable rule.

**Verdict: C — Real architectural gap.** fileciteturn0file3 fileciteturn0file1

**ADR Recommendation**

**Title**  
Deterministic P4 Regime Overlay Annex with Versioned Label Generation

**Problem**  
P4 is required for phase gates and RDL-2 dependency, but the system lacks a reproducible algorithm + calibration + label vintage contract. This enables evaluation non-reproducibility and governance bypass via relabeling or tuning.

**Proposed Change**  
Add a normative “P4 Annex” to the Protocol Spec that includes:
- Exact input series definitions (weekly bars; timestamp convention; missing-data rules).
- Feature set (explicit list) and normalization rules.
- Model class / thresholds (rule-based or model-based) with parameter bounds.
- Calibration protocol (walk-forward only; no full-sample fitting) and a “label vintage” artifact: `{p4_version, calibration_cutoff_ts, label_generation_ts, dataset_hash}`.
- Deterministic label-generation pseudocode that produces a full historical label series and forbids post-hoc edits.
- “Label immutability” enforcement: once a Phase 1 OOS window is evaluated, its regime labels are archived and referenced by hash in all reports.

**Impact on system layers**
- Research Layer: unblocks RDL-2 by giving it a stable regime semantic anchor; enables comparable studies across time.  
- Governance Layer: makes phase-gate evidence auditable and prevents relabeling drift.  
- Portfolio Layer: enables deterministic behavior when P4 is referenced for routing/sizing.

**Risk of change**  
Medium: forces early commitment to regime taxonomy and may reveal that “≥2 regimes” spanning is harder than assumed. This is acceptable because it surfaces reality rather than allowing uncertified progress.

**Recommended Phase**  
Phase 0 (required before Phase 0→1 certification). fileciteturn0file5 fileciteturn0file3

---

**Q-ID: A-02**

**Short restatement**  
Make P3’s correlation trigger fully deterministic: define the asset population, return interval, inclusion rules, and the rule that selects **35% vs 50%** exposure reduction.

**Context from the system**  
P3 is a governance override in the P1–P4 hierarchy (“daily correlation trigger”), acting on a 20-day rolling average pairwise correlation threshold and then reducing gross exposure over a multi-day ramp. The spec currently defines thresholds and a range of actions but leaves population and selection logic ambiguous; audit architecture flags this as an implementation-divergence risk. fileciteturn0file0 fileciteturn0file1 fileciteturn0file5 fileciteturn0file4

**Analysis**  
The concern is **valid** because P3 is a *control-plane rule* with real portfolio consequences: small definition choices (population, return frequency, weighting) can flip triggers and alter exposure materially.

Interaction with invariants: While P3 is not itself a frozen non-negotiable, it is coupled to non-negotiable goals (drawdown containment and “structural rules, not passive design”), and to phase-gate comparability because the same system can produce different OOS outcomes depending on P3 implementation. fileciteturn0file0 fileciteturn0file2

Attack surfaces:
- **Population gaming**: compute correlation on “held positions only” vs “full universe,” or exclude recently added assets, to suppress triggers.
- **Frequency gaming**: daily close-to-close vs intraday bars can materially change measured correlation.
- **Action discretion**: choosing 35% vs 50% without a deterministic rule creates post-hoc degrees of freedom: “we reduced more because it felt like stress,” which is indistinguishable from performance shaping. fileciteturn0file1 fileciteturn0file4

Governance implication: P3 must be auditable as a deterministic state transition (trigger + action) or it becomes a “manual operator lever” in disguise, which undermines the protocol’s claim that risk controls are structural. fileciteturn0file0

**Possible Outcomes**  
A) False concern: not supported (audit explicitly flags ambiguity).  
B) Real risk but mitigated: partially (threshold exists), but not enough.  
C) Real architectural gap: arguable.  
D) **Requires spec clarification**.

**Verdict: D — Requires spec clarification (determinism and population contract).** fileciteturn0file5 fileciteturn0file1

**ADR Recommendation**

**Title**  
Canonical P3 Correlation Trigger Protocol with Deterministic Action Selection

**Problem**  
P3’s trigger is defined at a high level, but population/frequency/weighting and the 35–50% action selection are underspecified, enabling divergent implementations and governance ambiguity.

**Proposed Change**  
Publish a P3 “formula block” specifying:
- Population = assets with non-zero target weight at decision time *plus* all assets eligible in the active Phase universe (choose one and lock it).
- Return interval = explicit (e.g., daily log returns computed at a specified close time; or 4H returns if Phase 1 is 4H-driven—choose and lock).
- Correlation estimator = explicit (Pearson on returns; minimum sample size; missing-data handling).
- Pairwise aggregation = explicit (simple mean of upper triangle vs exposure-weighted mean).
- Action selection = deterministic mapping, e.g.:
  - if `ρ_avg ∈ (0.55, 0.65]` → reduce gross by 35%  
  - if `ρ_avg > 0.65` → reduce gross by 50%  
  - ramp schedule fixed (e.g., linear over 3 business days), with state logged.

**Impact on system layers**
- Research Layer: reduces degrees of freedom in evaluating correlation controls.  
- Governance Layer: makes P3 reproducible and prevents discretionary risk shaping.  
- Portfolio Layer: deterministic, testable behavior under stress.

**Risk of change**  
Low–Medium: may increase trigger frequency (or decrease it) versus informal interpretations, but improves auditability.

**Recommended Phase**  
Phase 0 (before Phase 1 runtime behavior is evaluated). fileciteturn0file1 fileciteturn0file0

---

**Q-ID: A-03**

**Short restatement**  
Define the **full concurrent state machine** for P1/P3/P4, including ramp interruptions and recovery ordering (U1–U4 cases).

**Context from the system**  
The spec defines precedence (P1 highest) and some conflict rules (“higher priority wins,” “no multiplicative combination”), but the audit identifies several concurrent/recovery scenarios that remain undefined and can cause paper-vs-evaluation divergence under stress. fileciteturn0file0 fileciteturn0file4 fileciteturn0file3 fileciteturn0file1

**Analysis**  
This is a **real architectural gap**: the current rules are necessary but not sufficient to guarantee deterministic execution. In distributed-systems terms, the spec defines priority arbitration but not the **state transition semantics** when events interleave (trigger during ramp, clear while another remains active, etc.). These edge cases matter because stress regimes are exactly when you most need deterministic behavior.

Invariants interaction: The protocol heavily relies on “structural drawdown control” and phase-gate comparability. If concurrency is undefined, two compliant implementations can diverge materially on exposure and trade count during recovery windows, contaminating both risk outcomes and metric comparability. fileciteturn0file2 fileciteturn0file4

Attack surfaces:
- **Implementation drift**: developers choose plausible but different interpretations that change realized DD, turnover, and P&L.
- **Adversarial selection**: an operator can prefer the implementation that “looks better” after the fact by framing it as a legitimate interpretation.
- **Silent gating bias**: if stress-period behavior differs, K thresholds become non-comparable across runs. fileciteturn0file4

Governance implication: Without a closed transition table, you cannot certify that Phase 1 evaluation, Phase 1 paper trading, and Phase 2 overlay experiments are running under the same control-plane semantics.

**Possible Outcomes**  
A) False concern: contradicted by audit stress tests.  
B) Real risk but mitigated: partially (precedence exists), but concurrency remains open.  
C) **Real architectural gap**.  
D) Requires spec clarification: yes, but the missing artifact is a full transition system.

**Verdict: C — Real architectural gap (state machine incomplete).** fileciteturn0file4 fileciteturn0file3

**ADR Recommendation**

**Title**  
Regime-Control State Machine Specification for P1/P3/P4 Concurrency

**Problem**  
Priority ordering exists, but interleavings and recovery/ramp semantics are underspecified, enabling evaluation-vs-execution divergence precisely during stress periods.

**Proposed Change**  
Add a normative state machine with:
- State variables: `{p1_active, p3_active, p3_ramp_progress, p4_state}` plus timestamps.
- Event types: `{p1_trigger, p1_clear, p3_trigger, p3_clear, p4_update}`.
- Transition table for all known ambiguous cases (U1–U4 and ramp interruption cases), explicitly stating:
  - whether P3 ramps pause/queue during P1 suspension,
  - what the target is immediately after P1 clears if P3 remains active,
  - whether P4 updates apply “track-only” vs “apply-inside-reduction” while P1 is active,
  - logging requirements (include transition reason, invariant checks).

**Impact on system layers**
- Research Layer: stabilizes experimental comparability across stress regimes.  
- Governance Layer: prevents “interpretation drift” and strengthens auditability.  
- Portfolio Layer: deterministic runtime behavior and simpler test harness.

**Risk of change**  
Medium: may force uncomfortable clarity (some interpretations reduce performance), but it eliminates silent non-determinism.

**Recommended Phase**  
Phase 0 (required before Phase 1 evaluation is treated as certifiable evidence). fileciteturn0file1 fileciteturn0file4

---

**Q-ID: A-04**

**Short restatement**  
Prevent **P4 calibration/vintage contamination** from invalidating Phase 1 OOS regime-span evidence.

**Context from the system**  
Phase 1 exit requires “15 months OOS spanning ≥2 regimes,” where regimes are defined via P4 labeling. The spec states “regime label immutability” (no retroactive rewriting after recalibration), but audit artifacts flag a missing boundary between “P4 calibration” and “Phase 1 OOS evidence.” fileciteturn0file0 fileciteturn0file1 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This is a **real gap** because immutability alone does not guarantee non-contamination. If the P4 algorithm involves any fitted parameters (thresholds, normalizers, classifier weights), then using full-sample data (or any look-through into the OOS period) contaminates the label series used for regime-span certification.

Adversarially, the core issue is that regime labeling becomes a “hidden training channel” unless it obeys the same time-boundary discipline as the evaluation harness. For gate integrity, it must be possible to prove that every regime label attached to an OOS return was produced using only information available at that time *and* using parameter vintages locked before the OOS window begins. fileciteturn0file4 fileciteturn0file2

Attack surfaces:
- **Retrofit labeling**: adjust P4 parameterization after seeing OOS results, then claim immutability by only freezing the final labels.
- **Implicit leakage**: compute regime thresholds using rolling statistics whose initialization implicitly uses future data (e.g., z-score normalizers built from full history).
- **Regime-span inflation**: classify short “fragments” to satisfy “≥2 regimes,” unless fragment counting rules are locked. fileciteturn0file0 fileciteturn0file4

Governance implication: Phase transitions become contestable; worst case, the protocol could “pass” Phase 1 while the core certification evidence is non-auditable.

**Possible Outcomes**  
A) False concern: not supported (audit flags it).  
B) Real risk but mitigated: partially (immutability exists), but not sufficient.  
C) **Real architectural gap**.  
D) Requires spec clarification: yes, and the fix must be formalized.

**Verdict: C — Real architectural gap (vintage discipline missing).** fileciteturn0file1 fileciteturn0file4

**ADR Recommendation**

**Title**  
P4 Label Vintage Control Policy for Phase-Gate Evidence

**Problem**  
Regime labels are used as gate evidence, but the protocol lacks a formal rule preventing calibration overlap / vintage contamination between P4 training and Phase 1 OOS windows.

**Proposed Change**  
Add a “P4 Vintage Control” policy:
- For Phase 1 certification, lock a P4 parameter vintage **before** the first OOS bar in the certification window.
- Generate labels via walk-forward-only labeling (strictly past-only inputs) or via strictly rule-based parameters fixed ex ante.
- Store a “label vintage artifact” for each reported window: `{p4_version, param_hash, calibration_end_ts, label_generation_ts, dataset_hash}`.
- Disallow using a recalibrated P4 vintage to re-label already-evaluated OOS windows; if re-labeling is required (bug fix), invalidate prior certification artifacts and re-run evaluation.

**Impact on system layers**
- Research Layer: enables stable comparisons across recalibrations.  
- Governance Layer: makes “≥2 regimes” auditable and prevents hidden leakage.  
- Portfolio Layer: clarifies operational behavior when P4 is recalibrated (future-only effect).

**Risk of change**  
Medium: may reduce apparent regime diversity in early Phase 1 until enough time elapses, but this is a truthful representation.

**Recommended Phase**  
Phase 0 (policy must exist before Phase 0→1 certification and any Phase 1 OOS claims). fileciteturn0file2 fileciteturn0file3

## Governance & Protocol Integrity

**Q-ID: B-01**

**Short restatement**  
Select the **canonical Harvey–Liu deflation/haircut** variant and define **cross-namespace trial aggregation** (Main + AT + RDL submission-time entries).

**Context from the system**  
Multiplicity correction is explicitly frozen as mandatory (“Trial Registry + multiplicity correction”), and Phase 1 exit criteria require the haircut to be < 0.05 Sharpe units. Audit artifacts flag the computation as non-auditable because the formula variant and aggregation scope are missing. fileciteturn0file0 fileciteturn0file2 fileciteturn0file3 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This is a **real architectural and governance gap** because it creates a “forkable” approval system: two compliant teams can produce different deflated Sharpe and different pass/fail outcomes from the same raw returns and the same trial log.

Interaction with invariants: the invariant registry explicitly marks the haircut formula as `FORMULA_MISSING`, and drift tooling treats this as a P0 blocker because it is gate-affecting. The adversarial review further notes that without a locked variant, thresholds like “<0.05” and “>0.08” are not interpretable. fileciteturn0file2 fileciteturn0file3 fileciteturn0file4

Attack surfaces:
- **Variant shopping**: pick a lenient correction family (or a conservative one) after seeing results.
- **Trial undercounting**: reclassify modifications as non-counted actions (ties directly to B-05).
- **RDL inflation shock**: if RDL submissions are counted at submission time (as the spec indicates), an uncontrolled backlog can make any haircut enormous, potentially weaponizing the Trial Registry against progress or incentivizing off-registry testing (which the protocol forbids). fileciteturn0file0 fileciteturn0file4

Governance implications: multiplicity correction in research protocols is analogous to consensus safety: it must be deterministic, centrally specified, and testable with a reproducibility suite.

Evidence from literature (needed for canonicalization): the core “haircut Sharpe ratio” / multiple-testing adjustment framing is treated directly in entity["people","Campbell R. Harvey","finance professor"] and entity["people","Yan Liu","finance researcher"]’s *Backtesting* (SSRN version), and related multiple-testing hurdles are also discussed in broader multiple-testing frameworks by Harvey/Liu/Zhu. citeturn5search4turn2search2

**Possible Outcomes**  
A) False concern: no (gate-affecting and flagged missing).  
B) Real risk but mitigated: not currently (no canonical variant).  
C) **Real architectural gap**.  
D) Requires spec clarification: also true, but the missing computation is the core.

**Verdict: C — Real architectural gap (gate-affecting formula undefined).** fileciteturn0file2 fileciteturn0file4

**ADR Recommendation**

**Title**  
Normative Harvey–Liu Haircut Specification with Cross-Namespace Trial Aggregation

**Problem**  
A mandatory, gate-affecting deflation exists, but no canonical computation variant or trial aggregation scope is defined, enabling inconsistent approvals and audit failure.

**Proposed Change**  
1) **Pick one canonical computation** by reference implementation:
- Adopt the “haircut Sharpe ratio” procedure consistent with Harvey & Liu’s published methodology and code artifacts (e.g., a single chosen adjustment method or an explicitly defined composite rule). citeturn5search4turn1search5  
2) **Define trial aggregation scope**:
- Define an unambiguous trial-count `M_total` used for haircut:
  - include all Trial Registry entries that were *submitted before any evaluation-window data access* for the phase’s certification window, across namespaces: Main, AT, and `RDL-*`,
  - exclude entries marked “withdrawn before evaluation-window access” (but require an auditable withdrawal record).
3) **Ship a reproducibility suite**:
- Provide 3–5 worked examples: given `{raw_SR, T, M_total}`, output `{haircut_SR, haircut_units}` and confirm `haircut_units < 0.05` decision deterministically.
4) **Bind the haircut to reports**:
- Every phase table/report must include `{raw_SR, deflated_SR, M_total, method_id, code_hash}`.

**Impact on system layers**
- Research Layer: makes multiplicity correction reproducible and discourages off-registry testing.  
- Governance Layer: restores auditability to a frozen non-negotiable and phase-gate rules.  
- Portfolio Layer: indirect—prevents invalid promotion of strategies based on under-deflated performance.

**Risk of change**  
Medium–High: once canonicalized, some previously “acceptable” outcomes may fail the haircut threshold. This is intended: it reflects corrected governance, not regression.

**Recommended Phase**  
Phase 0 (required before Phase 1 exit criteria can be interpreted). fileciteturn0file0 fileciteturn0file5

---

**Q-ID: B-02**

**Short restatement**  
Unify the **RDL operational boundary** (“Phase 2+” vs “after Phase 2 exit”) and define a machine-checkable **dormancy attestation** for pre-Phase-2.

**Context from the system**  
The spec states RDL is “dormant until Phase 2” (scaffolding only pre-Phase-2) but also uses conflicting language about when it becomes operational and when it may influence routing/sizing; drift tooling marks this boundary inconsistency as a P0 failure. fileciteturn0file0 fileciteturn0file3 fileciteturn0file1 fileciteturn0file5

**Analysis**  
This is a **real governance risk** because a boundary ambiguity is effectively an authorization ambiguity: it creates room for “technically we were in Phase 2” arguments to justify early RDL influence.

Key missing assumption: the protocol needs a **single authoritative boundary per action type**, not a single global boundary. Specifically, these are different permissions:
1) generating/logging CandidateHypothesis objects (scaffolding),
2) submitting to Trial Registry,
3) reading evaluation-window data / running WFO evaluation,
4) influencing Portfolio Layer routing/sizing,
5) influencing RBE activation/stop checks.

The current texts conflate (2) and (4): they suggest Phase 2+ for “operational” behavior while separately restricting portfolio influence until Phase 2 exit. That may be a defensible design (e.g., allow registry submission + evaluation in Phase 2, but no portfolio influence until later), but it must be stated unambiguously and externally attestable. fileciteturn0file0 fileciteturn0file3

Attack surfaces:
- **Early evaluation access**: if “Phase 2+ means operational,” a team could start evaluating RDL-generated hypotheses immediately at Phase 2 start, potentially creating a “shadow optimization stream” unless rate-limited and strictly preregistered.
- **Soft routing leakage**: even without explicit portfolio routing, RDL suggestions could be used informally to select which skills to allocate, which becomes de facto influence. This must either be forbidden or treated as GE-3 trial-counted selection. fileciteturn0file4

Dormancy attestation matters because the spec asserts that “any Phase 0–1 RDL routing or OOS claim is automatically P0,” implying the audit pipeline can detect violations, but the mechanism is not specified as a queryable artifact. fileciteturn0file0 fileciteturn0file3

**Possible Outcomes**  
A) False concern: no (drift marks it as FAIL).  
B) Real risk but mitigated: partially (policy intent exists), but not enforceable.  
C) **Real architectural gap** (attestation + unambiguous boundary missing).  
D) Requires spec clarification: yes, but enforcement also needed.

**Verdict: C — Real architectural gap (authorization boundary not machine-checkable).** fileciteturn0file3

**ADR Recommendation**

**Title**  
RDL Boundary Matrix and Dormancy Attestation Contract

**Problem**  
Conflicting boundary language creates governance bypass risk; pre-Phase-2 dormancy is not externally attestable.

**Proposed Change**  
Define a **Boundary Matrix** in the spec with allowed phases per action type:
- RDL scaffolding/logging: Phase 0–1 allowed.
- Trial Registry submission: explicitly allowed/not allowed in Phase 0–1 (choose and lock).
- Evaluation harness reads / WFO runs on RDL hypotheses: Phase 2 start allowed only after preregistration.
- Portfolio routing/sizing influence: only after Phase 2 exit (if that is intended).
- RBE influence: never.

Add a **Dormancy Attestation Schema**:
- A runtime flag `RDL_MODE ∈ {scaffold_only, eval_enabled, portfolio_disabled, portfolio_enabled}` with phase constraints.
- Mandatory telemetry: any consumption of an `RDL-*` object by Portfolio Layer or RBE must emit a structured log event.
- Audit query: “show all pre-Phase-2 `RDL-*` read paths” must return empty for certification.

**Impact on system layers**
- Research Layer: enables safe Phase 2 activation without informal bypass.  
- Governance Layer: makes dormancy enforceable and audit-friendly.  
- Portfolio Layer: prevents accidental/implicit RDL influence pre-authorized phases.

**Risk of change**  
Low–Medium: introduces friction but directly reduces governance ambiguity.

**Recommended Phase**  
Phase 0 (before implementing RDL scaffolding that could later be misused). fileciteturn0file5 fileciteturn0file0

---

**Q-ID: B-03**

**Short restatement**  
Define what “charter-level review” means operationally for **RBE activation** (authority, artifacts, storage, criteria).

**Context from the system**  
RBE is “locked by default,” and activation requires “charter-level review” plus preregistration. Drift tooling flags that “charter-level review” is undefined, making RBE activation non-auditable. fileciteturn0file0 fileciteturn0file3 fileciteturn0file1

**Analysis**  
This concern is **valid** and crosses from “process” into “architecture,” because governance artifacts are part of the protocol’s control plane. If RBE step transitions are not tied to a reproducible approval artifact, then the system effectively becomes “self-authorizing”—the very governance fragility the audit warns about. fileciteturn0file4 fileciteturn0file3

Attack surfaces:
- **Solo authorization**: the same actor proposes, approves, and activates a step change (explicitly flagged as a behavioral integrity gap).
- **Artifact laundering**: “review happened” with no fixed template, no durable storage, no required sign-off list.
- **Selective memory**: post-hoc justification for a risk step that improved metrics in hindsight. fileciteturn0file4

Governance implications: RBE is a reversible risk-elevation mechanism; without a formal approval packet, it becomes indistinguishable from ad hoc risk-taking.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not currently.  
C) **Real architectural gap**.  
D) Requires spec clarification: yes, but more than wording—requires artifacts.

**Verdict: C — Real architectural gap (approval plane undefined).** fileciteturn0file3

**ADR Recommendation**

**Title**  
RBE Charter-Level Review Packet and Authority Map

**Problem**  
RBE activation requires “charter-level review,” but there is no operational definition, making step changes non-auditable and self-authorizing.

**Proposed Change**  
Define a mandatory “RBE Activation Packet” template and storage rule:
- Required fields: proposer, approver(s), step requested, justification, preregistration ID, metrics snapshot, expected impact, explicit rollback conditions, and effective date.
- Authority map: list roles permitted to approve (single vs multi-sig; minimum separation of duties).
- Storage: immutable location (append-only governance log) referenced by hash in the Trial Registry entry.

**Impact on system layers**
- Research Layer: reduces incentives to “optimize to pass” by changing risk budgets informally.  
- Governance Layer: makes RBE activation auditable and reproducible.  
- Portfolio Layer: provides deterministic authorization for step changes.

**Risk of change**  
Low: primarily formalization; prevents later disputes.

**Recommended Phase**  
Phase 0 (before any RBE-related implementation is activated or referenced). fileciteturn0file1 fileciteturn0file0

---

**Q-ID: B-04**

**Short restatement**  
Enforce the **RDL→RBE non-interaction** rule and define how RBE step transitions interact with **K1–K6 measurement windows**.

**Context from the system**  
The spec states RDL outputs must never feed into RBE activation/stop evaluation, and that RBE is governed by realized P&L and structural metrics. Drift and adversarial review note this separation is not consistently propagated, and window-continuity rules under RBE transitions are missing. fileciteturn0file0 fileciteturn0file3 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This is a **real gap** because RBE changes can alter volatility/allocations and therefore affect the statistics used for kill criteria decisions. Without explicit “window semantics,” you lose comparability: K thresholds computed across mixed-risk regimes are no longer meaningful as gate evidence.

Attack surfaces:
- **Gate shaping**: activate RBE to push rolling Sharpe above thresholds without resetting the window or annotating the regime change.
- **RDL-assisted RBE trigger**: use RDL-generated signals to improve the metrics that justify RBE entry—despite policy that forbids RDL→RBE coupling.
- **Rollback framing**: after a rollback event, selectively present stats that exclude the adverse period. fileciteturn0file4

Missing invariants:
- “RBE step change produces a new measurement epoch for any kill criterion that depends on allocation/vol dynamics,” or alternatively “RBE step changes are forbidden during K1 certification windows.” The protocol must pick one. fileciteturn0file4

Governance implication: This is a classic control-plane/data-plane coupling issue. If you allow the control plane (RBE) to change while measuring the data plane (K windows) without defining epoch semantics, you cannot later defend “kill-or-continue” decisions.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: partially (policy intent), but not enforceable.  
C) **Real architectural gap**.  
D) Requires spec clarification: also true, but enforcement is missing.

**Verdict: C — Real architectural gap (epoch semantics missing).** fileciteturn0file4 fileciteturn0file3

**ADR Recommendation**

**Title**  
RBE Epoch Semantics for Kill Criteria and Enforced RDL→RBE Segregation

**Problem**  
RBE transitions can distort kill-criteria measurement windows; RDL→RBE non-interaction is policy-stated but not enforced via auditable controls.

**Proposed Change**  
1) Enforce RDL→RBE segregation:
- RBE entry/rollback computations must be computed from a whitelist of metrics derived only from (a+b+c) streams and structural monitors; any reference to `RDL-*` objects triggers an audit failure condition.
2) Define window continuity rules:
- Introduce “evaluation epochs” keyed by `{phase_id, rbe_step, policy_hash}`.
- For each kill criterion, specify whether it:
  - resets on epoch change,
  - pauses during epoch change,
  - or is computed per-epoch and then combined by a deterministic rule.
3) Require reporting:
- All K1–K6 reports must include epoch identifiers so comparisons are not silently mixed.

**Impact on system layers**
- Research Layer: prevents indirect “optimize-to-trigger-RBE” behaviors.  
- Governance Layer: restores interpretability of kill criteria under policy transitions.  
- Portfolio Layer: ensures step changes are traceable and comparable.

**Risk of change**  
Medium: may slow risk-budget experimentation, but improves integrity of certification evidence.

**Recommended Phase**  
Phase 1 (rules must exist before any RBE step >0 is even considered). fileciteturn0file0 fileciteturn0file4

---

**Q-ID: B-05**

**Short restatement**  
Define a bright-line: when is “zero/near-zero persistent weighting” a GE-2 allocation tweak vs a GE-3 strategy modification requiring preregistration?

**Context from the system**  
GE-2 permits allocation-based diversification tuning without preregistration if signal logic is unchanged; GE-3 requires preregistration for signal/feature/exit changes. Audit adversarial review explicitly flags a loophole where “de facto skill removal” could be treated as GE-2 and not trial-counted. fileciteturn0file0 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This concern is **valid**: in protocols that rely on trial counting, “turning off” a skill or asset sleeve can be equivalent to a strategy change, especially if it is motivated by observed underperformance. Without a bright-line, the Trial Registry becomes undercounted and the haircut becomes artificially low.

Attack surface (core): **selection bias through silent pruning**. If underperforming components are effectively set to zero weight and not trial-counted, the system can “improve” without paying multiplicity costs, undermining NN-5’s intent. fileciteturn0file4 fileciteturn0file0

Missing assumption: GE-2 needs an explicit boundary for when allocation changes become structural deactivation (which should be GE-3), and a rule for whether the motivation (“based on observed performance”) changes the classification.

**Possible Outcomes**  
A) False concern: no (explicitly identified in adversarial review).  
B) Real risk mitigated: not currently.  
C) Real architectural gap: borderline.  
D) **Requires spec clarification** (bright-line + test cases).

**Verdict: D — Requires spec clarification (loophole closure).** fileciteturn0file4

**ADR Recommendation**

**Title**  
GE-2 vs GE-3 Bright-Line for Sustained Zero-Weight Skill Deactivation

**Problem**  
Persistent near-zero weighting can function as unregistered strategy modification, suppressing trial counts and weakening multiplicity correction.

**Proposed Change**  
Add a deterministic classification rule, e.g.:
- If a previously active skill’s target weight is set below ε (e.g., 1% of gross) for ≥ one full rebalance cycle (or ≥N consecutive rebalances), it is classified as **GE-3** and must be preregistered/trial-counted as a “skill deactivation modification.”
- GE-2 remains valid only for reweighting within non-zero bands that preserve the skill as active.
- Require “motivation tagging”: if a weight change is justified by observed performance metrics, it defaults to GE-3 unless it was preregistered as an allocation policy experiment.

**Impact on system layers**
- Research Layer: reduces post-hoc pruning degrees of freedom.  
- Governance Layer: prevents undercounting and preserves multiplicity integrity.  
- Portfolio Layer: clarifies allowed allocation tuning vs structural strategy change.

**Risk of change**  
Low: mostly reclassification; increases trial counts (intentionally) and therefore may increase haircuts.

**Recommended Phase**  
Phase 0 (before GE rules are used operationally). fileciteturn0file0 fileciteturn0file4

## Research Methodology Risks

**Q-ID: C-01**

**Short restatement**  
Fix the **Sharpe confidence interval methodology** at 15 months and clarify how K1 / Phase 1 decisions should interpret uncertainty.

**Context from the system**  
The spec mandates reporting a 68% CI but provides a CI magnitude claim that audit tooling flags as arithmetically incorrect and potentially inconsistent with the protocol’s own Sharpe definition and annualization conventions. The adversarial review shows that wrong CI arithmetic can make K1 statistically non-discriminative or misleading. fileciteturn0file0 fileciteturn0file3 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This is a **real risk** because CI methodology is part of the protocol’s epistemic safety: it constrains how confidently you can make kill-or-continue decisions. Two distinct failure modes exist:

1) **CI arithmetic wrong**: The drift report treats the current CI magnitude claim as incorrect. fileciteturn0file3  
2) **CI definition ambiguous**: The spec’s Sharpe definition and annualization rules must align with a CI formula that uses the correct effective sample size and (ideally) adjusts for serial correlation—especially because the protocol itself warns about timeframe aggregation and uses multi-hour bars. fileciteturn0file0

From literature: entity["people","Andrew W. Lo","finance professor"] derives the sampling distribution for Sharpe ratios and emphasizes that naïve annualization can be invalid under serial correlation; this is directly relevant to “what is T / n” in the CI formula and how to adjust it. citeturn1search0

Governance implication: K1 is defined as “kill review” at a point-estimate threshold. Even if thresholds are frozen, the protocol must clarify whether CI is purely informational or whether CI triggers additional governance actions (e.g., extend evaluation, do not escalate phases, require stronger evidence under multiplicity). Without this, CI becomes a cosmetic number that can be interpreted opportunistically. fileciteturn0file4 fileciteturn0file0

**Possible Outcomes**  
A) False concern: no (drift marks it FAIL).  
B) Real risk mitigated: not currently (estimator undefined).  
C) **Real architectural gap** (measurement protocol missing).  
D) Requires spec clarification: also true, but the missing estimator is central.

**Verdict: C — Real architectural gap (CI estimator + interpretation undefined).** fileciteturn0file3

**ADR Recommendation**

**Title**  
Canonical Sharpe CI Estimator and Governance Interpretation Standard

**Problem**  
The protocol mandates Sharpe CIs but provides incorrect/ambiguous CI arithmetic and lacks a canonical estimator aligned with the protocol’s return frequency and serial-correlation realities.

**Proposed Change**  
- Specify exactly:
  - the return series used for Sharpe estimation (bar-level returns with explicit annualization convention),
  - the CI estimator (e.g., asymptotic SE under specified assumptions, plus an autocorrelation-adjusted variant),
  - and the effective sample size definition.
- Add a governance interpretation rule:
  - CI is mandatory in reports; if CI overlaps the K1 boundary by more than a defined margin, require an explicit “uncertainty note” and prohibit phase escalation until additional evidence (time or regimes) accrues.

**Impact on system layers**
- Research Layer: produces consistent evidence of statistical uncertainty.  
- Governance Layer: prevents opportunistic interpretation of borderline results.  
- Portfolio Layer: indirect; reduces pressure to “optimize to threshold.”

**Risk of change**  
Medium: may reduce confidence in short-horizon results, which is the intended correction.

**Recommended Phase**  
Phase 0 (before Phase 1 OOS evidence is treated as decisive). fileciteturn0file0 citeturn1search0

---

**Q-ID: C-02**

**Short restatement**  
Lock the authoritative **N_eff estimator** for K3 and define what to do when near-threshold decisions are estimator-variance sensitive.

**Context from the system**  
K3 is a kill criterion tied to diversification collapse. The invariant registry and drift report indicate ambiguity: one section provides an equicorrelation-style formula, while other parts reference clustering language without locking the estimator choice; adversarial review shows estimator choice can flip decisions. fileciteturn0file2 fileciteturn0file3 fileciteturn0file4 fileciteturn0file0 fileciteturn0file5

**Analysis**  
Valid concern: K3 is governance-critical, and an ambiguous estimator is effectively an ambiguous kill switch.

Adversarial evidence: the same correlation structure can yield materially different N_eff depending on equicorrelation vs eigenvalue participation-style estimators; this means an implementation can “pass” or “fail” K3 without changing the underlying portfolio. fileciteturn0file4

Missing invariants:
- “K3 uses estimator X, computed on Y data, with window Z, and a minimum stability rule.” Without this, K3 is not enforceable.

Governance implication: For kill criteria, prefer an estimator that is (a) simple, (b) hard to game, and (c) stable under small perturbations. If you want richer estimators, they can exist as diagnostics but must not determine pass/fail without a tie-break protocol.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not currently.  
C) **Real architectural gap** (kill criterion not deterministic).  
D) Requires spec clarification: yes, but determinism is missing.

**Verdict: C — Real architectural gap (K3 not deterministically computable).** fileciteturn0file2 fileciteturn0file4

**ADR Recommendation**

**Title**  
Deterministic K3 N_eff Estimator with Boundary Adjudication Policy

**Problem**  
Multiple plausible N_eff estimators exist; without locking one and defining near-threshold handling, K3 decisions are non-reproducible.

**Proposed Change**  
- Set a single authoritative estimator for K3 (e.g., equicorrelation N_eff computed from mean pairwise correlations on a specified window), and explicitly define:
  - the correlation input population (skills? assets? both—choose one),
  - the return interval,
  - the window length and update cadence.
- Add boundary policy:
  - if within a small band around threshold (e.g., 1.9–2.1), require persistence for N consecutive periods and/or confirm via a secondary diagnostic estimator, but keep the primary decision rule deterministic.

**Impact on system layers**
- Research Layer: reduces “metric gaming” via estimator selection.  
- Governance Layer: makes K3 enforceable and auditable.  
- Portfolio Layer: clarifies when diversification controller actions are sufficient vs when a kill review is mandatory.

**Risk of change**  
Medium: locking an estimator can cause a different effective boundary than some stakeholders expect, but that is necessary for governance.

**Recommended Phase**  
Phase 0 (before Phase 1 monitoring begins determining kill outcomes). fileciteturn0file0 fileciteturn0file3

---

**Q-ID: C-03**

**Short restatement**  
Define the **K4 t-statistic formula** and pick an explicit error-control intent (bias toward avoiding false-kill vs avoiding missed-kill).

**Context from the system**  
K4 governs retirement of shorts after a minimum sample. Audit artifacts note formula ambiguity and calibration weakness; adversarial review infers an implied formula but flags high misclassification risk. fileciteturn0file2 fileciteturn0file4 fileciteturn0file0 fileciteturn0file5

**Analysis**  
Valid concern: K4 is a governance lever that can abruptly remove an entire strategic sleeve; if the statistic is ill-defined, the lever is arbitrary.

The adversarial review’s inference that K4 likely uses an IC-root-N family (because it matches stated numerical expectations) is a strong clue, but inference is not governance: the protocol must declare the formula, degrees-of-freedom handling, and autocorrelation treatment (if any). fileciteturn0file4

Missing assumptions:
- Are “trades” independent samples?
- Is the t-stat derived from mean per-trade returns, per-week returns, or IC measurements?
- What is the null hypothesis and what error profile is preferred?

Governance implication: Shorts are higher operational and tail-risk complexity. This suggests K4 should probably be biased toward **avoiding missed-kill** (don’t keep a dead short sleeve), but the spec must say so explicitly or it will be argued both ways post-hoc.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not currently (formula undefined).  
C) Real architectural gap: arguable.  
D) **Requires spec clarification** (formalize the statistic; keep thresholds frozen).

**Verdict: D — Requires spec clarification (K4 computation protocol).** fileciteturn0file4 fileciteturn0file2

**ADR Recommendation**

**Title**  
Normative K4 t-Statistic Definition and Calibration Rationale

**Problem**  
K4 is gate-affecting but its statistic definition is ambiguous, enabling inconsistent implementations and high misclassification risk.

**Proposed Change**  
Define K4 as one unambiguous computation, including:
- sample unit (trade-level vs period-level),
- formula (mean/SE or IC·√N),
- any autocorrelation/overlap correction,
- and explicit intent: prioritize false-kill avoidance or missed-kill avoidance, with a short calibration note.

**Impact on system layers**
- Research Layer: ensures short-sleeve evaluation is reproducible.  
- Governance Layer: makes K4 a legitimate kill rule instead of an ambiguous heuristic.  
- Portfolio Layer: supports deterministic retirement decisions.

**Risk of change**  
Low: mostly clarifying what is already implicitly assumed; may change computed t-stat values for existing results.

**Recommended Phase**  
Phase 1 (before Phase 3 shorts are ever considered). fileciteturn0file0 fileciteturn0file2

---

**Q-ID: C-04**

**Short restatement**  
Define purge/embargo rules and a timestamp normalization contract for **evaluation joins**, **event labels**, and **feature/version transitions** (especially RDL-3/RDL-4).

**Context from the system**  
Audit artifacts flag that leakage controls are under-specified once you introduce feature libraries and event labels, especially across phase boundaries and version transitions. fileciteturn0file5 fileciteturn0file1 fileciteturn0file4 fileciteturn0file0

**Analysis**  
This is a **real architecture risk** because timestamp mistakes are among the hardest-to-detect failure modes in trading research: you can pass all high-level governance rules and still leak information via sloppy joins.

Missing invariants:
- A strict contract for what a timestamp means (“bar close time” vs “data available time”).
- A strict rule for feature availability: a feature computed over a window must become available only after the last observation in its window.
- Purge/embargo specifics: how much of the past must be purged from training to avoid overlapping label horizons or feature lookbacks bleeding into test segments.

Relevant literature: “purging” and “embargo” are named techniques in entity["book","Advances in Financial Machine Learning","lopez de prado 2018"] for preventing leakage when labels overlap; even if you run walk-forward evaluation, the moment you create event-driven labels with horizons you need an explicit non-overlap policy. citeturn5search49turn0search0

Attack surfaces:
- **Event-label leakage**: tagging an event using a timestamp that reflects confirmation after the fact, but joining it as if known earlier.
- **Feature-version leakage**: switching feature definitions mid-window without resetting training baselines or tracking feature vintages.
- **Clock skew/timezone mistakes**: mixing exchange timestamps, UTC offsets, and bar-close conventions. fileciteturn0file4

Governance implication: without this, RDL-3/RDL-4 integration undermines NN-3 (“no OOS label without harness”) because the harness itself can be fed contaminated inputs.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not currently (no standards).  
C) **Real architectural gap**.  
D) Requires spec clarification: the gap is the missing appendix.

**Verdict: C — Real architectural gap (leakage contract missing).** fileciteturn0file5 citeturn5search49

**ADR Recommendation**

**Title**  
Leakage-Control Appendix: Timestamp Contract plus Purge/Embargo Equations

**Problem**  
RDL-3/RDL-4 introduce joins and horizon-based labels that create leakage risks unless purge/embargo and timestamp semantics are explicitly standardized.

**Proposed Change**  
Add a “Leakage Control Appendix” specifying:
- Timestamp fields per dataset/object: `{ts_event, ts_observed, ts_available}` with a single time basis (UTC) and explicit bar-close semantics.
- Embargo function `E(h)` defined as a deterministic function of label horizon `h` and feature lookback.
- Purging rule for training samples whose label/feature windows overlap the test window.
- A “join whitelist”: any join must use `ts_available ≤ decision_ts`; joins violating this are rejected by the harness.

**Impact on system layers**
- Research Layer: prevents hidden lookahead in feature/event pipelines.  
- Governance Layer: strengthens NN-3 enforceability by making leakage checks testable.  
- Portfolio Layer: reduces risk of deploying strategies validated on leaked data.

**Risk of change**  
Medium: may reduce measured performance (by removing leaked edges) and may require refactoring data pipelines—this is desired.

**Recommended Phase**  
Phase 0 (before RDL scaffolding is populated with objects that later become hard to certify). fileciteturn0file0 fileciteturn0file1

## RDL Activation Risks

**Q-ID: D-01**

**Short restatement**  
Define a deterministic Phase 2 activation policy for **promoting scaffolded RDL hypotheses** (queueing, batch limits, and multiplicity shock controls).

**Context from the system**  
RDL is “scaffolding only” before Phase 2, then becomes a source of preregistered hypotheses; simultaneously, trial counting for RDL is specified as “count at submission, not promotion,” which can create a large step-function in multiplicity once Phase 2 starts unless controlled. fileciteturn0file0 fileciteturn0file1 fileciteturn0file4 fileciteturn0file5

**Analysis**  
The risk is **real**, but the protocol’s existing design intent partially anticipates it by (a) requiring preregistration, (b) counting RDL trials at submission time (which discourages mass submission), and (c) keeping RDL dormant before Phase 2. The missing piece is **operational policy**: what happens to the inevitable backlog of “CandidateHypothesis objects” when Phase 2 begins?

Attack surfaces:
- **Batch promotion gaming**: promote a large set, then narratively focus on the winners while the multiplicity penalty is either ignored or inconsistently applied.
- **Off-registry pre-screening temptation**: if batch submission is too punishing, an operator may be incentivized to screen hypotheses informally before registry submission, which conflicts with governance intent. fileciteturn0file4

Missing invariants: rate limits and queues are governance controls, not convenience. Without them, Phase 2 becomes a multiplicity discontinuity event.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: partially by submission-time counting, but not operationally.  
C) Real architectural gap: borderline.  
D) **Requires spec clarification** (activation policy).

**Verdict: D — Requires spec clarification (queue + rate limiting).** fileciteturn0file5

**ADR Recommendation**

**Title**  
Phase 2 RDL Promotion Queue and Batch Limit Policy

**Problem**  
Phase 2 activation can create a multiplicity shock and unstable gating interpretation unless promotion/submission is rate-limited and auditable.

**Proposed Change**  
- Define a promotion queue with:
  - maximum `RDL-*` submissions per calendar month/quarter,
  - a deterministic ordering rule (FIFO by creation timestamp unless explicitly overridden by a preregistered prioritization policy),
  - and a “shock control” rule: if `M_total` increases by >X within Y days, freeze further promotions until haircut impact is recomputed and logged.
- Require that any backlog-clearing event is a governance action with an audit record.

**Impact on system layers**
- Research Layer: stabilizes hypothesis throughput and discourages off-registry screening.  
- Governance Layer: prevents multiplicity discontinuities from being used opportunistically.  
- Portfolio Layer: indirect; ensures Phase 2 research does not distort future gate metrics.

**Risk of change**  
Medium: slows RDL throughput, but preserves integrity of multiplicity correction.

**Recommended Phase**  
Phase 1 (policy must exist before Phase 2 begins). fileciteturn0file0 fileciteturn0file4

---

**Q-ID: D-02**

**Short restatement**  
Prevent RDL-2 from producing semantically unstable **RegimeTag** outputs across P4 finalization/version changes.

**Context from the system**  
RDL-2 is a Market State Labeler intended to produce regime tags; it depends on a stable regime definition, but P4 is currently undefined and will necessarily evolve once specified. The question pool asks for a compatibility/versioning contract linking P4 versions to RDL-2 outputs. fileciteturn0file5 fileciteturn0file1 fileciteturn0file0

**Analysis**  
This is a **real gap** because regime tags are only meaningful relative to a regime ontology. If P4 (or the normative regime taxonomy) changes, then old RegimeTag datasets become incomparable unless they carry explicit version provenance and a migration rule.

Attack surfaces:
- **Semantic drift**: downstream studies unknowingly mix RegimeTag v1 and v2, producing “difference-in-regime” results that are artifacts of changed labels.
- **Backfilled relabeling**: re-run labeler with v2 and overwrite prior tags, making earlier research irreproducible—even if Phase 1 label immutability is respected for OOS windows, RDL research corpora can still drift. fileciteturn0file4

Missing invariants: every RegimeTag must be stamped with `{p4_version, labeler_version, dataset_hash}`; and there must be an explicit rule for whether migration is allowed (and if so, how old studies are invalidated or rebaselined).

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not currently.  
C) **Real architectural gap**.  
D) Requires spec clarification: yes, and it must be formal.

**Verdict: C — Real architectural gap (version contract missing).** fileciteturn0file5

**ADR Recommendation**

**Title**  
P4-to-RDL-2 Compatibility Matrix and RegimeTag Migration Protocol

**Problem**  
RDL-2 outputs depend on regime semantics that will change as P4 is defined/versioned; without a compatibility contract, RDL research becomes non-reproducible.

**Proposed Change**  
- Define a compatibility matrix:
  - For each `p4_version`, specify which `rdl2_labeler_version` is valid.
- Require per-object provenance:
  - `RegimeTag` includes `{p4_version, p4_param_hash, rdl2_version, ts_generated, dataset_hash}`.
- Define migration rules:
  - migration = create new dataset version; never overwrite prior tags;
  - any report must state which versions were used.

**Impact on system layers**
- Research Layer: preserves comparability across labeler iterations.  
- Governance Layer: prevents “moving target” regime narratives.  
- Portfolio Layer: indirect; reduces risk that research artifacts later contaminate live routing.

**Risk of change**  
Low–Medium: adds metadata overhead but prevents larger epistemic failures.

**Recommended Phase**  
Phase 0–Phase 1 (must exist before Phase 2 RDL activation). fileciteturn0file0 fileciteturn0file1

---

**Q-ID: D-03**

**Short restatement**  
Implement hard isolation controls proving RDL outputs cannot influence **routing/sizing** or **RBE inputs** before authorized phases.

**Context from the system**  
The spec states strong policy constraints (“no RDL influence pre-Phase-2; no RBE interaction ever”), and drift notes that policy-only separation is vulnerable without technical enforcement and audit queries. fileciteturn0file0 fileciteturn0file3 fileciteturn0file2 fileciteturn0file5

**Analysis**  
This is a **real gap** in enforcement architecture. Policy statements reduce intent ambiguity, but they do not prevent accidental coupling (a developer wires an RDL feature into portfolio selection) or intentional shadow influence (“we didn’t route it automatically, but we used it to decide what to allocate”).

Attack surfaces:
- **Data-plane seepage**: shared feature store tables where RDL-derived features are indistinguishable from allowed features.
- **Control-plane seepage**: RDL outputs inform manual parameter changes framed as “allocation tuning” under GE-2.
- **RBE coupling**: RDL-derived signals improve near-term metrics and thereby influence the decision to activate or avoid rolling back RBE. fileciteturn0file4

Missing invariants: need machine-checkable separation plus audit queries for certification (“show me all RDL object reads by portfolio/RBE code paths”).

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: partially by policy and audit pipeline intent, but not proven.  
C) **Real architectural gap**.  
D) Requires spec clarification: also true; enforcement is the core.

**Verdict: C — Real architectural gap (isolation not technically specified).** fileciteturn0file3 fileciteturn0file5

**ADR Recommendation**

**Title**  
RDL Isolation Architecture with Mandatory Telemetry and Compliance Checks

**Problem**  
RDL is policy-gated, but without hard isolation controls it can influence routing/sizing or RBE indirectly or accidentally, undermining phase gating integrity.

**Proposed Change**  
- Separate namespaces and access controls:
  - RDL objects stored in a logically separate store/namespace with explicit “no-read” policies for Portfolio Layer and RBE code paths pre-authorized phases.
- Add “consumption telemetry”:
  - any attempt to load `RDL-*` objects from Portfolio/RBE code paths emits a structured log and fails CI/tests in restricted phases.
- Add certification audits:
  - formal audit queries used in Phase certification to prove absence of RDL influence.

**Impact on system layers**
- Research Layer: still functional; prevents accidental promotion to influence.  
- Governance Layer: makes dormancy and segregation enforceable (not aspirational).  
- Portfolio Layer: strong guardrails; fewer accidental couplings.

**Risk of change**  
Medium: requires engineering discipline and may slow integration, but prevents deep governance violations.

**Recommended Phase**  
Phase 0 (build guardrails before RDL scaffolding grows). fileciteturn0file0 fileciteturn0file3

## Spec Ambiguities

**Q-ID: E-01**

**Short restatement**  
Make net Sharpe stream composition canonical everywhere (**a+b+c** vs **a+c**) and enforce conformance in reports/tables.

**Context from the system**  
NN-2 defines four-stream P&L and states that net Sharpe uses (a)+(b)+(c) only, excluding treasury (d). Drift tooling flags wording drift where some phase tables appear to exclude stream (b), which can silently omit short-side performance. fileciteturn0file0 fileciteturn0file3 fileciteturn0file2 fileciteturn0file5

**Analysis**  
This is a **spec ambiguity with potentially severe reporting consequences**. Even if the implementation is correct, inconsistent documentation is a known failure mode in governance-heavy systems: teams implement what they read in tables, not what is stated in a “non-negotiables” section.

Attack surface: “metric laundering” by omission—if short P&L is negative, excluding (b) inflates apparent net Sharpe; if short P&L is positive, excluding it hides the contribution and can distort phase-go decisions. Either way, this creates an integrity gap. fileciteturn0file3

**Possible Outcomes**  
A) False concern: no (drift confirms).  
B) Real risk mitigated: partially (NN-2 is explicit), but drift indicates active inconsistency.  
C) Real architectural gap: not exactly; it’s a definition drift.  
D) **Requires spec clarification**.

**Verdict: D — Requires spec clarification (definition conformance).** fileciteturn0file3

**ADR Recommendation**

**Title**  
Net Sharpe Definition Conformance Lint Across Spec and Reports

**Problem**  
Wording drift can lead to inconsistent implementations and silent exclusion of short P&L from primary metrics.

**Proposed Change**  
- Declare NN-2’s net Sharpe definition as the single canonical reference and remove/patch any conflicting table wording.
- Add a conformance checklist (lint):
  - every performance report must explicitly show (a), (b), (c), (d), and compute net Sharpe from (a+b+c) only.
- Require code/report schema validation: “net_sharpe_inputs = {a,b,c} exactly.”

**Impact on system layers**
- Research Layer: improves repeatability of reported metrics.  
- Governance Layer: prevents silent metric scope drift.  
- Portfolio Layer: indirect (prevents misinformed decisions based on wrong metrics).

**Risk of change**  
Low: mostly documentation and reporting schema enforcement.

**Recommended Phase**  
Phase 0 (before Phase 1 reporting begins). fileciteturn0file0 fileciteturn0file3

---

**Q-ID: E-02**

**Short restatement**  
Resolve K3 timing ambiguity: “2 consecutive months” vs “≥3 months monitoring precondition,” and define conflict-resolution precedence among docs.

**Context from the system**  
Drift tooling flags inconsistency across documents for K3 temporal trigger conditions; invariant registry notes ambiguity and missing determinism. fileciteturn0file3 fileciteturn0file2 fileciteturn0file5

**Analysis**  
This ambiguity is **governance-relevant**: timing conditions directly alter kill outcomes. The core failure is that K3 is a kill criterion; any ambiguity becomes an opportunity for post-hoc arbitration.

Attack surface: cherry-pick the stricter or looser interpretation depending on whether you prefer to trigger or avoid the kill review. This is especially dangerous when N_eff is itself noisy and estimator-dependent (C-02). fileciteturn0file4

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not if docs disagree.  
C) Real architectural gap: secondary, but effects are real.  
D) **Requires spec clarification**.

**Verdict: D — Requires spec clarification (canonical grammar).** fileciteturn0file3

**ADR Recommendation**

**Title**  
Canonical K3 Temporal Trigger Grammar and Document Precedence Rule

**Problem**  
K3 timing conflicts across docs produce divergent kill outcomes and undermine auditability.

**Proposed Change**  
- Declare one canonical K3 temporal rule in the Protocol Spec’s kill criteria reference and explicitly supersede other phrasings.
- Add a doc precedence rule: “Protocol Spec > Charter tables > other artifacts,” or the intended hierarchy.
- Require K3 evaluation logs to include `{monitoring_start_ts, consecutive_periods_counted, rule_version}`.

**Impact on system layers**
- Research Layer: avoids inconsistent “kill/no-kill” based on timing semantics.  
- Governance Layer: prevents post-hoc arbitration across documents.  
- Portfolio Layer: clarifies when diversification collapse actions must occur.

**Risk of change**  
Low: formalizes what should already be consistent.

**Recommended Phase**  
Phase 0. fileciteturn0file2 fileciteturn0file3

---

**Q-ID: E-03**

**Short restatement**  
Define the phase topology for **Phase 5 (Treasury activation)** when Phase 4 is optional/bypassed.

**Context from the system**  
The spec simultaneously describes treasury as last in sequential rollout and provides a Phase 5 gate that references Phase 1 exit + live capital criteria, while drift tooling flags missing explicit 4→5 topology semantics. fileciteturn0file0 fileciteturn0file3 fileciteturn0file5

**Analysis**  
This is a **real ambiguity** because phase topology is governance: under what conditions can the protocol allocate idle capital to treasury instruments, and does that require completing intermediate phases, bypassing them, or treating Phase 5 as orthogonal?

Attack surface: less about adversarial cheating and more about “policy drift by convenience,” where treasury gets activated early because it improves blended returns, and governance later rationalizes it. This is explicitly called out as a key risk (treasury masking weak alpha). fileciteturn0file0

Missing assumption: whether Phase 5 is (a) strictly sequential after Phase 4 (or a formal bypass decision), or (b) a parallel “treasury sleeve” activation contingent only on Phase 1 exit + live readiness.

**Possible Outcomes**  
A) False concern: no (drift flags).  
B) Real risk mitigated: not if topology is unclear.  
C) Real architectural gap: it’s mainly a topology definition.  
D) **Requires spec clarification**.

**Verdict: D — Requires spec clarification (phase graph).** fileciteturn0file3

**ADR Recommendation**

**Title**  
Explicit Phase 5 Topology Rule Under Optional Phase 4 Bypass

**Problem**  
Inconsistent phase topology can enable early treasury activation, undermining sequential governance and masking alpha issues.

**Proposed Change**  
- Publish a phase dependency graph textually:
  - define whether Phase 5 depends on (Phase 4 exit) OR (Phase 4 bypass decision recorded) OR (Phase 1 exit + live criteria only).
- Require a “Phase 4 bypass decision artifact” if Phase 4 is skipped; Phase 5 activation must reference that artifact.
- Reaffirm metric integrity: treasury P&L is never included in net Sharpe.

**Impact on system layers**
- Research Layer: maintains clarity on what performance is being certified.  
- Governance Layer: prevents premature treasury activation and preserves roll-out discipline.  
- Portfolio Layer: clarifies when treasury sleeve can be operational.

**Risk of change**  
Low–Medium: may delay treasury activation; increases clarity and prevents masking.

**Recommended Phase**  
Phase 0. fileciteturn0file0 fileciteturn0file3

---

**Q-ID: F-01**

**Short restatement**  
Add an IC_long “suspect threshold” policy mirroring IC_short governance and standardize FLAM arithmetic/correlation assumptions.

**Context from the system**  
The spec includes an IC_short suspect threshold (“if IC_short > 0.04, treat as suspect and apply a haircut”) and audit artifacts flag that IC_long lacks a symmetric policy. Separately, both drift and adversarial review highlight inconsistencies in FLAM-related arithmetic and assumptions, which affects feasibility narratives and phase prioritization. fileciteturn0file0 fileciteturn0file2 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This is not merely “theory hygiene.” In a governance protocol, feasibility assumptions drive which risks you tolerate and which modules you prioritize. If long-edge assumptions are allowed to be optimistic without a “suspect” policy, the protocol can drift into narrative-driven decision-making (“long IC is strong, so we’re fine”) while short IC is held to a stricter skepticism standard.

From literature: the fundamental law framing (IR ≈ IC·√Breadth) is widely used, but it is highly sensitive to how breadth and independence are defined—exactly the failure noted in the audit artifacts. citeturn5search51

Attack surfaces:
- **Optimism bias**: long IC interpreted as “strong edge” even when it may reflect leakage or overfitting.
- **Inconsistent skepticism**: shorts get penalized for “too good,” longs do not.
- **Planning distortion**: inconsistent breadth arithmetic changes expectations for net Sharpe and can influence phase sequencing arguments. fileciteturn0file4

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: not currently.  
C) Real architectural gap: moderate—affects governance narratives more than hard gates.  
D) **Requires spec clarification** (governance symmetry + standardized assumptions).

**Verdict: D — Requires spec clarification (symmetry and corrected assumptions).** fileciteturn0file4

**ADR Recommendation**

**Title**  
Symmetric IC Governance and Standardized FLAM Assumption Note

**Problem**  
Asymmetric skepticism (IC_short suspect policy exists; IC_long does not) and inconsistent FLAM arithmetic enable distorted feasibility narratives and reduce audit integrity.

**Proposed Change**  
- Add IC_long suspect threshold policy comparable to IC_short:
  - if IC_long exceeds a defined bound, require (a) replication across subperiods and (b) a reporting haircut/flag.
- Publish a corrected FLAM assumption note:
  - lock breadth arithmetic, long/short correlation assumptions, and the specific N_eff interpretation used for feasibility planning.

**Impact on system layers**
- Research Layer: reduces leakage/overfit optimism risk.  
- Governance Layer: prevents narrative drift and improves symmetry of scrutiny.  
- Portfolio Layer: indirect; affects how edges are trusted and promoted.

**Risk of change**  
Low–Medium: may reduce stated expected performance; improves realism.

**Recommended Phase**  
Phase 0. fileciteturn0file0 fileciteturn0file4

---

**Q-ID: F-02**

**Short restatement**  
Decide whether Phase 1 needs a **K6-like SimBroker drift hold/kill** rule, and specify thresholds/actions.

**Context from the system**  
Phase 1 exit criteria already require “SimBroker cost accuracy confirmed within 15%,” while K6 is defined for Phase 3–4 as “short-cost model diverges >20% from paper-fill costs for 2 consecutive months.” Audit architecture nevertheless flags Phase 1 drift handling as lacking a kill/hold action despite certification dependence. fileciteturn0file0 fileciteturn0file1 fileciteturn0file5

**Analysis**  
The concern is **real but partially mitigated** by existing design: Phase 1 cannot exit (and therefore cannot certify into Phase 2) if SimBroker cost accuracy is not within 15%. That is an important safeguard. fileciteturn0file0

What remains unresolved is the **mid-window semantics**: if drift is discovered during Phase 1 OOS accumulation, what happens to (i) already logged “OOS” results, (ii) the ongoing window, and (iii) governance decisions made on those results? If the answer is “we just fix the broker and keep going,” you risk mixing cost regimes in the same evidence window, which repeats the epoch problem seen in B-04. fileciteturn0file4

Attack surface: not direct adversarial in most cases; the larger risk is **contaminated certification evidence** that is later defended because “exit criterion eventually passed,” while earlier parts of the OOS window were evaluated under a wrong cost model.

**Possible Outcomes**  
A) False concern: not entirely (gap exists).  
B) **Real risk but mitigated by existing design** (exit gate already requires cost accuracy).  
C) Real architectural gap: remaining gap is mid-window semantics.  
D) Requires spec clarification: yes.

**Verdict: D — Requires spec clarification (mid-window drift semantics), even though gate mitigation exists.** fileciteturn0file0 fileciteturn0file1

**ADR Recommendation**

**Title**  
Phase 1 SimBroker Drift Epoch Semantics and Hold Procedure

**Problem**  
Phase 1 is protected by an exit criterion, but lacks explicit rules for handling drift discovery during the OOS accumulation window, risking mixed-regime evidence.

**Proposed Change**  
- Define a Phase 1 “drift hold” procedure:
  - if cost accuracy exceeds a threshold for N consecutive checks, freeze certification counting and mark the window segment as “non-certifiable pending recalibration.”
- Define re-evaluation requirement:
  - after recalibration, re-run evaluation for affected intervals or reset the certification window boundary.
- Require drift reporting:
  - include drift metrics and cost-model version hashes in all Phase 1 performance artifacts.

**Impact on system layers**
- Research Layer: prevents mixed cost-regime evaluation artifacts.  
- Governance Layer: clarifies whether Phase 1 evidence remains valid under drift events.  
- Portfolio Layer: ensures execution realism remains consistent with reported performance.

**Risk of change**  
Medium: may lengthen time to certification; improves evidence integrity.

**Recommended Phase**  
Phase 1 (policy must exist before Phase 1 results are used for go/no-go). fileciteturn0file0

---

**Q-ID: F-03**

**Short restatement**  
Define the canonical matched-pair construction protocol for **Phase 2 overlay evaluation**.

**Context from the system**  
The spec states that extension deltas must be computed on matched observations against a pre-defined baseline (no comparing different windows), and Phase 2 requires paper comparison with “comparable trade pairs.” Audit artifacts flag that pairing ambiguity can change measured overlay delta and decisions. fileciteturn0file0 fileciteturn0file4 fileciteturn0file5

**Analysis**  
This is a **real spec ambiguity** with measurement consequences. Without a canonical pairing rule, Phase 2 can “win” by construction:
- define pairs only when both baseline and overlay trade (excludes the overlay’s avoided losses),
- or define pairs by entry signal only (includes avoided trades but forces imputation for overlay non-trades),
- or exclude pairs with early exits (biases results).

Each approach answers a different causal question. The protocol must state which causal question Phase 2 is designed to answer (e.g., “does overlay improve outcomes holding entries constant?” vs “does overlay improve portfolio outcomes including trade suppression?”). fileciteturn0file4

Governance implication: Phase 2 is a phase gate; “overlay worked” must mean a single thing, not a choice among metrics.

**Possible Outcomes**  
A) False concern: no.  
B) Real risk mitigated: partially (matched principle stated), but not method.  
C) Real architectural gap: moderate.  
D) **Requires spec clarification** (canonical pairing).

**Verdict: D — Requires spec clarification (reproducible matched-pair method).** fileciteturn0file5

**ADR Recommendation**

**Title**  
Phase 2 Matched-Pair Evaluation Protocol for Overlay Delta

**Problem**  
Pairing ambiguity enables inconsistent overlay delta measurements, undermining phase-gate decisions.

**Proposed Change**  
- Define the unit of pairing (entry-signal event at time t for asset i).
- Define inclusion rules:
  - how to treat overlay-suppressed trades,
  - how to handle differences in exit timing,
  - how to treat missing pairs.
- Define the primary delta metric and at least one robustness metric (both preregistered):
  - e.g., paired trade return delta + portfolio-level matched-period return delta.

**Impact on system layers**
- Research Layer: prevents measurement gaming and clarifies causal question.  
- Governance Layer: makes Phase 2 gate evidence reproducible.  
- Portfolio Layer: improves confidence that overlay changes are actually beneficial.

**Risk of change**  
Medium: may reduce reported overlay benefit once ambiguity is removed, but increases validity.

**Recommended Phase**  
Phase 1 (must exist before Phase 2 overlay evaluation begins). fileciteturn0file0 fileciteturn0file4

## Architectural Summary

Confirmed architectural risks
- **P4 is gate-critical but algorithmically undefined**, blocking reproducible Phase gates and undermining regime-span evidence integrity. fileciteturn0file3 fileciteturn0file1
- **Concurrency semantics for P1/P3/P4 are not fully specified**, enabling evaluation-vs-execution divergence in stress periods. fileciteturn0file4
- **Multiplicity correction (Harvey–Liu haircut) is mandatory yet non-computable** as a canonical rule, making Phase 1 exit criteria non-auditable. fileciteturn0file2 fileciteturn0file3
- **RDL boundary and isolation are not machine-attested**, creating governance bypass risk via ambiguity and informal influence channels. fileciteturn0file3

Spec clarifications required
- Deterministic P3 population/frequency/aggregation and 35–50% action selection mapping. fileciteturn0file5
- Canonical Sharpe CI estimator aligned with the protocol’s return conventions and a governance rule for interpreting uncertainty (supported by Sharpe sampling distribution literature). citeturn1search0 fileciteturn0file3
- Locked K3 N_eff estimator and timing grammar to make K3 enforceable and auditable. fileciteturn0file3
- Explicit Phase 5 topology under Phase 4 optionality/bypass. fileciteturn0file3
- Canonical Phase 2 matched-pair rules. fileciteturn0file4

Design improvements
- Treat governance rules as control-plane artifacts: add **versioned annexes** (P4, leakage-control, multiplicity correction) with hashable, testable reference implementations. fileciteturn0file1 fileciteturn0file0
- Introduce **epoch semantics** for any policy/risk-budget change that affects kill-criteria measurement windows (RBE step changes, SimBroker recalibration). fileciteturn0file4
- Enforce RDL dormancy and RDL→RBE segregation with **auditable telemetry and negative proofs** (certification queries that must return empty). fileciteturn0file3

Questions that remain unresolved
- The exact canonical choice of a **single** Harvey–Liu haircut variant (or a formally defined composite) and its deterministic mapping from trial counts to Sharpe haircut units, including correlation/dependence handling. citeturn5search4turn1search5
- The final normative decision on whether Phase 5 is strictly sequential after Phase 4 (or formal bypass) vs an orthogonal sleeve once Phase 1 exit + live criteria are met; current artifacts support both readings. fileciteturn0file0 fileciteturn0file3