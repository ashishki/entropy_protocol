# Trader Risk Audit Workspace Startup Pressure Test

Дата: 2026-05-07
Режим: deep/full
Основа: чтение `products/trader-risk-audit` на ветке `codex/trader-risk-audit-work`, root portfolio docs, web research по рынку, конкурентам и текущим workflow трейдеров.

## 1. Verdict

**Strong, but only after validation.**

Текущий wedge `trade upload + rule violation audit` является правильным первым сужением, потому что он проверяет платную боль без брокерских API, live capital, SaaS, стратегии и Telegram scraping. Но продукт пока не доказал бизнес: текущий код уже закрывает Phase 5 concierge workflow, а главный риск теперь не engineering, а то, заплатят ли трейдеры за post-trade дисциплину повторно. Следующий шаг - не расширять продукт, а продать 3-5 ручных аудитов реальным трейдерам с реальными экспортами и письменными правилами. Если трейдеры говорят "классный отчет", но не платят, не дают экспорт и не возвращаются через 2-4 недели, проект надо остановить или split/pivot.

## 2. Strategic Reframe

**Что это реально, исходя из repo:** локальный deterministic audit workflow. Трейдер дает trade export и risk policy, оператор нормализует CSV, система детерминированно проверяет правила, атрибутирует P&L, генерирует Markdown report, Telegram-ready packet и artifact manifest. В коде уже есть canonical trade schema, CSV importer, policy schema, review packet gate, deterministic rule evaluation, P&L attribution, report model, claim guard, manifest, retention/delete и pilot regression fixtures.

**Что это не:** не trading journal общего назначения, не backtesting platform, не signal analytics product, не live risk guard, не broker automation layer, не AI strategy generator, не SaaS dashboard и не investment advice.

**Какие комментарии трейдера совпадают с текущим продуктом:** "первый вариант может просто загружать сделки и проверять все сделки против правил"; Telegram-first packaging как delivery surface; идея контроля дисциплины после факта; возможность small teams / Russian trading teams как warm-intro ICP.

**Какие комментарии ведут к отдельным продуктам:** backtesting strategies, live API lockout "минус 2%, 24 часа не торговать", Telegram/X signal stats/equity curve, natural-language strategy-to-code, screenshot/chart learning. Это adjacent wedges, но они имеют другую data model, другой risk profile и другую buying trigger.

**Что не строить сейчас:** broker/exchange API, order blocking, public SaaS, full dashboard, mobile app, strategy generator, Telegram channel parser, paid X API dependency, private Telegram scraping, marketplace, live execution, institutional compliance tooling.

**Самый сильный narrow wedge:** "audit-as-evidence" для трейдеров, у которых уже есть письменные risk rules и внешний стимул соблюдать их: prop/funded-account traders, active discretionary crypto traders с self-imposed rules, small teams/coaches, которые хотят weekly accountability report.

## 3. Scorecard

Скоринг: 1 = плохо/слабый сигнал, 5 = сильно/хороший сигнал.

| Area | Score | Evidence |
|---|---:|---|
| Pain intensity | 3/5 | Потеря денег из-за rule-breaking реальна, особенно у prop/funded traders: FTMO прямо определяет max daily loss/max loss как account-failing rules. Но еще не доказано, что pain достаточно сильна именно для post-trade paid audit. |
| Buyer clarity | 3/5 | Primary ICP можно сузить до prop/funded-account traders и small teams с explicit rules. Broad retail слишком размыт и часто не имеет формализованных правил. |
| Urgency | 2/5 | After-the-fact report может быть vitamin, если нет внешнего наказания, coach/team accountability или payout risk. Urgency вырастает, если трейдер уже терял funded account, payout или капитал из-за нарушения rules. |
| Differentiation | 3/5 | Journals уже умеют analytics, imports, risk metrics, AI/replay/backtesting. Дифференциация только в deterministic violation truth + source-row evidence + self-defined policy audit, а не в "красивой аналитике". |
| Speed to validate | 5/5 | Можно валидировать вручную за 14 дней: 10 calls, 5 real exports, 3 paid reports. Код уже достаточен для concierge pilot, но его не надо продавать как SaaS. |
| Founder advantage | 3/5 | Технический founder может быстро строить deterministic audit artifacts, но это же главный риск: уйти в infra вместо продаж. Advantage появится только через доступ к trader communities и теплым интро. |
| Trust/liability risk | 3/5 | Manageable в v1, потому что нет live control и advice claims. Становится 1/5 при broker API/order blocking: API trading несет trading-loss liability, regulatory scrutiny и security burden. |
| Engineering scope risk | 4/5 | Риск низкий, если держать local-first CLI, fixed schemas, rule taxonomy, claim guard. Риск резко растет при broker integrations, Telegram scraping, SaaS auth, AI strategy generation. |
| Distribution access | 2/5 | Пока нет доказанной access path. Russian teams могут быть reachable, но relationship-heavy sales нельзя считать scalable channel до теплых интро и paid pilots. |
| Retention potential | 3/5 | Weekly/monthly audit может повторяться, если отчет становится accountability loop. Если это одноразовая curiosity report, retention слабая. |
| Fit with current codebase | 5/5 | Repo уже идеально соответствует narrow wedge: deterministic local audit, artifacts, Telegram-ready summary, retention, no live API guardrails. |

