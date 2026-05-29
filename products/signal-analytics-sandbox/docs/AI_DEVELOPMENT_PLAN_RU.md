# AI Development Plan RU - Signal Analytics Sandbox

Date: 2026-05-19
Status: post-v1-internal-validation-plan

## 0. Где мы сейчас

Система уже прошла внутренний V1 loop:

- есть public-source capture для трех Telegram-каналов;
- есть нормализация рыночных утверждений в claim surface;
- есть review-калибровка false positive / false negative;
- есть structured claim extractor;
- есть deterministic outcome engine;
- есть provider/proxy config;
- есть V1 metric recompute;
- есть customer-readable candidate report;
- есть external gate.

Текущий gate: `approve_internal_only`.

Это значит: внутренний продуктовый прототип работает, но платный внешний отчет
пока нельзя выпускать как готовый продукт. Следующий этап - превратить
исследовательский pipeline в повторяемый paid-pilot workflow.

## 1. Product Goal

Сделать систему, которая для любого публичного канала может:

1. собрать публичные текстовые, аудио и image/OCR артефакты;
2. извлечь рыночные claims;
3. нормализовать claims в единый формат;
4. проверить claims на исторических данных через открытые API или
   operator-approved public exports;
5. посчитать полезность канала по метрикам;
6. показать evidence, misses, limitations и blockers;
7. выпустить отчет только если external gate безопасно разрешает delivery.

## 2. Non-Negotiable Guardrails

- Только public/operator-authorized sources.
- Никакого private Telegram scraping, login bypass или paywalled обхода.
- No private Telegram scraping remains a hard product boundary.
- Никакого investment advice.
- Никаких future-profit claims.
- Никакого leaderboard/marketplace до отдельного legal/product решения.
- Unreviewed transcript/OCR/chart claims не попадают в customer-facing metrics.
- Unsupported providers/proxies считаются exclusions, не wins/losses.
- Market history не храним огромной базой; используем on-demand windows и
  compact reproducibility snapshots.
- Каждый customer-facing отчет проходит external-ready gate.
- Customer-facing отчет проходит external-ready gate before delivery.

## 3. Development Tracks

| Track | Цель | Почему важно |
|---|---|---|
| External-ready trust | Довести один V1 report до безопасного paid-pilot состояния | Без этого нельзя продавать отчет |
| Quant quality | Сделать метрики похожими на финансовую оценку, а не простой hit-rate | Это повышает ценность для клиента |
| Review operations | Ускорить human/operator review | Без review UI масштаб не взлетит |
| Provider/media coverage | Покрыть больше рынков и multimodal evidence | Меньше useful claims будет выпадать |
| Product packaging | Сделать повторяемый report/demo workflow | Это превращает код в продукт |

## 4. Proposed Phase Graph

### Phase 28 - External-Ready Review Sprint

Goal: довести один трехканальный V1 отчет до состояния, которое можно показать
потенциальному покупателю как internal pilot/demo, а не как production claim.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-001 | Full-corpus human review queue | `docs/pilot/three_channel_FULL_REVIEW_QUEUE.md/json` | Все included/excluded candidates имеют review status или explicit carry-forward reason. |
| SAS-NEXT-002 | False-negative extraction pass | обновленный extractor calibration | False negatives из V1 review либо extracted, либо documented as unsupported. |
| SAS-NEXT-003 | Report language safety pass | revised V1 report | Нет advice, future-profit, unsupported ranking, exaggerated accuracy wording. |
| SAS-NEXT-004 | External gate rerun | revised external gate | Gate явно: approve external / internal only / reject, с blockers. |

Definition of done:

- full review coverage recorded;
- V1 report has no overclaim language;
- all metrics trace back to evidence and provider metadata;
- external gate decision is defensible.

### Phase 29 - Review UI And Operator Workflow

Goal: убрать ручную markdown/json боль и дать человеку быстрый интерфейс для
подтверждения claims.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-005 | Review data model | `src/signal_sandbox/review/` | Claim review statuses, reasons, reviewer id, timestamp, source refs. |
| SAS-NEXT-006 | Review queue API/export | CLI/API export | Можно загрузить claims и выгрузить reviewed decisions deterministically. |
| SAS-NEXT-007 | Minimal review UI | local web UI or static HTML workflow | Reviewer can accept/reject/needs_context claims and save artifact. |
| SAS-NEXT-008 | Review audit trail | review audit artifact | Every decision has source URL, evidence span, reviewer, and reason. |

