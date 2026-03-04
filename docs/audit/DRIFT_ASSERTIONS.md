# Entropy Protocol — Drift Assertions

**Classification:** Confidential — Internal Audit Document  
**Filename:** `docs/audit/DRIFT_ASSERTIONS.md`  
**Audit Cycle:** Cycle 1 — Phase 0 (Pre-Development)  
**Pipeline Step:** Step 4 — Protocol Drift Guard  
**Pipeline Version:** v1.0  
**Date:** 2026-03-04  
**Status:** Draft — Awaiting Spec Owner Acceptance  
**Prior drift artifacts:** None (Cycle 1 first formal run)

---

| INV-ID | Invariant short name | Verdict | Evidence pointer (doc + section) | Prior cycle verdict | Regression? |
|---|---|---|---|---|---|
| INV-A-01 | NN-1 Gross <=1.0 | PASS | PROTOCOL_SPEC B NN-1; CHARTER B NN-1; GLOSSARY P&L attribution section | N/A | No |
| INV-A-02 | NN-2 Four-stream separation | PASS | PROTOCOL_SPEC B NN-2; CHARTER B NN-2; GLOSSARY P&L Attribution | N/A | No |
| INV-A-03 | NN-3 Evaluation-engine-first | PASS | PROTOCOL_SPEC B NN-3; CHARTER B NN-3; EVOLUTION Section 1 | N/A | No |
| INV-A-04 | NN-4 Sequential rollout | AMBIGUOUS | PROTOCOL_SPEC B NN-4 vs Phase 5 prerequisites (F section); CHARTER NN-4 and Phase ordering | N/A | No |
| INV-A-05 | NN-5 Registry + HL correction | AMBIGUOUS | PROTOCOL_SPEC B NN-5 + C/F/J; CHARTER NN-5; GLOSSARY Deflated Sharpe (formula absent) | N/A | No |
| INV-A-06 | NN-6 Asset-specific stops | PASS | PROTOCOL_SPEC B NN-6; CHARTER NN-6 + Correction 3; GLOSSARY Cost Model | N/A | No |
| INV-B-K1 | K1 Sharpe kill threshold | AMBIGUOUS | PROTOCOL_SPEC F/J K1; CHARTER Phase 1 K1; GLOSSARY Kill Criteria + Net Sharpe CI inconsistency | N/A | No |
| INV-B-K2 | K2 Cost burden kill | PASS | PROTOCOL_SPEC F/J K2; CHARTER Phase 1 K2; GLOSSARY Kill Criteria K2 | N/A | No |
| INV-B-K3 | K3 N_eff kill condition | FAIL | CHARTER Phase 1 metrics table ("2 consecutive months") vs CHARTER/PROTOCOL_SPEC/GLOSSARY kill text ("after 3+ months" only) | N/A | No |
| INV-B-K4 | K4 Short t-stat kill | AMBIGUOUS | PROTOCOL_SPEC F/J K4; CHARTER Correction 2 + K4; formula for t-stat not defined in any doc | N/A | No |
| INV-B-K5 | K5 Treasury dominance | AMBIGUOUS | PROTOCOL_SPEC F/J K5; CHARTER K5; GLOSSARY K5 (window protocol not formalized) | N/A | No |
| INV-B-K6 | K6 SimBroker short-cost kill | PASS | PROTOCOL_SPEC F/J K6; CHARTER K6; GLOSSARY K6 | N/A | No |
| INV-B-P2K1 | P2K1 Overlay turnover kill | PASS | PROTOCOL_SPEC F/J P2K1; CHARTER Phase 2; GLOSSARY P2K1 | N/A | No |
| INV-B-P2K2 | P2K2 False-trigger reduction kill | PASS | PROTOCOL_SPEC F/J P2K2; CHARTER Phase 2; GLOSSARY P2K2 | N/A | No |
| INV-B-P4K1 | P4K1 Funding-drag kill | PASS | PROTOCOL_SPEC F/J P4K1; CHARTER Phase 4; GLOSSARY P4K1 | N/A | No |
| INV-B-P4K2 | P4K2 Combined short delta kill | PASS | PROTOCOL_SPEC F/J P4K2; CHARTER Phase 4; GLOSSARY P4K2 | N/A | No |
| INV-C-01 | Gate 0->1 leakage audit | PASS | PROTOCOL_SPEC F Phase 0 exit; CHARTER Phase 0 exit | N/A | No |
| INV-C-02 | Gate 0->1 SimBroker 15%/100 fills | PASS | PROTOCOL_SPEC F Phase 0 exit; CHARTER Phase 0 exit; GLOSSARY SimBroker | N/A | No |
| INV-C-03 | Gate 0->1 Trial registry operational | PASS | PROTOCOL_SPEC F Phase 0 exit; CHARTER Phase 0 exit; workflow_ai_development Section 6 | N/A | No |
| INV-C-04 | Gate 0->1 Data continuity >=90d | PASS | PROTOCOL_SPEC F Phase 0 exit; CHARTER Phase 0 exit | N/A | No |
| INV-C-05 | Gate 0->1 P4 3-year labels | AMBIGUOUS | PROTOCOL_SPEC/CHARTER Phase 0 exits require output; no P4 algorithm in any loaded doc | N/A | No |
| INV-C-06 | Gate 0->1 P1 synthetic test suite | AMBIGUOUS | PROTOCOL_SPEC F and CHARTER Phase 0 exits mention test; ARCHITECT_BRIEF known gap on recovery sequencing | N/A | No |
| INV-C-07 | Gate 1->2 15mo + 2 regimes | AMBIGUOUS | PROTOCOL_SPEC F Phase 1 exit; CHARTER Phase 1 exit; depends on unresolved P4 label validity | N/A | No |
| INV-C-08 | Gate 1->2 Sharpe >=0.28 | AMBIGUOUS | PROTOCOL_SPEC/CHARTER/GLOSSARY Net Sharpe + CI claim arithmetically inconsistent | N/A | No |
| INV-C-09 | Gate 1->2 HL/K1-K3 consistency | AMBIGUOUS | PROTOCOL_SPEC F/J; CHARTER Phase 1; GLOSSARY (HL and K3 formula incompleteness) | N/A | No |
| INV-C-10 | Gate 2->3 Phase 2 criteria | AMBIGUOUS | PROTOCOL_SPEC F Phase 2; CHARTER Phase 2; false-trigger and P4 definitions incomplete | N/A | No |
| INV-C-11 | Gate 3->4 Phase 3 criteria | AMBIGUOUS | PROTOCOL_SPEC F Phase 3; CHARTER Phase 3; K4 formula unspecified | N/A | No |
| INV-C-12 | Gate 4->5 direct transition rule | FAIL | No direct 4->5 gate in PROTOCOL_SPEC/CHARTER; Phase 5 prerequisite references Phase 1 + live capital | N/A | No |
| INV-C-13 | Phase 5 prerequisite protocol | AMBIGUOUS | PROTOCOL_SPEC F Phase 5; CHARTER Phase 5 (live-capital measurement protocol not formalized) | N/A | No |
| INV-D-P1 | P1 DD circuit breaker | AMBIGUOUS | PROTOCOL_SPEC D; CHARTER D; ARCHITECT_BRIEF D (HWM specifics not formalized) | N/A | No |
| INV-D-P2 | P2 funding exit | PASS | PROTOCOL_SPEC D; CHARTER D; GLOSSARY Regime hierarchy | N/A | No |
| INV-D-P3 | P3 correlation trigger | AMBIGUOUS | PROTOCOL_SPEC D; CHARTER D; GLOSSARY Regime hierarchy (population undefined) | N/A | No |
| INV-D-P4 | P4 weekly overlay | AMBIGUOUS | PROTOCOL_SPEC D/E/F requires outcomes; no algorithm in PROTOCOL_SPEC/CHARTER/GLOSSARY/EVOLUTION | N/A | No |
| INV-D-CR-01 | Priority override rule | PASS | PROTOCOL_SPEC D conflict rules; CHARTER D conflict rules; ARCHITECT_BRIEF C | N/A | No |
| INV-D-CR-02 | Non-multiplicative combination | PASS | PROTOCOL_SPEC D rule 2; CHARTER D rule 2 | N/A | No |
| INV-D-CR-03 | Regime label immutability | AMBIGUOUS | PROTOCOL_SPEC D immutability; CHARTER D immutability; vintage handling absent | N/A | No |
| INV-D-U1 | Undefined P1 recover while P3 active | FAIL | ARCHITECT_BRIEF C known gap; absent explicit state rule in PROTOCOL_SPEC D / CHARTER D | N/A | No |
| INV-D-U2 | Undefined P3 trigger during P1 suspension | FAIL | ARCHITECT_BRIEF C known gap; absent explicit state rule in PROTOCOL_SPEC D / CHARTER D | N/A | No |
| INV-D-U3 | Undefined P3 ramp interrupted by P1 | FAIL | ARCHITECT_BRIEF C known gap; absent explicit state rule in PROTOCOL_SPEC D / CHARTER D | N/A | No |
| INV-D-U4 | Undefined P4 change during P1 active hold | FAIL | ARCHITECT_BRIEF C known gap; absent explicit state rule in PROTOCOL_SPEC D / CHARTER D | N/A | No |
| INV-E-01 | Net Sharpe stream composition | FAIL | PROTOCOL_SPEC/CHARTER NN-2 define a+b+c; Phase 1 metric rows use "a+c" in multiple docs | N/A | No |
| INV-E-02 | Net Sharpe CI arithmetic | FAIL | CHARTER C; PROTOCOL_SPEC C/F; GLOSSARY Net Sharpe repeat +/-0.15-0.20 claim; REVIEW_REPORT F-2 derivation conflict | N/A | No |
| INV-E-03 | Harvey-Liu formula spec completeness | AMBIGUOUS | PROTOCOL_SPEC B/F/J; CHARTER NN-5; GLOSSARY Deflated Sharpe (formula absent everywhere) | N/A | No |
| INV-E-04 | IC_long prior + suspect policy | AMBIGUOUS | GLOSSARY IC section; PROTOCOL_SPEC I Q1; no suspect threshold counterpart to IC_short | N/A | No |
| INV-E-05 | IC_short prior + suspect threshold | PASS | PROTOCOL_SPEC Phase 3; CHARTER correction language; GLOSSARY IC rules | N/A | No |
| INV-E-06 | N_eff formula selection | FAIL | PROTOCOL_SPEC J1 gives explicit formula; elsewhere DR+clustering language lacks locked estimator | N/A | No |
| INV-E-07 | FLAM marginal formula + BR inputs | FAIL | CHARTER/GLOSSARY BR_long expression arithmetic inconsistency (5x2x12=120 vs stated 240); PROTOCOL_SPEC/REVIEW_REPORT unresolved | N/A | No |
| INV-E-08 | K4 t-stat formula definition | AMBIGUOUS | K4 threshold exists in PROTOCOL_SPEC/CHARTER/GLOSSARY; no explicit t-stat computation variant | N/A | No |
| INV-E-09 | P3 rho metric protocol | AMBIGUOUS | Threshold in PROTOCOL_SPEC/CHARTER/GLOSSARY; return interval/population not specified | N/A | No |
| INV-E-10 | K5 denominator/window protocol | AMBIGUOUS | "any 12-month period" present; rolling/calendar and denominator conventions unspecified | N/A | No |
| INV-E-11 | Funding-drag annualization protocol | AMBIGUOUS | P4K1 threshold present; estimator details scattered and incomplete | N/A | No |
| INV-E-12 | Sharpe-delta uncertainty protocol | AMBIGUOUS | Delta thresholds in P2/P4; no general SE/confidence method for rolling-window delta tests | N/A | No |
| INV-F-01 | Registry prereg before data | PASS | PROTOCOL_SPEC B/E/G/J1; CHARTER NN-5; workflow_ai_development policy | N/A | No |
| INV-F-02 | GE-1 suspicious improvement control | PASS | PROTOCOL_SPEC J1 Rule GE-1 (no contradiction elsewhere) | N/A | No |
| INV-F-03 | GE-2 allocation-only exemption boundary | AMBIGUOUS | PROTOCOL_SPEC J1 GE-2 + E Submodule2; edge-case boundaries not formally specified | N/A | No |
| INV-F-04 | GE-3 signal mods always prereg | PASS | PROTOCOL_SPEC J1 GE-3; F phase rules; workflow policy alignment | N/A | No |
| INV-F-05 | GE-4 CRR threshold actions | PASS | PROTOCOL_SPEC J1 GE-4; Growth Layer E Submodule1 | N/A | No |
| INV-F-06 | GE-5 N_eff optimization scope | PASS | PROTOCOL_SPEC J1 GE-5; F phase freeze constraints | N/A | No |
| INV-F-07 | GE-6 CER deterioration review | PASS | PROTOCOL_SPEC J1 GE-6 | N/A | No |
| INV-F-08 | RDL dormancy phase boundary | FAIL | PROTOCOL_SPEC E says "operational from Phase 2+" but also "Phase 2 exit criteria met before routing influence"; workflow_ai_development Section 6 says Phase 2+ operational boundary | N/A | No |
| INV-F-09 | Growth locked until RBE activation | AMBIGUOUS | PROTOCOL_SPEC E/J2 enforce lock; no independent definition of "charter-level review" | N/A | No |
| INV-F-10 | RDL submission-time trial counting | FAIL | Present in PROTOCOL_SPEC E only; absent in GLOSSARY and other governance docs | N/A | No |
| INV-F-11 | RDL non-interaction with RBE | FAIL | Present in PROTOCOL_SPEC E; not mirrored in workflow governance policy or glossary | N/A | No |
| INV-F-12 | Four-stream blending prohibition | PASS | PROTOCOL_SPEC B/C/F; CHARTER B/C; GLOSSARY P&L attribution | N/A | No |
| INV-F-13 | RBE transition log immutability | PASS | PROTOCOL_SPEC J2 RBE Transition Log (no contradiction elsewhere) | N/A | No |
| INV-F-14 | Finding lifecycle closure governance | PASS | workflow_ai_development Section 3; review_pipeline + PROMPT_0 hard constraints | N/A | No |
| INV-G-GL-01 | Growth lock default | AMBIGUOUS | PROTOCOL_SPEC E/J2 states lock; no cross-doc enforcement artifact | N/A | No |
| INV-G-GL-02 | RBE charter-review prerequisite | FAIL | PROTOCOL_SPEC E/J2 uses term; no operational definition in CHARTER/EVOLUTION/workflow | N/A | No |
| INV-G-GL-03 | RBE Step 4 freeze prohibition | PASS | PROTOCOL_SPEC J2 Step 4 prohibition + freeze policy K | N/A | No |
| INV-G-GL-04 | Step sequence + rollback moratorium | AMBIGUOUS | PROTOCOL_SPEC J2 defines rule but stop-condition specificity uneven across steps | N/A | No |
| INV-G-GL-05 | Step 1 no risk increase | AMBIGUOUS | PROTOCOL_SPEC J2 Step 1 with GE-2/GE-3 interaction boundary not bright-line in edge cases | N/A | No |
| INV-G-GL-06 | Step 2 entry condition formulas | AMBIGUOUS | PROTOCOL_SPEC J2 Step 2 conditions defined; metric estimator methods incomplete | N/A | No |
| INV-G-GL-07 | Step 3 DD micro-adjustment constraints | AMBIGUOUS | PROTOCOL_SPEC J2 Step 3 constraints present; interaction with kill framework not codified elsewhere | N/A | No |
| INV-G-GL-08 | RBE cannot override NN-1 | PASS | PROTOCOL_SPEC J2 Step 0/Step4 constraints; NN-1 preserved in B/K | N/A | No |
| INV-G-RDL-01 | RDL dormancy (scaffolding-only pre-2) | AMBIGUOUS | PROTOCOL_SPEC E + workflow Section 6 aligned generally, but auditable state flag absent | N/A | No |
| INV-G-RDL-02 | RDL submission-count budget rule | FAIL | Rule appears in PROTOCOL_SPEC E; absent in GLOSSARY and registry governance references | N/A | No |
| INV-G-RDL-03 | RDL routing influence phase gate | AMBIGUOUS | PROTOCOL_SPEC E uses "Phase 2 exit criteria met"; workflow states operational starts at Phase 2+ | N/A | No |
| INV-G-RDL-04 | RDL never feeds RBE triggers | FAIL | Explicit in PROTOCOL_SPEC E only; no corroborating governance rule outside spec | N/A | No |
| INV-G-RDL-05 | RDL-2 depends on P4 prereg spec | FAIL | PROTOCOL_SPEC E references missing P4 prereg spec; absent everywhere else | N/A | No |
| INV-G-RDL-06 | RDL-3 new version requires new registry entry | PASS | PROTOCOL_SPEC E RDL-3 + GE-3 cross-reference consistent | N/A | No |
| INV-G-RDL-07 | RDL-4 pre-Phase-2 logging-only constraint | AMBIGUOUS | PROTOCOL_SPEC E states constraint; timestamp convention controls not defined in glossary/governance docs | N/A | No |
| TOTAL | — | PASS: 30 / FAIL: 17 / AMBIGUOUS: 34 | — | — | Regressions: 0 |