## 4. Wedge Comparison

| Wedge | User | Pain | Current workaround | WTP likelihood | Sales difficulty | Engineering complexity | Liability/compliance risk | Fit with workspace | Fastest validation test | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1. Trade Upload + Rule Violation Audit | Prop/funded traders, active discretionary traders, small teams/coaches | "Я нарушил свои правила, потерял деньги, не вижу точную картину" | Excel/Sheets, broker CSV, TradeZella/TraderSync/Tradervue/Edgewonk, Notion, manual journal, ChatGPT | Medium: если есть external accountability, payout risk или coach | Medium: trust/data-sharing barrier | Low-medium: importer + policy schema + deterministic rules | Low if no advice/live control | Excellent | 10 prospects -> 5 exports -> 3 paid reports | **Build only as manual/concierge pilot; validate now** |
| 2. Live Broker/Exchange Risk Guard | Traders who want self-lockout and pre-trade blocking | "Я не могу остановиться после -2%" | Broker limits, exchange risk settings, prop dashboard rules, manual discipline, separate account, platform max loss tools | Potentially high, but only if trust is solved | High: requires credentials, trust, legal comfort | High: APIs, secrets, order state, latency, fail-safe, broker variance | Very high: capital-adjacent control, trading loss disputes, advice/control boundary | Poor for current v1 | Concierge interview: last live breach, willingness to use read-only monitor first, legal/security objection | **Defer; decision gate only** |
| 3. Hypothesis & Backtesting Workbench | Systematic retail traders, strategy testers | "У меня есть идея, хочу быстро проверить" | TradingView Strategy Tester, MT5 tester, Python notebooks, Excel, backtesting.py/vectorbt, TradeZella/TraderSync/TradesViz replay/backtest | Medium-high in broad market, but crowded | High: strong expectations and benchmarks | High: data, execution assumptions, OOS, slippage, strategy DSL | Medium-high: performance claims risk | Weak for current workspace; belongs near Entropy Core/hypothesis bridge | Ask paid pilot users whether their next paid request is audit or hypothesis test | **Defer/separate unless audit pilots demand it** |
| 4. Telegram Signal Analytics Bot | Signal subscribers, crypto traders, market researchers | "Канал обещает win rate, хочу проверить" | Telegram groups, screenshots, Telemetrio/TGStat, SignalBlink/BotLedger-like tools, manual spreadsheet | Medium: viral curiosity; trust hard | Medium: public channels easier, private channels harder | High: parsing signals, market data, edits/deletes, private access, X API cost | Medium: not advice if framed as analytics, but claims sensitive | Separate sandbox already exists | Manually audit 3 public channels and sell one report to subscribers | **Separate product; do not contaminate TRA** |
| 5. Natural-Language Strategy Builder | Novice systematic traders | "Опишу стратегию, пусть сделает код/backtest" | ChatGPT/Claude, TradingView Pine, freelancers, strategy builders | Low-medium: many want magic, few pay for rigorous constraints | High: expectations unrealistic | Very high: codegen, backtesting, validation, support | High: performance/advice claims | Bad | Landing/interview test only; no build | **Reject for now** |
| 6. Chart/Screenshot-to-Rules Assistant | Visual discretionary traders/coaches | "Покажи на графике сетап и найди похожее" | Screenshot journals, chart markup, TradingView screenshots, coaching sessions | Unknown | High: users struggle to specify truth | Very high: OCR/multimodal, chart state reconstruction, labeling | Medium: false pattern claims | Bad for v1 | Manual labeling service with 3 users; no automation | **Reject/defer hard** |

## 5. Core Assumption

**The business works only if active traders with explicit rules will repeatedly pay for a deterministic post-trade audit that shows rule violations, source rows, and violation-attributed P&L better than their current journal/spreadsheet workflow.**

| Assumption | Why it matters | Evidence currently available | Fastest test | Disconfirming signal | Decision if false |
|---|---|---|---|---|---|
| 1. Traders will share real exports and written rules | Without real data, no audit product exists | Trading tools already rely on imports; Tradervue documents import quotas and supported broker/platform workflows; TradingView and MT5 expose export/report paths | Ask 10 qualified prospects for last 30-90 days export + written rules before showing product | Fewer than 5/10 qualified prospects provide export/rules within 7 days | Stop upload product; pivot to education/coaching content or no-build |
| 2. Rule violations are painful enough to pay for | Curiosity reports do not build business | Prop firms enforce daily/max loss rules; funded traders have account-failing stakes | Sell $49-$149 one-time audit before building more | They accept free sample but refuse payment or delay indefinitely | Keep only as internal tool or pivot ICP |
| 3. Deterministic audit beats journals | Existing journals are strong and habit-forming | TradeZella, TraderSync, Edgewonk, TradesViz already offer imports, risk analytics, replay/backtesting/AI | Compare report against user's current journal in a call | User says their journal already shows everything needed | Narrow to teams/coaches or prop rules; do not compete with journals broadly |
| 4. Post-trade is enough before live blocking | If users only want blocking, audit is weak | Trader colleague asked for API lockout; exchanges/brokers already have some risk controls; live API adds high burden | Discovery: last rule breach, what they wanted at the moment, what they did after | Majority say "I only pay if it blocks trades live" | Defer live guard but evaluate read-only monitor as separate gate |
| 5. Reports can become recurring workflow | One-time autopsy is not a company | Current repo supports repeatable artifacts and retention, but no pilot evidence yet | 6-week pilot: weekly/monthly audit cadence | No repeat audit, no referral, no coach/team sharing | Stop productization; sell one-off service only or pivot |