Recommended UI shape:

- dense table, not marketing UI;
- filters by channel, claim type, asset, provider status, review status;
- side-by-side source text and normalized claim;
- keyboard shortcuts only if they do not hide functionality;
- explicit buttons: accept, false positive, false negative, needs context,
  unsupported provider, media blocked.

### Phase 30 - Provider And Proxy Expansion

Goal: уменьшить потери полезных claims из-за неподдержанных рынков.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-009 | US equity/fund provider path | provider config + tests | `SPY`, liquid US tickers/funds have approved public provider route or explicit unsupported status. |
| SAS-NEXT-010 | FX proxy policy | FX proxy spec | `CNY`, USD/RUB-like pairs have direction semantics, source, and exclusions. |
| SAS-NEXT-011 | Futures/commodity policy | futures proxy spec | `BR`, `NG`, `GOLD`, `SI`, index futures have rollover/proxy rules or remain excluded. |
| SAS-NEXT-012 | Benchmark-relative outcomes | outcome extension | Claims can be measured vs approved benchmark where valid. |

Do not:

- silently map ambiguous shorthand to random tickers;
- mix futures continuous contracts without rollover rules;
- treat missing provider as a failed call.

### Phase 31 - Quant Metrics V2

Goal: перейти от простого hit-rate к оценке полезности, риска и торгуемости.

Metrics to add:

- precision / recall of extractor after human review;
- hit rate by claim type;
- avg and median directional return;
- MFE / MAE;
- entry fill rate;
- target hit rate;
- stop hit rate;
- timeout rate;
- average RR;
- realized R multiple where entry/stop/target exist;
- benchmark-relative return;
- volatility-adjusted return;
- drawdown of naive follow strategy;
- performance by asset class and market regime;
- stale-signal / repeated-signal deduplication.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-013 | Quant metric schema V2 | `docs/specs/CHANNEL_QUANT_METRICS_V2.md` | Metric definitions, formulas, exclusions, and examples are documented. |
| SAS-NEXT-014 | Setup outcome expansion | outcome code + tests | Entry fill, stop, target, timeout, R multiple computed deterministically. |
| SAS-NEXT-015 | Channel utility score V2 | scorecard artifact | Score separates coverage, clarity, extraction quality, outcome quality, risk quality, and limitations. |
| SAS-NEXT-016 | Robustness checks | report appendix | Metrics show sample size, confidence warning, and sensitivity to horizon/provider. |

Important: channel score should not become a public leaderboard until legal and
product framing are reviewed.

### Phase 32 - Multimodal Expansion

Goal: audio, transcript, screenshots, charts and OCR should flow into the same
claim surface, but only after review.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-017 | Media acquisition inventory per channel | media inventory artifact | Public media refs and blockers recorded by channel. |
| SAS-NEXT-018 | Transcript human review workflow | transcript review artifact/UI | Transcript refs can be accepted/rejected for claim use. |
| SAS-NEXT-019 | OCR/chart source-link policy | OCR/chart policy | Chart claims need source-linked artifact and human accepted interpretation. |
| SAS-NEXT-020 | Multimodal claim recompute | V2 metric recompute | Reviewed media claims enter metrics; unreviewed media remains excluded. |

Stop condition:

- If media source cannot be linked to public evidence, do not use it.
- If chart interpretation is machine-only, keep it internal/draft.

### Phase 33 - Report Productization

Goal: reports become repeatable artifacts, not one-off markdown files.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-021 | Report template system | report renderer | Same data can render Markdown/HTML/PDF-ready output. |
| SAS-NEXT-022 | Evidence appendix generator | appendix artifact | Every metric row links to source, provider, snapshot, and review decision. |
| SAS-NEXT-023 | Buyer-demo pack | demo folder | Includes report, methodology, limitations, talk track, and gate status. |
| SAS-NEXT-024 | Customer-safe wording library | wording spec/tests | Blocks advice, future-profit, unsupported ranking, and overclaim phrases. |