## 6. Fatal Flaws

| Risk | Severity | Why it matters | Evidence to seek | Fast test | Kill/pivot threshold |
|---|---|---|---|---|---|
| Traders may not pay for post-trade discipline audits | High | They may like the report but not change payment behavior | Prepaid audit orders | Offer $49-$149 manual audit to 10 qualified prospects | <3 paid audits from 10 qualified prospects |
| Existing journals may be good enough | High | TradeZella/TraderSync/Edgewonk/TradesViz already own journaling, analytics, imports, replay/backtesting | Side-by-side comparison with user's existing tool | Ask users to show last journal review workflow | >50% say current journal already identifies rule breaks clearly enough |
| Traders may want live blocking, not after-the-fact reports | High | If the acute pain is impulse control at execution time, audit is late | Past breach stories: what they wanted in the moment | Discovery around last max-loss/cooldown breach | >50% only show WTP for live lockout |
| Live blocking creates liability and API/security burden | Critical | Order blocking means secrets, availability, false blocks, missed blocks, trading loss disputes | Legal memo, API terms, security review, broker coverage | Read-only monitoring pilot before any trade permissions | Any pilot requires trade permission before trust/legal gates |
| Exports may be too messy to normalize manually at scale | Medium | Broker CSVs vary; commission/timestamps/open P&L often missing | 5-10 real exports from ICP | Run manual taxonomy across exports | >40% exports require custom manual cleanup that users won't tolerate |
| P&L attribution may become disputed | High | If user disputes "violation-attributed P&L", trust dies | User review of source rows and attribution assumptions | Deliver report with row evidence and ask user to challenge it | >2 material disputes in first 5 audits |
| Russian trading teams may be reachable but sales may be relationship-heavy | Medium | Warm intros may work; cold sales may not | Intro conversion rate, trust/privacy objections | 10 warm intro asks through trader colleague network | No warm intros or no export sharing despite interest |
| Telegram signal analytics may be more viral but a different product | Medium | Could distract founder into a market with different user, data, and claims | Separate landing/manual report test in sandbox | One manual public-channel report sold separately | Do not merge; split if stronger evidence appears |
| Founder may keep building infra instead of selling reports | Critical | Code is already ahead of market proof | Calendar/time audit | Freeze feature work; only sales + manual delivery for 14 days | Any new feature before 3 paid reports triggers build pause |

## 7. Problem Reality

**Exact painful moment:** after a losing day/week, the trader suspects they broke rules but cannot prove exactly where, how often, and how much P&L came from those breaches. The sharpest version is not "I want analytics"; it is "I violated max daily loss/cooldown/position size, I may lose funded status or payout, and I need evidence."

**Who feels it most sharply:** prop/funded-account traders, active discretionary crypto/futures traders with real written rules, small teams/coaches reviewing discipline. Broad retail traders with vague "be disciplined" goals feel shame but often lack structure and WTP.

**What they do today:** export broker/platform history, use Excel/Google Sheets, use TradingView/MT5 reports, use TradeZella/TraderSync/Tradervue/Edgewonk/TradesViz, journal in Notion/paper, ask a coach, screenshot charts, or paste data into ChatGPT/Claude.

**Workaround cost:** time, inconsistency, shame/privacy friction, manual mistakes, no source-row evidence, no explicit deterministic policy, and reports that visualize performance without forcing "which rule did I break?"

**Painkiller or vitamin:** currently a **conditional painkiller**. It is painkiller for users with external accountability or repeated costly rule-breaking; vitamin for broad retail traders who merely want another dashboard.

**Behavior proving urgency:** user prepays, sends real export/rules within 24 hours, argues about source rows, asks for next audit date, shares report with coach/team, or asks for monthly accountability.

### JTBD Ranking

| JTBD | Trigger | Desired outcome | Frequency | WTP signal | Retention strength | Build decision |
|---|---|---|---|---|---|---|
| 1. Upload trades and detect rule violations | Bad day/week, funded account review, coach session | Know exact rule breaches with timestamps/source rows | Weekly/monthly for active traders | Pays for audit, provides export | Medium-high if accountability loop | Build now, concierge-first |
| 2. Quantify P&L damage from rule violations | Suspects discipline costs money | Separate compliant vs violating P&L | Weekly/monthly | Challenges attribution and still pays | High if trusted | Build now, but with careful claim guard |
| 3. Identify repeated discipline patterns | Repeated losses or review session | See recurring rule IDs/days | Weekly/monthly | Asks for trend over multiple audits | High if recurring | Build now in report, not dashboard |
| 4. Produce shareable accountability report | Coach/team/funded review | Show proof without raw data dump | Monthly/after incidents | Sends to mentor/team | Medium | Build now as Markdown/Telegram-ready packet |
| 5. Enforce self-defined risk rules before trading | Impulse after loss, max-loss breach | Stop trading mechanically | Daily/intraday | Will connect account/API after trust | Potentially high | Later/separate decision gate |
| 6. Turn strategy idea into testable hypothesis | New strategy idea | Backtest or falsify hypothesis | Ad hoc | Pays for research/backtest | Medium | Later, only if paid audit users demand |
| 7. Evaluate Telegram/Twitter signal source | Considering paid signal group | Verify channel's real performance | Ad hoc/ongoing | Pays for public channel report | Medium-high but different product | Separate sandbox/product |

## 8. Competition Map

**Current behavior competitors**

| Competitor/substitute | What users use it for | Why they might stay | Why they might switch | What TRA must prove |
|---|---|---|---|---|
| Excel / Google Sheets | Manual P&L, tags, rule notes, charts | Free, flexible, private, familiar | Error-prone, no deterministic source-row audit, hard to repeat | Faster credible report than spreadsheet in <48h |
| Broker CSV/activity statements | Raw truth source | Already available, trusted | Not interpreted against personal rules | Normalize without hiding source evidence |
| TradingView | Strategy tester, charts, export strategy data | Habit, strong charting, strategy workflow | Does not audit executed broker trades against personal risk policy | TRA is post-trade discipline audit, not chart/backtest replacement |
| MetaTrader / MT5 reports | Account history, orders/deals/positions report | Native to FX/CFD workflow | Report is generic, not policy audit | Convert history into rule violation evidence |
| QUIK / MOEX terminals | Russian market trading, exports to Excel/database | Entrenched terminal workflow | Outdated/manual review burden | Support export taxonomy without live integration |
| Notion / paper journal | Reflection and psychology | Low friction, private | No deterministic P&L attribution/source rows | Produce hard evidence, not just notes |
| ChatGPT/Claude | Ad hoc trade review and narrative | Easy and cheap | Cannot be final truth for violations/P&L | Deterministic artifacts and claim guard |

**Direct product competitors**

| Competitor | What users use it for | Why they stay | Why they switch | What TRA must prove |
|---|---|---|---|---|
| TradeZella | Journaling, playbooks/rules, risk tools, analytics | Polished UI, broker imports, education, reporting | May not audit custom written rules with source-row determinism | TRA gives stricter audit report, not another journal |
| TraderSync | Journaling, trade replay, AI coach, backtesting/replay | Broad features, mobile, imports, AI | Feature-rich but not focused on deterministic rule breach evidence | TRA is narrow, faster, evidence-first |
| Tradervue | Import/share trades, reports, community | Established workflow and free tier | Dated or limited; manual import friction | TRA wins on paid incident audit, not broad journaling |
| Edgewonk | Journal, psychology, mistake tracking, Tiltmeter, performance simulator | Strong discipline/psychology positioning | User wants external deterministic audit/report | TRA produces artifact trail and violation P&L |
| TradesViz | All-in-one journal, 600+ stats, AI, simulators, auto-sync | Feature breadth and free plan | Too broad; user needs policy audit | TRA must be sharper, not broader |

**Indirect competitors**

| Substitute | Use | Switch condition |
|---|---|---|
| Prop-firm dashboards | Rule compliance, daily/max loss, payout gates | TRA adds independent post-mortem and personal rules, not replacing firm rules |
| Exchange/broker risk settings | Position/leverage/risk limits | TRA handles personal discipline rules after export; live settings remain platform-owned |
| Trading coaches/mentors | Accountability and interpretation | TRA gives coach evidence packet and saves manual review |
| Telegram groups | Social accountability/signals | TRA is private evidence, not entertainment/community |

**AI-wrapper competitors:** generic LLM review, AI journal assistants, Cypher-like trader coaches. Their weakness is that they can explain and summarize but must not own final violation truth, P&L arithmetic, or source-row traceability.

**Non-consumption:** many traders do nothing after a breach because of shame, laziness, low account size, or belief that "next time I will be disciplined." This is the real default.

**Real enemy:** habit + shame + trust + workflow inertia + messy data + lack of urgency. The product loses if it becomes another dashboard instead of a painful accountability artifact.

## 9. ICP Decision