Report sections:

1. Executive summary.
2. Source and period.
3. Coverage.
4. Reviewed claim quality.
5. Outcome metrics.
6. Confirmed examples.
7. Contradicted examples.
8. Exclusions and unsupported claims.
9. Media status.
10. Methodology.
11. Limitations.
12. External gate decision.

### Phase 34 - Pilot Operations

Goal: проверить, кто реально платит и за что.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-025 | Pilot buyer list | `docs/pilot/BUYER_DISCOVERY.md` | 10-20 buyer profiles with pains and expected use case. |
| SAS-NEXT-026 | Demo script | `docs/pilot/DEMO_SCRIPT.md` | 15-minute demo flow with clear limitations. |
| SAS-NEXT-027 | Paid pilot offer | offer artifact | Clear scope, price hypothesis, turnaround time, deliverables, exclusions. |
| SAS-NEXT-028 | Feedback loop | feedback log | Each demo records objection, willingness to pay, requested output, and next step. |

Buyer hypotheses:

- crypto fund/research desk wants source quality filtering;
- private investor community wants channel diligence;
- media/analytics firm wants evidence-backed influencer/source report;
- risk/compliance team wants "do not trust blindly" source audit.

### Phase 35 - Reliability And Scaling

Goal: сделать pipeline устойчивым и воспроизводимым.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-NEXT-029 | Run manifest and caching | run manifest schema | Every report run records inputs, versions, hashes, providers, and outputs. |
| SAS-NEXT-030 | Retry and provider failure handling | provider error model | API errors produce explicit retry/exclusion states. |
| SAS-NEXT-031 | Regression suite for known channels | golden tests | Known claims and metrics do not drift unexpectedly. |
| SAS-NEXT-032 | Cost/time instrumentation | run metrics | Capture, review, market data, and report generation time/cost are measured. |

### Phase 36 - Channel Impact Framework And Cross-Channel Completion

Goal: перейти от "прибыль/убыток по сигналам" к широкой оценке импакта канала
и применить одинаковый evidence loop к `bablos79`, `nemphiscrypts` и
`pifagortrade`.

Core idea:

- dashboard должен показывать компактные базовые метрики и confidence;
- paid deep report объясняет, почему канал так оценен, с evidence appendix;
- PnL - только один слой, а не вся ценность канала;
- trend sense, insight depth, methodology, risk management, practical
  usefulness и creativity должны быть first-class criteria;
- source of truth всегда разделяется на author statement, interpretation,
  market outcome, and product conclusion.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-IMPACT-001 | Impact rubric and truth model | `docs/specs/CHANNEL_IMPACT_FRAMEWORK.md` | PnL and non-PnL dimensions plus source-of-truth layers are explicit. |
| SAS-IMPACT-002 | Cross-channel development loop | loop artifact | Same loop applies to `bablos79`, `nemphiscrypts`, `pifagortrade`. |
| SAS-BABLOS-001..008 | `bablos79` completion path | per-channel artifacts | Text/audio/image gaps are closed or carried as blockers. |
| SAS-IMPACT-003 | `nemphiscrypts` completion scope | scope artifact | Same corpus/media/truth loop is defined. |
| SAS-IMPACT-004 | `pifagortrade` completion scope | scope artifact | Same corpus/media/truth loop is defined. |
| SAS-IMPACT-005 | Impact claim taxonomy expansion | taxonomy spec | Trend/insight/methodology/risk/creativity are reviewed evidence types. |
| SAS-IMPACT-006 | Dashboard score schema | score schema | Compact metrics, confidence, sample size, and gate are defined. |
| SAS-IMPACT-007 | Paid deep report boundary | boundary spec | Dashboard vs paid evidence/report content is separated. |
| SAS-IMPACT-008 | Cross-channel impact recompute and gate | scorecard + gate | Three-channel comparison is confidence-aware and no-advice. |

Stop condition:

- If source rows or media cannot be linked to public/operator-authorized
  evidence, keep them as blockers; do not infer claims.
- If a channel has useful qualitative evidence but few deterministic trade
  signals, score it as confidence-limited instead of forcing PnL conclusions.