| ICP | Pain intensity | Ability to pay | Trust/liability requirements | Access path | Fit with current product | Early adopter quality | Verdict |
|---|---|---|---|---|---|---|---|
| Prop/funded-account traders | High | Medium | Need accuracy, privacy, no advice | Prop communities, Discord/Telegram, coaches, warm intros | High | High: explicit rules, frequent exports | **Primary** |
| Active discretionary crypto traders | Medium-high | Medium | Privacy, exchange export support, no live API in v1 | Telegram groups, Twitter/X, communities | Medium | Good if they have written rules | Secondary |
| Retail discretionary traders | Low-medium | Low-medium | Low formal rules, high churn | Social media/courses | Low-medium | Weak: vague discipline | Defer |
| Systematic retail traders | Medium | Medium | Need backtest validity, OOS rigor | TradingView/Python communities | Medium-low | Good but pulls toward backtesting | Secondary/defer |
| Small trading teams | High | Medium-high | Need confidentiality, repeatability, team workflow | Warm intros, local communities | High | Strong if team lead owns process | Secondary |
| Russian trading teams / small funds | Medium-high | Medium-high | Relationship trust, data privacy, local terminal/export quirks | Trader colleague, warm intros, Russian Telegram communities | Medium-high | Strong but access uncertain | Secondary after warm-intro proof |
| Trading coaches / mentors | High | Medium | Need report they can use with students | Coach DMs, paid communities | High | Strong distribution leverage | Secondary/partner |
| Signal-channel subscribers | Medium | Low-medium | Wants public proof; different data | Telegram/crypto communities | Low | Different problem | Defer to signal sandbox |
| Signal sellers / influencers | Low/negative | Medium | Incentive conflict; may dislike audit | Creator outreach | Low | Bad early adopter | Reject for TRA |

**Primary ICP:** prop/funded-account traders who already have written risk rules and can export trade history.

Justification: they have explicit external rules, painful consequences, repeat review cadence, and a reason to care about max daily loss/drawdown/cooldown evidence. This ICP also forces the product to stay deterministic and source-traceable. Broad retail will praise the idea and not pay; signal subscribers are a separate product; live risk guard users introduce too much liability for v1.

## 10. First 10 Customers Plan

**Where to find prospects**

- Trader colleague's warm network first: prop/funded traders, crypto/futures scalpers, small Russian/RU-speaking teams, coaches.
- Telegram/Discord groups where funded-account rules, payout denials, daily drawdown, overtrading, revenge trading are discussed.
- Coaches/mentors who already review journals manually.
- Users posting about TradeZella/TraderSync/Edgewonk pricing, journaling fatigue, max daily loss, funded account failures.

**Who founder should contact first**

Start with 20 warm or semi-warm prospects, not strangers: 10 active prop/funded traders, 5 coaches/team leads, 5 active crypto/futures traders with written rules. Do not start with signal sellers or broad retail beginners.

**Outreach sequence**

1. DM with a specific ask: "Я проверяю, платят ли трейдеры за независимый аудит нарушений risk rules по реальному export. Не продаю SaaS. Хочу посмотреть, как ты в последний раз разбирал нарушение max loss/cooldown."
2. 15-minute call about last real breach and current workflow.
3. Ask for anonymized 30-90 day export + written rules.
4. Offer paid manual audit: one report within 48-72 hours.
5. Review report live, ask user to challenge source rows and attribution.
6. Ask for next audit date or referral only after payment/report review.

**What not to automate**

Do not automate onboarding, broker import, Telegram bot delivery, public dashboard, payment funnel, strategy parsing, or signal analytics. The founder needs to hear objections directly.

**First call must test**

- Did they have a real recent costly violation?
- Do they already track rules in a concrete way?
- Can they export data quickly?
- Are they willing to show data despite shame/privacy?
- Do they pay for trading tools/coaching now?
- Would an evidence report change behavior, coach review, payout preparation, or team accountability?

**Success**

- 10 qualified calls in 14 days.
- 5 real exports + written rules.
- 3 prepaid or paid audit reports.
- At least 2 users schedule a second audit.
- At least 1 coach/team lead asks for multi-trader package.

**False-positive enthusiasm**

- "Крутая идея" but no export.
- Wants live blocking only.
- Wants strategy generator/backtest instead.
- Sends screenshots but no trade history.
- Refuses payment but asks to be notified when SaaS exists.
- Wants Telegram signal analytics, not own-trade audit.

**10 discovery questions about past behavior**

1. Когда ты в последний раз нарушил свое risk rule? Что именно произошло по времени и сделкам?
2. Как ты понял, что правило было нарушено: терминал, spreadsheet, журнал, prop dashboard, ощущение после факта?
3. Сколько денег, payout, account status или времени это стоило?
4. Где были записаны правила до нарушения: документ, Notion, sheet, чат, память?
5. Когда ты последний раз экспортировал сделки? Из какого терминала/брокера и в каком формате?
6. Как ты сейчас ведешь journal: TradeZella/TraderSync/Edgewonk/Excel/Notion/ничего? Что платишь сейчас?
7. Как ты проверяешь max daily loss, max drawdown, cooldown после loss или position size?
8. Что ты сделал после последнего нарушения: остановился, уменьшил размер, показал кому-то отчет, проигнорировал?
9. Что мешало показать сделки coach/team/friend: стыд, приватность, messy export, отсутствие формата?
10. Какой последний отчет/скрин/журнал ты показывал coach/team/prop support? Что они сказали, чего не хватало?

## 11. MVP / Pilot Test

**Decision:** первый pilot должен быть **A. manual trade/risk audit report**.

Почему не B: автоматизированный CLI уже есть, но продавать надо outcome, а не tool. Почему не C: Telegram-ready delivery полезен как упаковка, но не core value. Почему не D: live risk guard преждевременен и рискован. Почему не E: backtesting - другой buying trigger.

**Core pilot promise**

"Пришли trade export и written risk rules. За 48-72 часа получишь audit report: какие правила нарушены, source rows/timestamps, repeated patterns, worst days, violation-attributed P&L, limitations, next-review checklist. Это не investment advice и не live control."

**What is manually concierge**

- Prospect qualification.
- Export intake and anonymization.
- Mapping user's rule text into policy schema.
- Resolving ambiguous columns/rules.
- Report review and delivery.
- Payment, follow-up, and objection logging.

**What must be productized**

- Deterministic importer for most common pilot exports.
- Explicit policy schema.
- Source-row traceability.
- Violation records.
- Reconciled attribution.
- Markdown report.
- Claim guard/disclaimer.
- Manifest and local retention/delete.

Эти pieces уже mostly implemented in repo. Do not rebuild them.

**What must be cut**

Live broker/exchange API, order blocking, Telegram sending bot, public SaaS, dashboard, mobile app, signal parsing, AI rule truth, strategy generator, backtest workbench, private group scraping.

**2-week validation sprint**

- Days 1-2: compile 50 prospects, prioritize 20 warm/semi-warm.
- Days 2-5: 10 calls, no product demo before past-behavior questions.
- Days 3-7: collect 5 exports + written rules.
- Days 5-10: deliver 3 paid manual reports.
- Days 10-14: live report review, collect disputes, ask for second audit/referral.

**6-week concierge pilot**

- Week 1-2: first 3 paid reports.
- Week 3-4: repeat audits for same users; refine rule taxonomy/export taxonomy.
- Week 5: coach/team package test.
- Week 6: decide productization based on repeat payment and data normalization pain.

**Behavioral success metrics**

- 50%+ of qualified prospects provide real export/rules.
- 30%+ pay for first audit.
- 50%+ of paid users review report live.
- 30%+ request or schedule repeat audit.
- 20%+ refer another trader/coach.

**Payment test**

Take payment before or immediately after data intake. Free sample can be one anonymized example, not a full free audit.

**Retention test**

Ask for second audit at 2-4 week interval. Retention is not opening a dashboard; retention is sending new export/rules and paying again.

**Referral test**

Ask: "Кому еще ты показывал этот report or who else has this exact problem?" Referral without prompt is strongest.

**Kill criteria**

- <3 paid reports from 10 qualified prospects.
- <5 real exports/rules from 10 qualified prospects.
- >2 major attribution disputes in 5 audits.
- No repeat audit scheduled after 6 weeks.
- Most demand is for live blocking/backtesting/signal analytics rather than audit.

## 12. Next Development Phases

### Phase A: No-code / no-build validation

- **Objective:** prove paid pain before more engineering.
- **Why now:** code is ahead of market evidence.
- **Scope in:** interviews, manual mock report, payment ask, export/rule collection.
- **Scope out:** all new code, UI, broker API, Telegram bot, signal analytics.
- **Entry criteria:** current repo baseline accepted; founder has prospect list.
- **Exit criteria:** 10 qualified calls, 5 exports/rules, 3 paid reports or explicit failure.
- **Main artifacts:** call notes, objection log, anonymized workflow examples, payment receipts.
- **Engineering tasks:** none.
- **Validation tasks:** past-behavior discovery, payment ask, data access test.
- **Risks:** founder hides behind building; prospects praise but do not pay.
- **Kill/pivot criteria:** fewer than 3 paid reports from 10 qualified prospects.

### Phase B: Manual audit report pilot

- **Objective:** deliver audit value manually while using existing deterministic pieces only where helpful.
- **Why now:** tests core assumption with real inputs.
- **Scope in:** manual normalization, manual policy mapping, generated Markdown report, Telegram-ready copy if requested.
- **Scope out:** product UI, self-service, broker sync, strategy/backtest, live lockout.
- **Entry criteria:** at least 3 prospects agree to paid/manual audit.
- **Exit criteria:** 3 paid reports delivered; each reviewed with user.
- **Main artifacts:** audit report, source-row mapping notes, user dispute log.
- **Engineering tasks:** only bug fixes needed to complete paid reports; no feature expansion.
- **Validation tasks:** report usefulness, attribution trust, WTP, privacy objections.
- **Risks:** report looks impressive but does not change behavior.
- **Kill/pivot criteria:** users do not pay, do not review, or do not request repeat.

### Phase C: Trader workflow and export taxonomy

- **Objective:** learn which exports/rules actually appear in pilots.
- **Why now:** scale risk is importer mess, not evaluator code.
- **Scope in:** broker/terminal/export taxonomy, rule taxonomy, timezone/session patterns, Russian terminal notes.
- **Scope out:** broad broker integration library.
- **Entry criteria:** 5 real exports across at least 2 platforms.
- **Exit criteria:** top 2-3 export formats and top 6-10 rule patterns documented.
- **Main artifacts:** export taxonomy doc, rule taxonomy doc, unsupported-data list.
- **Engineering tasks:** small parser adjustments only after repeated demand.
- **Validation tasks:** measure cleanup time per audit.
- **Risks:** every user needs custom cleanup.
- **Kill/pivot criteria:** average normalization >2 hours per audit with no willingness to pay for concierge.