## 5. Recommended Execution Order

Do not start with a big dashboard. The highest-signal order is:

1. `SAS-IMPACT-001..002` - lock impact criteria, truth model, and dev loop.
2. `SAS-BABLOS-001..008` - finish the `bablos79` evidence gap before using it
   as a long-period multimodal example.
3. `SAS-IMPACT-003..004` - apply the same completion scope to the other two
   channels.
4. `SAS-IMPACT-005..008` - taxonomy, dashboard schema, paid boundary, and
   cross-channel recompute/gate.
5. `SAS-NEXT-001..004` - external-ready review sprint.
6. `SAS-NEXT-005..008` - review UI/workflow.
7. `SAS-NEXT-013..016` - quant metrics V2.
8. `SAS-NEXT-009..012` - provider/proxy expansion.
9. `SAS-NEXT-021..024` - report productization.
10. `SAS-NEXT-025..028` - buyer discovery and paid pilot.
11. `SAS-NEXT-017..020` - multimodal expansion, unless buyer feedback proves
   media is urgent earlier.
12. `SAS-NEXT-029..032` - reliability/scaling.

Reasoning:

- External readiness and review quality unlock trust.
- Review UI removes the biggest manual bottleneck.
- Quant metrics make the product financially meaningful.
- Provider expansion increases measurable coverage.
- Productized reports enable selling.

## 6. Two-Week AI Development Sprint

If an AI agent starts tomorrow, the practical first sprint should be:

### Week 1

1. Build full-corpus review queue schema and artifact.
2. Add deterministic review decision loader.
3. Add tests that V1 metrics only use accepted rows.
4. Draft report language safety rules.
5. Prepare minimal review UI or static HTML review surface.

### Week 2

1. Run full review on the three pilot channels.
2. Recompute V1.1 metrics.
3. Regenerate report and gate.
4. Build internal buyer-demo pack.
5. Write buyer-discovery script and pilot offer.

Sprint exit:

- one demo-ready internal package;
- clear external blockers;
- 3-5 buyer conversations scheduled or logged;
- no unreviewed claim in customer-facing language.

## 7. AI Agent Implementation Contract

Every task should include:

- task id;
- input artifacts;
- output artifacts;
- code paths touched;
- tests added/updated;
- validation commands;
- rollback/stop conditions;
- external boundary statement.

Default validation:

```bash
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check src/ tests/ scripts/
.venv/bin/ruff format --check src/ tests/ scripts/
.venv/bin/pyright
```

When touching market/outcome logic, also include:

- deterministic fixture snapshots;
- Decimal-based expected values;
- explicit insufficient data cases;
- provider gap exclusions.

When touching reports, also include:

- no-advice wording checks;
- no future-profit wording checks;
- source/evidence link checks;
- external gate status checks.

## 8. Success Criteria

Internal success:

- AI can process a new public channel and produce an internal report with
  evidence, metrics, misses, and limitations.

Paid-pilot success:

- a buyer agrees to pay for a bounded diligence report, even if the answer is
  "this channel is not reliable enough".

Product success:

- reports are repeatable across channels;
- review cost per channel goes down;
- useful claims and misses are both visible;
- customer gets a decision-support artifact without investment advice.

## 9. Current Recommendation

Phase 37 pre-client artifact hardening is complete. The review decision is
`continue_internal_hardening`, so start Phase 38 client-readiness evidence
acceptance before any buyer outreach, paid delivery, private-channel analysis,
or marketplace scope.

Current next task is:

Phase 38 - Client-Readiness Evidence Acceptance.

Why:

- `SAS-IMPACT-001..002` already define the framework and cross-channel loop;
- `SAS-BABLOS-003..008` completed the `bablos79` Phase 36 pass as
  internal-only: 0 human/operator accepted transcripts, 0 OCR drafts,
  0 accepted media claims, 0 computed outcomes;
- `SAS-IMPACT-003..004` applied the same corpus/media/truth completion scope to
  `nemphiscrypts` and `pifagortrade`;
- `SAS-IMPACT-005..008` added taxonomy, dashboard score schema, paid boundary,
  three-channel scorecard, external gate, and deep review;