### Phase D: Minimal import + policy schema engineering

- **Objective:** automate only repeated manual work.
- **Why now:** paid reports reveal repeated formats/rules.
- **Scope in:** local-first CLI, deterministic CSV import, explicit policy schema, review packet, artifact manifest.
- **Scope out:** SaaS onboarding, OAuth, live broker credentials, AI-owned rule mapping.
- **Entry criteria:** repeated export/rule patterns from paid pilots.
- **Exit criteria:** same audit can be rerun deterministically with stable hashes.
- **Main artifacts:** normalized trades, approved policy YAML, review packet, manifest.
- **Engineering tasks:** support top repeated export formats, improve validation errors, local retention/delete.
- **Validation tasks:** operator time saved, user trust in source-row evidence.
- **Risks:** overbuilding generic importer.
- **Kill/pivot criteria:** no repeated formats/rules after 10 audits.

### Phase E: Deterministic rule evaluation + attribution

- **Objective:** make violation truth and P&L attribution defensible.
- **Why now:** this is the actual differentiated asset.
- **Scope in:** max daily loss, max drawdown, cooldown, max position size, forbidden assets, leverage warnings, violation-attributed P&L, claim guard.
- **Scope out:** counterfactual returns, causal-loss claims, strategy adherence without approved deterministic mapping.
- **Entry criteria:** users have explicit rules and disputes from pilots are understood.
- **Exit criteria:** users accept source-row evidence and attribution assumptions in review.
- **Main artifacts:** violations JSON, attribution summary, report sections, golden fixtures.
- **Engineering tasks:** evaluator coverage only for validated rule types; regression tests.
- **Validation tasks:** ask users to challenge each violation row.
- **Risks:** P&L attribution gets disputed or overclaims causality.
- **Kill/pivot criteria:** material attribution disputes in >30% paid reports.

### Phase F: Telegram-ready delivery, only if pilots demand it

- **Objective:** deliver where traders already communicate without changing core product.
- **Why now:** only if users actually forward/review reports in Telegram.
- **Scope in:** copyable Telegram summary, report path, limitations, disclaimer.
- **Scope out:** bot sending, private group scraping, signal parsing, Telegram auth.
- **Entry criteria:** >50% pilot users ask to receive/share summary in Telegram.
- **Exit criteria:** Telegram packet improves review/referral behavior.
- **Main artifacts:** delivery packet text, character-limit tests.
- **Engineering tasks:** deterministic formatting only.
- **Validation tasks:** track whether packet gets shared with coach/team.
- **Risks:** Telegram UX becomes signal analytics scope creep.
- **Kill/pivot criteria:** users still prefer PDF/Markdown or Telegram requests are about signal channels.

### Phase G: Repeatable concierge packaging

- **Objective:** turn paid manual audit into repeatable offer.
- **Why now:** after 3-5 successful paid audits.
- **Scope in:** offer page, intake checklist, data handling promise, pricing, report SLA.
- **Scope out:** self-service SaaS, subscriptions without repeat evidence.
- **Entry criteria:** 3 paid audits and at least 1 repeat intent.
- **Exit criteria:** 5-10 paid audits delivered with predictable operator time.
- **Main artifacts:** offer one-pager, intake form, sample anonymized report, privacy note.
- **Engineering tasks:** reduce operator time, not add features.
- **Validation tasks:** pricing, objection handling, coach/team package.
- **Risks:** service business without software leverage.
- **Kill/pivot criteria:** unit economics fail at prices users accept.

### Phase H: Live risk guard decision gate

- **Objective:** decide whether live lockout is separate product, not sneak it into v1.
- **Why now:** only after audit users repeatedly demand pre-trade enforcement and pay for audit.
- **Scope in:** research-only, liability memo, read-only monitoring concept, API permission model, security gates.
- **Scope out:** order blocking, trade execution, broker credentials in product, kill switch implementation.
- **Entry criteria:** at least 5 paying audit users explicitly ask for live prevention and accept read-only first.
- **Exit criteria:** legal/security/product decision: reject, defer, separate product, or read-only monitor pilot.
- **Main artifacts:** ADR, liability memo, API risk map, user demand evidence.
- **Engineering tasks:** none until separate approval; maybe read-only paper prototype.
- **Validation tasks:** paid pre-order for read-only monitoring, not blocking.
- **Risks:** false sense of safety, missed block, false block, trading-loss liability.
- **Kill/pivot criteria:** users require trade permissions before trust/legal gates.

### Phase I: Expansion or split-product decision

- **Objective:** choose next product path after evidence.
- **Why now:** prevent contamination from backtesting/signal/live-control ideas.
- **Scope in:** compare paid evidence for audit, signal sandbox, hypothesis bridge, live guard.
- **Scope out:** merging all ideas into one platform.
- **Entry criteria:** 6-week pilot data.
- **Exit criteria:** continue TRA, split product, pivot, or stop.
- **Main artifacts:** pilot evidence review, decision log, roadmap update.
- **Engineering tasks:** only after decision.
- **Validation tasks:** compare revenue, retention, referral, trust, implementation risk.
- **Risks:** founder follows most exciting feature instead of strongest paid behavior.
- **Kill/pivot criteria:** audit lacks repeat payment; adjacent wedge shows stronger paid behavior in separate validation.