- two-month multimodal and media-reviewer runs now provide enough internal
  evidence to build reliable artifacts before customer outreach;
- Phase 37 produced internal artifacts and a safety gate, but still has
  0 operator-accepted media claims, 0 dashboard-safe RR rows, and
  0 market-outcome recomputed candidates.

### Phase 37 - Pre-Client Artifact Hardening

Goal: produce reliable internal artifacts for a free dashboard and paid deep
report workflow before talking to clients. This phase includes only work the AI
development loop can do itself with public/operator-authorized evidence and
existing model-review outputs.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-PRECLIENT-001 | Product artifact contract and reliability bar | `docs/specs/PRECLIENT_ARTIFACT_CONTRACT.md` | Artifact list, reliability states, audience boundary, and review gates are explicit. |
| SAS-PRECLIENT-002 | Model-reviewed candidate review packet | `docs/pilot/preclient_MODEL_REVIEW_PACKET.md/json` | 9 arbiter-accepted rows and mass-accepted rows are source-linked and queued for operator action. |
| SAS-PRECLIENT-003 | Evidence appendix builder | `preclient_EVIDENCE_APPENDIX.md/json` | Text/media/review/outcome refs are traceable by channel without raw media bytes. |
| SAS-PRECLIENT-004 | Free dashboard card dataset | `preclient_FREE_DASHBOARD_CARDS.md/json` | One safe summary card per channel with strengths, weaknesses, confidence, and gate status. |
| SAS-PRECLIENT-005 | Per-channel internal deep reports | `reports/preclient/*_DEEP_REPORT_V0.md` | Three channel reports cite evidence, strengths, weaknesses, examples, blockers, and internal gate. |
| SAS-PRECLIENT-006 | Paid-style demo report | `PAID_STYLE_DEMO_REPORT.md` | One polished internal demo report shows the product promise without external approval. |
| SAS-PRECLIENT-007 | Candidate outcome/RR recompute | `preclient_CANDIDATE_OUTCOMES.md/json` | Review candidates are evaluated or explicitly blocked by fields/provider/post-factum/media status. |
| SAS-PRECLIENT-008 | Static free dashboard prototype | `preclient_dashboard/index.html` | Internal static dashboard renders the free cards, no ranking or advice. |
| SAS-PRECLIENT-009 | Artifact safety gate | `preclient_ARTIFACT_SAFETY_GATE.md/json` | Dashboard-safe, paid-report-only, internal-only, and blocked fields are decided. |
| SAS-PRECLIENT-010 | Phase 37 deep review | `docs/archive/PHASE37_PRECLIENT_REVIEW.md` | Decide proceed to client discovery, continue hardening, or pivot scope. |

Definition of done:

- every claim in a report/card traces to evidence or an explicit blocker;
- model-reviewed media is not customer-facing until human/operator accepted;
- no dashboard/report text implies investment advice, future returns, ranking,
  or private-source access;
- the safety gate says exactly what can be shown in first buyer conversations.

### Phase 38 - Client-Readiness Evidence Acceptance

Goal: turn the Phase 37 internal artifact stack into a defensible buyer-demo
candidate without starting outreach yet.

Tasks:

| Task ID | Task | Output | Acceptance Criteria |
|---|---|---|---|
| SAS-CLIENTREADY-001 | Operator media acceptance ledger | `clientready_OPERATOR_MEDIA_LEDGER.md/json` | 9 model-reviewed candidates receive operator accepted/rejected/needs-context/post-factum decisions. |
| SAS-CLIENTREADY-002 | Accepted candidate RR/outcome recompute | `clientready_ACCEPTED_OUTCOMES.md/json` | Only operator-accepted sufficient rows are recomputed through approved public providers. |
| SAS-CLIENTREADY-003 | Redacted buyer demo subset | `clientready_REDACTED_BUYER_DEMO.md/json` | A compact showable candidate excludes full appendix/raw media and forbidden language. |
| SAS-CLIENTREADY-004 | Discovery gate and success criteria | `clientready_DISCOVERY_GATE.md/json` | Decide ready_for_discovery, continue_internal_hardening, or pivot_scope before outreach. |