## 13. Pricing And Offer Test

Не использовать TAM/SAM/SOM. Use competitor pricing only as analogs: TradeZella/TraderSync paid tiers are around journal subscription behavior; Edgewonk lists $197/year; Tradervue has free/import-limited and paid tiers; TradesViz has free + paid all-in-one positioning. These are not proof of TRA pricing, only anchors.

| Offer | Price range | Included | Excluded | Validating payment behavior | Killer objections |
|---|---:|---|---|---|---|
| One-time manual audit report | $49-$149 | One export period, written rules mapping, violation report, P&L attribution, limitations, review call | Ongoing journal, live API, backtest, strategy advice, Telegram signal analytics | User prepays or pays before delivery; sends export/rules within 24h | "I can do this in my journal", refuses data, wants free sample only |
| Monthly accountability audit | $99-$299/month | 2-4 audits/month, repeated patterns, month-over-month discipline trend, Telegram-ready summary | Live blocking, full dashboard, broker sync | User schedules next audit and pays month 2 | No second export, no behavior change, report not opened/shared |
| Team/coach package | $300-$1,000/month concierge | 3-10 traders, standardized rule policy, per-trader reports, coach/team summary | Enterprise compliance, SaaS seats, institutional SLAs | Coach/team lead pays for multiple traders after pilot | Privacy blocks exports, rules too vague, team wants full platform before paying |

## 14. Final Recommendation

**What to do this week**

- Stop product expansion.
- Contact 20 warm/semi-warm prospects.
- Run 10 past-behavior calls.
- Ask for real export + written rules.
- Sell 3 one-time manual audits at $49-$149.
- Deliver with current local-first deterministic workflow and manual operator review.
- Track every objection in a simple evidence log.

**What to stop doing**

- Stop building features before paid reports.
- Stop discussing live broker/API lockout as v1.
- Stop merging Telegram signal analytics into TRA.
- Stop pitching "AI trading strategy/backtest generator."
- Stop optimizing CLI/importer until real exports force it.

**What to build next only after validation**

- Support the top repeated export formats from paid pilots.
- Improve policy review packet for common rule wording.
- Add only validated rule types.
- Improve report packaging if users actually share it with coach/team/Telegram.
- Add repeat-audit workflow artifacts, not SaaS dashboard.

**Single metric deciding whether project advances**

3 paid audit reports from 10 qualified prospects within 14 days, followed by at least 2 repeat audit commitments within 30 days.

**Most dangerous founder trap**

Confusing technical correctness with market pull. The repo is already good enough to test the business; every extra feature before payment evidence is avoidance.

## 15. Sources

External sources used for current market, competitor, pricing, workflow, risk, and compliance claims:

1. TradeZella pricing/features and explicit "not a brokerage" positioning: https://www.tradezella.com/pricing
2. TradeZella trading journal feature positioning: https://www.tradezella.com/trading-journal
3. TraderSync pricing/features, replay, AI coach, backtesting positioning: https://tradersync.com/pricing/
4. Edgewonk pricing and feature list including risk/mistake/discipline analytics: https://edgewonk.com/pricing
5. Tradervue trade import quota and manual import constraints: https://app.tradervue.com/help/quota
6. Tradervue supported brokers/platforms and import limitations: https://app.tradervue.com/help/brokers
7. TradesViz pricing, free plan, AI analytics/simulators/auto-sync positioning, not investment advisor disclaimer: https://www.tradesviz.com/pricing/
8. TradingView official strategy data export docs: https://www.tradingview.com/support/solutions/43000613680-how-to-export-strategy-data/
9. MetaTrader 5 official trading report/history docs: https://www.metatrader5.com/en/terminal/help/trading_advanced/history_report
10. FTMO official trading objectives/max daily loss/max loss rules: https://ftmo.com/en/trading-objectives/
11. Bybit official risk limit documentation: https://www.bybit.com/en/help-center/article/Risk-Limit-Inverse-Contract
12. Moscow Exchange terminal docs, Excel/database export and risk parameters: https://www.moex.com/a1530
13. Investor.gov definition of investment adviser: https://www.investor.gov/introduction-investing/getting-started/working-investment-professional/investment-advisers
14. CFTC automated trading risk controls and safeguards concept release: https://www.cftc.gov/PressRoom/PressReleases/6683-13
15. FINRA algorithmic trading supervision/control topic page: https://www.finra.org/rules-guidance/key-topics/algorithmic-trading
16. Interactive Brokers API software license risk/liability language: https://interactivebrokers.github.io/
17. SignalBlink Telegram signal performance analytics positioning: https://www.signalblink.com/
18. Telemetrio Telegram analytics pricing and channel analytics positioning: https://telemetr.io/en/pricing
19. X API enterprise pricing/custom pricing dependency: https://docs.x.com/enterprise-api/getting-started/pricing
