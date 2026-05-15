# Signal Analytics Sandbox Startup Pressure Test

Дата: 2026-05-07
Режим: deep/full
Язык: русский
Scope: только чтение репозитория, рыночный research и стратегический pressure test. Продуктовый код, roadmap и инженерные документы не изменялись.

## 1. Verdict

**Build pause required.**

`Public signal-source historical audit report` выглядит как реальная платная wedge, но не как продукт, который сейчас надо дальше автоматизировать. Боль существует, прямые конкуренты уже обещают `Telegram channel -> verified stats`, а значит “киллер фича” не уникальна; выигрыш возможен только через доверие, воспроизводимость, юридическую аккуратность и ручную точность. Самый правильный следующий шаг: остановить расширение, продать 3-10 ручных публичных audit reports, проверить платеж и только потом доделывать workflow automation. Telegram-first важен как delivery/package для пилотов, но не оправдывает Telegram bot как первичный продукт сейчас.

## 2. Strategic Reframe

**Что это на самом деле.** По репозиторию Signal Analytics Sandbox - это не “бот для сигналов”, а локальный evidence-backed due-diligence инструмент: оператор берет публичный источник, фиксирует capture/provenance, вручную или rule/LLM-draft извлекает сигналы, утверждает ledger, матчится с историческими OHLCV snapshot и выпускает Markdown audit report. Внутренняя архитектура уже жестко выбрала deterministic core, public-source-only границы, human review, snapshot immutability, non-advice disclaimer и отсутствие Entropy Core contamination.

**Что это не.** Это не Telegram scraper, не private group monitor, не copy-trading, не signal marketplace, не публичный leaderboard, не broker integration, не инвестиционный совет, не full backtester и не Entropy Core research feed.

**Что в комментариях трейдера совпадает с текущим продуктом.**

- “Я указываю Telegram channel или Twitter/X аккаунт, и мне выдает его торговую стату по сигналам” - совпадает с promise, но не обязательно с UX “сам указал и мгновенно получил”.
- “Или график доходности” - совпадает, если это историческая equity-style series с caveat “без комиссий/проскальзывания/position sizing”, а не обещание доходности.
- “Пользователь загружает ссылку на инфлюенсера, бот выдает инфу” - совпадает как конечная упаковка, но не как текущий MVP.
- “Только она должна быть в Telegram” - важный delivery insight: отчет лучше приносить туда, где трейдер уже живет, но это не доказывает, что нужно строить Telegram bot до paid pilots.

**Что комментарии трейдера тянут в отдельный продукт.** Telegram bot с self-serve link ingestion, continuous tracking, source rankings, leaderboard, private channel access и публичными “reliability ratings” - это уже отдельный SaaS/bot/marketplace risk surface. Его нельзя смешивать с текущим local-first audit sandbox без новых legal, trust, support и data-access gates.

**Что нельзя строить сейчас.** Нельзя строить private Telegram scraping, paid X API dependence, public SaaS, marketplace, copy trading, broker integration, live execution, influencer leaderboard, automated publishing, OCR, LLM-owned final signal truth и Entropy Core feed. Нельзя строить еще extraction infrastructure до продажи ручных отчетов.

**Самая сильная узкая wedge.** Ручной независимый отчет “Стоит ли платить за этот публичный signal source?” для человека, который уже рассматривает платную подписку или уже платит и сомневается.

## 3. Scorecard

| Area | Score | Evidence |
|---|---:|---|
| Pain intensity | 4/5 | Пользователи обсуждают платные signal groups, fake screenshots, удаленные/отредактированные сообщения и невозможность понять track record до подписки; SignalBlink и SignlyAnalytics прямо продают эту боль. |
| Buyer clarity | 3/5 | Лучший buyer - потенциальный/текущий subscriber платного канала; signal sellers и команды возможны, но хуже по incentives. |
| Urgency | 3/5 | Urgency есть перед платежом $50-300/мес за канал или после убытков, но для многих это curiosity и entertainment. |
| Differentiation | 2/5 | Прямые конкуренты уже обещают AI extraction, OHLCV evaluation, leaderboard, PDF/reports и Telegram monitoring. SAS дифференцируется не идеей, а audit discipline: provenance, deterministic matching, human review, disclaimers. |
| Speed to validate | 5/5 | Можно валидировать без кода: взять 3 публичных Telegram sources, вручную извлечь 30-50 сигналов, сделать Markdown/PDF report и попросить оплату. |
| Founder advantage | 3/5 | Техническая сила в deterministic audit architecture; слабость - риск уйти в инженерку раньше продаж. |
| Trust/legal risk | 2/5 | Telegram/X ToS, reputational/defamation risk, ambiguity of signals, edited/deleted posts и AI scraping restrictions делают риск высоким. |
| Engineering scope risk | 2/5 | Repo уже содержит много core modules, но CLI workflow остается stubbed; следующий шаг легко распухнет в bot/SaaS/parser platform. |
| Distribution access | 2/5 | Нужны теплые интро в trading communities; cold outreach к crypto/forex Telegram users тяжелый и недоверчивый. |
| Retention potential | 2/5 | One-off due diligence сильнее, чем recurring; retention появится только если пользователи регулярно покупают/проверяют источники или teams мониторят текущие подписки. |
| Fit with current product workspace | 4/5 | Текущий workspace правильно отделен от Entropy Core/Trader Risk Audit и подходит под public-source audit, если не расширять его в marketplace/bot. |

## 4. Wedge Comparison

### 1. Manual Public Signal Audit Report

- User: человек, который собирается купить платный signal group; текущий subscriber; small due-diligence user.
- Pain: “я не знаю, реальны ли прошлые сигналы, не хочу платить/терять деньги на фейке”.
- Current workaround: листает Telegram history, сверяет старые calls на TradingView, смотрит скриншоты, спрашивает в чатах, ведет Excel.
- WTP likelihood: medium-high, если платеж за группу или potential loss заметен; low, если это просто любопытство.
- Sales difficulty: medium; нужно доверие и sample report.
- Engineering complexity: low; можно делать concierge.
- Legal/ToS/reputation risk: medium; публичные captures, аккуратные citations, no advice, no defamation language.
- Fit with current product workspace: very high.
- Fastest validation test: вручную продать 3 отчета по одному публичному Telegram source за фиксированный fee.
- Verdict: **build now as manual service; no more automation yet**.

### 2. Telegram-First Signal Analytics Bot

- User: Telegram-native trader, который не хочет выходить из мессенджера.
- Pain: “хочу кинуть ссылку и получить summary/report прямо в Telegram”.
- Current workaround: пересылка ссылок друзьям, ChatGPT/Claude, ручной поиск, Telegram bots для summaries.
- WTP likelihood: medium, но риск free-bot expectations высокий.
- Sales difficulty: medium-low для trial, high для payment.
- Engineering complexity: medium-high: bot UX, auth, queue, source capture, billing, abuse handling.
- Legal/ToS/reputation risk: high; bot может подтолкнуть к automated capture и private-channel requests.
- Fit with current product workspace: medium as delivery layer, low as primary product.
- Fastest validation test: отправлять готовый Markdown/PDF report вручную в Telegram и смотреть, читают ли/платят ли.
- Verdict: **validate as delivery, defer as product**.

### 3. Automated Public Telegram/X Source Parser

- User: founder/operator, analyst, power user.
- Pain: manual extraction slow.
- Current workaround: ручной extraction, regex, export, TG parser APIs, LLM prompts.
- WTP likelihood: indirect; users pay for outcome report, not parser.
- Sales difficulty: high if sold alone.
- Engineering complexity: high due to ambiguity, edits, multi-language posts, source formats, rate limits.
- Legal/ToS/reputation risk: high; Telegram content licensing restricts scraping/aggregation for AI, X has strict API/content distribution policy.
- Fit with current product workspace: medium only after manual bottleneck is proven.
- Fastest validation test: measure operator minutes per approved signal in 3 paid reports.
- Verdict: **defer until manual extraction is bottleneck**.

### 4. Signal Seller Verification Report

- User: signal seller/influencer who wants credibility.
- Pain: “подписчики не верят моим скриншотам”.
- Current workaround: screenshots, public Telegram posts, Myfxbook/FX Blue if they have real trading account, testimonials.
- WTP likelihood: medium for honest sellers; low for sellers whose edge is marketing opacity.
- Sales difficulty: high; negative report creates conflict.
- Engineering complexity: low-medium if manual.
- Legal/ToS/reputation risk: medium-high; seller may dispute methodology and public wording.
- Fit with current product workspace: medium.
- Fastest validation test: offer paid private verification to 5 sellers, require permission to share summary.
- Verdict: **validate later; secondary ICP**.

### 5. Signal Subscriber Due-Diligence Report

- User: person considering a paid group or already subscribed.
- Pain: “не хочу платить за garbage / хочу decide stay or cancel”.
- Current workaround: ask Discord/Reddit, inspect history, use free trial, small account/demo following.
- WTP likelihood: highest among listed wedges if decision has immediate cost.
- Sales difficulty: medium.
- Engineering complexity: low if concierge.
- Legal/ToS/reputation risk: medium.
- Fit with current product workspace: very high.
- Fastest validation test: “send me the public channel you are considering; I will audit last 50 extractable calls”.
- Verdict: **primary wedge**.

### 6. Public Influencer Leaderboard

- User: broad retail traders browsing “best signal providers”.
- Pain: comparison and discovery.
- Current workaround: MQL5 rankings, eToro/ZuluTrade, Telegram lists, Reddit, Google, influencer rankings.
- WTP likelihood: low from users; monetization drifts to ads/affiliate/sellers.
- Sales difficulty: high due to trust and cold traffic.
- Engineering complexity: high: continuous ingestion, normalization, disputes, SEO, moderation.
- Legal/ToS/reputation risk: high; defamation and platform data rights.
- Fit with current product workspace: low.
- Fastest validation test: landing page waitlist is weak; better test is whether paid report buyers ask for comparison after first report.
- Verdict: **defer/reject now**.

### 7. Signal Marketplace

- User: subscribers and signal sellers.
- Pain: discovery, subscription, payments, trust.
- Current workaround: MQL5, eToro, ZuluTrade, Telegram paid channels, Whop-like communities.
- WTP likelihood: possible, but chicken-and-egg.
- Sales difficulty: very high.
- Engineering complexity: very high.
- Legal/ToS/reputation risk: very high; can become investment advice/copy trading/affiliate conflict.
- Fit with current product workspace: very low.
- Fastest validation test: none worth doing before audit demand.
- Verdict: **reject for this workspace; separate product only after evidence**.

### 8. Copy-Trading / Execution Product

- User: passive trader who wants trades copied.
- Pain: no time/skill to trade.
- Current workaround: MQL5 Signals, eToro CopyTrader, ZuluTrade, brokers, MT5 copiers.
- WTP likelihood: known market, but crowded and regulated/liability-heavy.
- Sales difficulty: high.
- Engineering complexity: very high.
- Legal/ToS/reputation risk: very high.
- Fit with current product workspace: zero.
- Fastest validation test: irrelevant to SAS.
- Verdict: **reject**.

### 9. Entropy Core Research Input Feed

- User: Entropy operator/researcher.
- Pain: public signals might inspire hypotheses.
- Current workaround: manual research notes.
- WTP likelihood: none externally.
- Sales difficulty: none; internal temptation.
- Engineering complexity: medium.
- Legal/ToS/reputation risk: high if contaminated as evidence.
- Fit with current product workspace: explicitly forbidden.
- Fastest validation test: not needed.
- Verdict: **reject for now; no Core contamination**.

## 5. Core Assumption

**The business works only if traders who are about to pay for or cancel a signal source will pay now for an independent, evidence-backed historical audit and will trust a caveated deterministic report enough to change behavior.**

| Assumption | Why it matters | Evidence currently available | Fastest test | Disconfirming signal | Decision if false |
|---|---|---|---|---|---|
| 1. Buyers pay for due diligence, not just click curiosity | Without payment, this is content/SEO, not product | Direct competitors price from $9.99 credits to $49-99/mo; Reddit users discuss verification pain | Offer $99-299 manual audit before building more | 20 prospects ask for free sample but 0 pay/deposit | Stop automation; pivot to seller-funded verification or kill |
| 2. Public posts contain enough extractable calls | If public sources are mostly vague, stats will be mostly exclusions | Repo supports ambiguity flags; competitor claims AI extraction, but that is marketing | Manually extract 50 posts from 3 pilot sources | <30% posts yield defensible signal records | Narrow to sources with explicit format or pivot to seller-submitted ledgers |
| 3. Deterministic outcome rules are accepted | If users dispute every fill/TP/SL rule, trust collapses | Repo has rule registry and snapshot provenance; forums mention execution/slippage disputes | Show methodology before payment and ask for objections on past examples | Users reject report because “real entries were different” | Report only “source clarity/integrity” or require seller-defined rules |
| 4. Subscriber is better buyer than seller | Sellers resist negative third-party audits; subscribers have immediate avoidance pain | Signal sellers benefit from opacity unless honest; users complain about fake claims | Sell first 10 to prospective/current subscribers, then test sellers | Only sellers engage, subscribers do not pay | Reframe as private seller verification, not public buyer tool |
| 5. Telegram delivery matters less than trust/report quality in first pilot | Building bot early burns scope | Trader colleague says Telegram-first matters; Telegram analytics bots are common | Deliver reports manually in Telegram chat/PDF and ask what they actually opened | Prospects refuse non-Telegram delivery or do not read PDFs | Add Telegram delivery wrapper after paid report, not before |

## 6. Fatal Flaws

| Risk | Severity | Why it matters | Evidence to seek | Fast test | Kill/pivot threshold |
|---|---|---|---|---|---|
| Users may be curious but unwilling to pay | High | “Is this guru legit?” generates clicks, not necessarily revenue | Deposits, paid calls, paid report orders | Ask for payment before report production | <3 paid/committed reports from 20 qualified prospects |
| Signal-channel subscribers may not trust negative reports | High | A user who wants hope may dismiss the audit as “methodology wrong” | Behavior after receiving negative report | Deliver one negative report privately and see if they cancel/share/refer | Users argue result but do not change decision |
| Signal sellers may resist third-party audits | High | Honest sellers are rare; opaque sellers have no incentive | Seller willingness to provide source rules and public permission | Pitch private verification to 10 sellers | Sellers demand only positive badge or editorial control |
| Public posts may be too ambiguous to extract consistently | High | Vague entries, zones, “hold”, “layer in”, edits and screenshots make deterministic ledger weak | Extraction coverage and ambiguity rate | Manual extraction over 150 posts | <30-40 approved/evaluable records per source |
| Outcome matching may be disputed | High | Intra-candle order, stop/target sequence, spread, partial TP and missing entry create disputes | Objections to rule registry | Show per-signal rule examples before sale | >50% of prospects reject methodology as unfair |
| Private groups are where valuable signals live, but are out of scope | High | Paid/private channels may hold “real” calls while public channel is marketing | Prospect source requests | Track requested sources | >60% of paid-intent requests require private/paywalled access |
| Public Telegram/X capture may create ToS/legal/reputation risk | High | Telegram content licensing restricts scraping/aggregation and AI use; X restricts content redistribution | Legal review per source and capture method | Update SAS-002 for each pilot source | Legal memo blocks target sources or forbids report evidence format |
| Paid X API or data providers may destroy unit economics | Medium | X moved to pay-per-use; historical access costs can be unpredictable | Cost per report by source | Produce one X-source cost model before enabling X | API/data cost >25% of pilot price |
| Telegram-first UX may pull product into bot/SaaS too early | Medium | Bot requires auth, billing, queue, abuse handling and may invite private source requests | Delivery preference versus paid behavior | Send manual reports via Telegram first | Users pay only for bot automation, not report |
| Founder may build extraction infrastructure before selling manual reports | Critical | This is the most likely failure mode in this repo: good engineering masks unvalidated demand | Time spent selling vs building | 14-day no-code sales sprint | No paid calls because time went to code |

## 7. Problem Reality

**Exact painful moment.** A trader is about to pay for a Telegram/X signal source, renew a subscription, or follow a public influencer with real capital, but the only available evidence is screenshots, public wins, testimonials and messy historical posts.

**Who feels it most sharply.** People considering paid signal groups and current subscribers who have already lost money or suspect cherry-picking. Prop/funded-account traders may feel it if signals threaten account rules, but they are better served by Trader Risk Audit unless they specifically buy external signals.

**What they do today.** They manually scroll Telegram history, check old calls on TradingView, ask Reddit/Discord, look for Myfxbook/FX Blue/Kinfo verification, follow free signals on demo, compare screenshots, use ChatGPT/Claude to summarize, or simply avoid paid groups.

**Workaround cost.** Time, missed context, false confidence, paying $50-300/mo for a weak source, and potentially trading losses. The strongest paid moment is before paying for a group or immediately after a loss, not casual browsing.

**Painkiller or vitamin.** For broad crypto retail: mostly vitamin/curiosity. For someone about to pay or who was burned: painkiller if report can be delivered fast and credibly.

**Behavior proving urgency.** User pays deposit before report, provides source-of-interest, accepts methodology, reads the report, changes subscribe/cancel decision, and refers another source to audit.

### JTBD Ranking

| JTBD | Trigger | Desired outcome | Frequency | WTP signal | Retention strength | Build now? |
|---|---|---|---|---|---|---|
| 1. Check whether a paid signal source is worth buying | Before subscription/trial expires | Avoid bad paid group | Episodic | Pays one-off audit fee | Low-medium | **Build manually now** |
| 2. Verify whether a public signal source cherry-picks results | Suspicious screenshots/win claims | Expose edits/deletions/hidden losses | Episodic | Pays for integrity flags | Medium if multiple channels | **Build manually now** |
| 3. Produce historical win/loss and equity-style report | Comparing source claims | Get concrete track record | Episodic | Pays for report artifact | Medium | **Build manually now with caveats** |
| 4. Compare several signal sources before subscribing | Choosing among 2-5 groups | Pick least bad option | Episodic | Pays higher comparison fee | Medium | Later, after single-source reports |
| 5. Give a signal seller a credibility report | Seller wants trust/marketing | Shareable proof | Occasional | Seller pays and accepts methodology | Medium | Validate later |
| 6. Track a source continuously over time | Already subscribed | Accountability and alerts | Monthly | Pays subscription | High if real | Later, after report repeat demand |
| 7. Turn public signals into Entropy research hypotheses | Internal research curiosity | Generate ideas | Rare | No external WTP | None | Not yet / reject for Core |

## 8. Competition Map

### Current Behavior Competitors

| Competitor/substitute | What users use it for | Why they might stay | Why they might switch | What SAS must prove |
|---|---|---|---|---|
| Manual Telegram scrolling | Check old posts, claimed wins, comments | Free, native, no trust transfer | Time-consuming, easy to miss edits/deletions | Report saves hours and catches ambiguity |
| TradingView chart replay | Check whether old calls hit target/stop | Familiar chart tool | Manual and inconsistent | Deterministic per-signal table is faster |
| Screenshots/testimonials | Social proof | Easy, emotional, seller-provided | Fake/cherry-picked risk | Evidence references beat screenshots |
| Excel/Google Sheets | Manual tracking | Flexible, cheap | Tedious, no provenance | SAS must provide repeatable ledger + snapshot |
| Free trials/demo following | Observe future calls | Real experience | Slow, can miss historical manipulation | Historical audit accelerates decision |
| Reddit/Discord due diligence | Ask community if source is scam | Social trust | Anecdotal and noisy | Report gives source-specific evidence |
| ChatGPT/Claude manual analysis | Summarize posts | Cheap and fast | Non-deterministic, no price matching | SAS numbers must be reproducible |

### Direct Product Competitors

| Competitor | What users use it for | Why they might stay | Why they might switch | What SAS must prove |
|---|---|---|---|---|
| [SignlyAnalytics](https://www.signlyanalytics.com/) | Telegram channel reliability reports, OHLCV evaluation, integrity flags, scenario/equity analysis | Cheap: $9.99 credits / $19.99 Pro; self-serve | Trust/methodology unknown; may over-automate | Human-reviewed audit is more defensible |
| [SignalBlink](https://www.signalblink.com/) | Automatic Telegram signal tracking, leaderboard, real market data, reports | Strong UX, $49/$99 monthly, free tier | Claims private channel access and automation may scare careful users | Public-only legal posture and evidence rigor |
| [SignalTrack](https://signaltrack.io/) | Crypto Telegram signal provider rankings and large signal database | Breadth and leaderboard | Users may need source-specific private audit | More precise bespoke report |
| BotLedger | Claimed Telegram signal verification | Similar promise | Site unavailable via fetch; trust unclear | SAS must not rely on marketing claims |
| TG Parser style tools | Extract public Telegram data | Developer convenience | Not signal-specific or legally safe by itself | SAS is audit report, not data scraping API |

### Indirect Competitors

| Competitor | What users use it for | Why they might stay | Why they might switch | What SAS must prove |
|---|---|---|---|---|
| [Myfxbook](https://www.myfxbook.com/help/knowledge-base/verification/) | Verified broker-linked account track record | Known verification workflow | Many Telegram signal sellers have no linked account | SAS can audit public calls without broker access |
| [FX Blue](https://api.fxblue.com/live/about-verification) | Broker-synced verified trading results | Direct broker data | Only works when seller exposes account | SAS handles public source evidence |
| [Kinfo](https://kinfo.com/) | Broker-integrated verified trading performance | Strong “data cannot be manipulated” claim | Requires broker integration; not public signal history | SAS covers public influencer posts |
| [MQL5 Signals](https://www.mql5.com/en/signals) | Paid/free copyable signals with prices and reliability | Integrated into MT5 and copy execution | Not Telegram/X influencer due diligence | SAS is pre-subscription audit outside MT5 |
| [eToro CopyTrader](https://investors.etoro.com/news-releases/news-release-details/etoro-brings-copytradertm-us-empowering-investors-trade-smarter) | Copy real investors and view performance history | Integrated broker/social platform | Different asset/user universe; execution product | SAS avoids execution and advice |
| [TradingView Ideas](https://www.tradingview.com/ideas/) | Public ideas, charts, influencer discovery | Massive habit and community | Ideas are not normalized signal ledgers | SAS converts messy posts to auditable ledger |
| Trading journals: [TradeZella](https://help.tradezella.com/en/articles/8911582-our-pricing), [TraderSync](https://tradersync.com/pricing/) | Personal trade tracking and review | Existing trader workflow | They analyze user trades, not influencer calls | SAS audits external source before following |

### AI-Wrapper Competitors

- Telegram summary bots like [QuickRecapBot](https://www.quickrecapbot.com/), [Telepath](https://www.trytelepath.com/) and TeleSummarizer prove users accept Telegram-native summarization, but they summarize conversations, not trading outcomes.
- TG Parser V2 claims public Telegram channel parsing with no login and rate-limit handling. That is a warning: data extraction is becoming commoditized and legally noisy; SAS should sell trust/report decisions, not parser access.
- ChatGPT/Claude with pasted posts is the free/cheap fallback. SAS must beat it with deterministic price matching, provenance and human-approved signal truth.

### Non-Consumption

Many traders simply do not check. They either assume all paid signal groups are scams, follow a friend referral, use tiny size/demo, or decide that verifying old calls is not worth the time. This is dangerous: non-consumption means the market may be smaller than the “everyone complains” surface suggests.

### Real Enemy

The real enemy is **trust plus willingness to pay**, not lack of features. Data ambiguity, legal risk, habit, Telegram-native workflow inertia and low urgency can kill this even if the engineering works.

## 9. ICP Decision

| ICP | Pain intensity | Ability to pay | Trust/legal requirements | Access path | Fit with current product | Early adopter quality | Verdict |
|---|---|---|---|---|---|---|---|
| People considering paying for signal groups | High | Medium | Needs clear no-advice/report caveats | Reddit, Telegram, Discord, referrals | Very high | High: acute decision | **Primary** |
| Active crypto retail traders | Medium | Low-medium | High skepticism, scam-heavy | Crypto Telegram/X communities | Medium | Mixed: noisy | Secondary |
| Prop/funded-account traders | Medium | Medium-high | Need rule/risk integration | Prop communities | Low-medium | Better for Trader Risk Audit | Defer |
| Signal-channel subscribers | High after bad experience | Medium | Need private report and trust | Existing paid/free groups | High if public source | High if currently paying | Secondary |
| Signal sellers / influencers | Medium | Medium-high | Need consent, dispute handling | Direct seller outreach | Medium | Biased incentives | Defer/validate later |
| Trading coaches / educators | Medium | Medium | Reputation sensitive | Warm intros | Medium | Could use reports in education | Secondary later |
| Small trading teams | Medium-high | High | Methodology, retention, confidentiality | Warm network | High if they monitor sources | Good but fewer | Secondary |
| Telegram community admins | Low-medium | Medium | More interested in audience analytics | Admin communities | Low | Not core pain | Reject/defer |
| Market researchers / due diligence users | Medium | Medium-high | Strong provenance needs | Analyst network | High | Good if reachable | Secondary |

**Primary ICP: people considering paying for signal groups.**
They have the cleanest trigger, fastest payment test and strongest fit with public-source-only audit. They do not require seller cooperation, marketplace liquidity, broker integration or private scraping. The product promise should be phrased around a buying decision: “Before you pay this channel, get a public-history audit of what it actually posted.”

## 10. First 10 Customers Plan

This must be manual and non-scalable.

**Where to find first 10 prospects.**

- Warm trader network first: the colleague who gave Telegram-first input, his paid/free Telegram signal users, people who have recently discussed signal groups.
- Reddit threads and communities where users ask “are these signals legit?”: Forex, Forexstrategy, Daytrading, Trading, CryptoCurrency adjacent groups. Do not spam; identify concrete posters asking for due diligence.
- Telegram groups where signal groups are compared, but only through human intro and direct conversation.
- Small trading teams or prop-style communities that already pay for tools and have discipline around review.

**Who founder should contact first.**

1. The trader colleague and 5 people he knows who recently considered or paid for a signal group.
2. 5 traders who can name a specific public channel they considered buying.
3. 5 current subscribers who have doubts and can share the public source link.

**Outreach sequence.**

1. Ask for a 15-minute conversation about the last time they evaluated a signal source.
2. If they have a concrete source, offer a paid manual audit of one public channel over a bounded historical window.
3. Show a one-page sample methodology, not a product demo.
4. Ask for payment/deposit before doing the full report.
5. Deliver privately, preferably in Telegram if that is their normal workflow, then ask what decision changed.

**What not to automate.** No source ingestion, no bot, no Stripe funnel, no leaderboard, no public rankings, no private group access, no X pipeline. Founder should personally feel the extraction pain and sales objections.

**What the first call should test.** Past behavior, not opinions: whether they recently paid, checked history, lost money, trusted screenshots, used Myfxbook/FX Blue/Kinfo, asked friends, and what proof changed their action.

**Success.** 3 paid reports from 10 qualified conversations, with named source-of-interest, upfront payment/deposit, and at least one repeat/referral.

**False-positive enthusiasm.** “Cool idea”, “I would use it”, “send me free report”, “make a bot and I’ll try it”, “I’ll pay once it supports private groups”, “I’ll pay if it finds profitable channels”.

### 10 Discovery Questions

1. Когда вы в последний раз рассматривали платную signal group или инфлюенсера? Какой именно источник?
2. Что вы сделали тогда, чтобы проверить источник перед оплатой?
3. Сколько старых сигналов вы реально просмотрели вручную и сколько времени это заняло?
4. Чем вы сверяли результат старых calls: TradingView, broker chart, Excel, screenshots, Myfxbook/FX Blue, что-то еще?
5. Когда вы в последний раз теряли деньги или subscription fee из-за плохого signal source? Что произошло?
6. За какие signal groups или copy/signal services вы уже платили? Сколько и как долго?
7. Какое доказательство в прошлый раз убедило вас подписаться или отказаться?
8. Насколько вы доверяли Telegram screenshots/result posts? Были ли случаи, когда посты редактировали или удаляли?
9. Делились ли вы когда-нибудь негативным разбором signal source с другими? Где и почему/почему нет?
10. В каком формате вы реально дочитали бы report: Telegram message, PDF/Markdown, spreadsheet, chart screenshot, голосовой summary?

## 11. MVP / Pilot Test

**Выбор: A. manual public-source signal audit report.**

Не B, потому что Telegram bot проверяет UX, а не платеж за audit. Не C, потому что parser/CLI проверяет engineering, а не demand. Не D/E/F, потому что leaderboard, badge, marketplace/copy trading расширяют risk surface до доказательства wedge.

**Core pilot promise.** “За 48-72 часа вы получите независимый исторический audit одного публичного signal source: extractable calls, exclusions/ambiguity, win/loss/timeout, equity-style historical curve where defensible, methodology, evidence links, limitations and no-advice disclaimer.”

**What is manually concierge.**

- Source eligibility review.
- Public capture collection.
- Signal extraction and ambiguity labeling.
- Per-signal review.
- Report delivery and explanation call.
- Objection handling.

**What must be productized.**

- Stable report template.
- Source manifest fields.
- Approved ledger format.
- Deterministic outcome rules.
- Snapshot provenance.
- Disclaimers and limitations.

**What must be cut.**

- Telegram bot.
- X support.
- Private groups.
- Paid APIs unless needed for a paid report.
- OCR/screenshots.
- Leaderboard.
- Seller badges.
- Continuous monitoring.
- LLM as final truth.

### 2-week validation sprint

| Day | Task | Artifact |
|---|---|---|
| 1 | Define one-page offer and methodology | Offer doc + sample report outline |
| 2-3 | Contact 20 qualified prospects manually | Prospect sheet |
| 3-5 | Run 10 calls | Discovery notes |
| 5-7 | Close 3 paid/deposit reports | Payment/deposit log |
| 7-10 | Produce first report manually | Report v1 |
| 10-12 | Deliver and interview | Decision-change notes |
| 12-14 | Decide advance/kill | Pilot memo |

### 6-week concierge pilot

- Week 1: sell first 3 reports.
- Week 2: deliver first 2 reports and measure extraction time.
- Week 3: deliver third report, collect objections.
- Week 4: test comparison report across 2-3 sources with one buyer.
- Week 5: test monitoring/accountability offer with current subscribers.
- Week 6: decide whether to automate ledger/report workflow or kill/pivot.

**Behavioral success metrics.**

- 3 paid reports from 10 qualified conversations.
- At least 70% of paid buyers provide a source within 24 hours.
- At least 2 buyers say the report changed subscribe/cancel/avoid decision.
- At least 1 buyer asks for a second source or refers another trader.
- Operator extraction time falls below a survivable threshold: target <4 hours for 50 extractable posts before automation.

**Payment test.** Deposit upfront. Free reports do not count.

**Retention test.** One buyer pays for a second source or monthly monitoring after seeing first report.

**Referral test.** Two warm intros from buyers without incentive.

**Kill criteria.**

- 0 paid reports after 20 qualified conversations.
- Most prospects require private groups/paywalled content.
- Public sources produce too few defensible signals.
- Buyers reject caveated deterministic reports because they want “profitable channel recommendation”.
- Legal memo blocks target capture/report format.

## 12. Next Development Phases

### Phase A: No-code / no-build validation

- Phase name: No-code / no-build validation.
- Objective: prove paid demand before more engineering.
- Why now: repo already over-invested relative to market evidence.
- Scope in: offer page/doc, sample report skeleton, 20 conversations, payment asks.
- Scope out: all code, bot, parser, SaaS, X API.
- Entry criteria: founder can name 20 reachable prospects.
- Exit criteria: 3 paid/deposit reports with named public source-of-interest.
- Main artifacts: prospect log, discovery notes, payment/deposit log.
- Engineering tasks: none.
- Validation tasks: calls, outreach, source qualification, payment ask.
- Risks: compliments without payment.
- Kill/pivot criteria: <3 paid/committed reports from 20 qualified prospects.

### Phase B: Manual public-source audit reports

- Objective: deliver paid reports manually and learn report format.
- Why now: tests the real value proposition.
- Scope in: public Telegram sources, manual capture, manual extraction, deterministic/careful spreadsheet if needed, Markdown/PDF.
- Scope out: bot, private groups, OCR, auto parser, leaderboard.
- Entry criteria: at least 1 paid/deposit report.
- Exit criteria: 3 delivered reports and documented objections.
- Main artifacts: delivered reports, ambiguity log, extraction time log.
- Engineering tasks: only use existing scripts/modules if they reduce repeated work; no new features unless blocking paid delivery.
- Validation tasks: buyer debrief, decision-change check, referral ask.
- Risks: report takes too long; users dispute method.
- Kill/pivot criteria: delivered reports do not change buyer behavior.

### Phase C: Legal/ToS and reputation-risk memo

- Objective: convert repo SAS-002 from initial memo into source-specific pilot policy.
- Why now: legal/reputation risk is load-bearing.
- Scope in: public Telegram channel capture, X public posts if requested later, quoting/citation policy, retention, takedown/dispute process, no-advice language.
- Scope out: private/access-controlled sources, broad scraping, AI training/aggregation, public accusations.
- Entry criteria: first paid report source selected.
- Exit criteria: memo approves/blocks exact source and report evidence format.
- Main artifacts: updated pilot legal/risk memo or addendum.
- Engineering tasks: none unless memo requires report wording guard.
- Validation tasks: ask buyers if caveats reduce value.
- Risks: memo blocks high-demand sources.
- Kill/pivot criteria: legal posture prevents producing useful report for most requested sources.

### Phase D: Source/capture workflow definition

- Objective: define exactly how operator captures public posts without crossing platform boundaries.
- Why now: capture quality determines trust.
- Scope in: source manifest, capture timestamp, raw-text hash, URL, eligibility verdict, manual export/import process.
- Scope out: automated scraping, Telegram account auth, X paid API, screenshots/OCR.
- Entry criteria: 3 paid reports or source capture repeatedly slows delivery.
- Exit criteria: repeatable capture checklist used in 3 reports.
- Main artifacts: capture SOP, source manifest examples, source eligibility checklist.
- Engineering tasks: wire existing manifest/capture loader only if it saves time.
- Validation tasks: buyer accepts source evidence format.
- Risks: manual capture not trusted or too slow.
- Kill/pivot criteria: buyers require private proof or source data unavailable publicly.

### Phase E: Minimal ledger + manual extraction engineering

- Objective: productize only the repeated manual extraction bottleneck.
- Why now: only after paid reports prove demand and extraction time hurts margin.
- Scope in: local-first CLI/library, public-source-only, operator-supplied captures, manual extraction first, human review before approved ledger.
- Scope out: LLM-owned truth, autonomous ingestion, private scraping.
- Entry criteria: 3 paid reports and extraction time is top bottleneck.
- Exit criteria: approved ledger generated reproducibly for one source.
- Main artifacts: signal ledger, ambiguity log, reviewer approval record.
- Engineering tasks: connect existing modules into operator workflow; keep deterministic ledger.
- Validation tasks: measure time saved and buyer trust.
- Risks: engineering expands into parser platform.
- Kill/pivot criteria: automation does not reduce delivery time or improves speed but not sales.

### Phase F: Deterministic price snapshot + outcome matching

- Objective: make historical outcomes reproducible and defensible.
- Why now: after ledger is real and buyers want numbers.
- Scope in: immutable price snapshots, provider provenance, deterministic rule registry, excluded signals.
- Scope out: real-time feeds, tick/slippage modeling unless paid users demand, paid data by default.
- Entry criteria: approved ledger for paid report.
- Exit criteria: per-signal outcomes reproducible from same ledger/snapshot.
- Main artifacts: price snapshot, outcomes file, rule methodology.
- Engineering tasks: use current `PriceSnapshot`, matcher and aggregator contracts.
- Validation tasks: show methodology to buyers and collect disputes.
- Risks: target/stop ordering and price provider disputes.
- Kill/pivot criteria: buyers reject deterministic assumptions even with caveats.

### Phase G: Markdown report + provenance/claim guard

- Objective: produce the sellable audit artifact.
- Why now: report is the product.
- Scope in: Markdown/PDF-style report, provenance, evidence links, historical-only language, non-advice disclaimer.
- Scope out: public publishing, ratings that imply advice, automated posting.
- Entry criteria: outcomes and summary available.
- Exit criteria: 3 buyers read the report and can explain what decision it supports.
- Main artifacts: report template, limitation section, dispute notes.
- Engineering tasks: use current report generator; add only packaging fixes after paid feedback.
- Validation tasks: format preference, readability, Telegram delivery test.
- Risks: too technical; users ignore caveats.
- Kill/pivot criteria: buyers do not read or act on report.

### Phase H: Telegram-ready delivery, only if pilots demand it

- Objective: deliver reports where users already work.
- Why now: only after paid users ask for Telegram delivery and reports are valuable.
- Scope in: manually send report in Telegram, compact summary message, maybe Mini App/link later.
- Scope out: Telegram bot as primary product, automated capture, private channel ingestion, billing bot.
- Entry criteria: at least 3 paid report buyers prefer Telegram delivery.
- Exit criteria: Telegram delivery increases read/completion/referral rate.
- Main artifacts: Telegram summary format, report attachment format.
- Engineering tasks: none at first; later a thin delivery wrapper if repeated.
- Validation tasks: compare PDF/Markdown/email vs Telegram read behavior.
- Risks: delivery request mutates into bot/SaaS.
- Kill/pivot criteria: Telegram delivery does not improve payment or reading.

### Phase I: Gated LLM/rule extraction, only if manual extraction is the bottleneck

- Objective: reduce extraction time without losing human-approved truth.
- Why now: after manual reports prove paid demand and extraction cost hurts margin.
- Scope in: rule/regex extraction where possible, LLM drafts gated by cost cap and human approval.
- Scope out: AI final truth, OCR, unsupported languages unless paid source demands.
- Entry criteria: manual extraction >50% of delivery time across paid reports.
- Exit criteria: extraction acceptance rate improves and cost per approved record is acceptable.
- Main artifacts: rule templates, LLM eval log, acceptance-rate baseline.
- Engineering tasks: use/extend current rule and gated LLM adapters.
- Validation tasks: buyer trust in “human-approved” process.
- Risks: AI errors damage trust; Telegram ToS AI scraping issue.
- Kill/pivot criteria: LLM drafts create more review burden than they save.

### Phase J: Continuous tracking / bot / leaderboard decision gate

- Objective: decide whether recurring product exists.
- Why now: only after one-off reports repeat or users ask for monitoring.
- Scope in: monthly accountability report, opt-in monitoring of public sources, private buyer dashboard only if paid.
- Scope out: public leaderboard, seller marketplace, private groups, copy trading, automated public claims.
- Entry criteria: at least 3 repeat/monitoring requests from paid users.
- Exit criteria: 3 users pay monthly for monitoring.
- Main artifacts: recurring offer, monitoring requirements, risk memo.
- Engineering tasks: scheduled batch only after legal gate.
- Validation tasks: retention, churn, cancellation reasons.
- Risks: unit economics and legal risk worsen.
- Kill/pivot criteria: users like one-off reports but will not pay monthly.

### Phase K: Expansion or split-product decision

- Objective: choose whether SAS stays audit sandbox, expands, or spawns a new product.
- Why now: after validated usage patterns, not before.
- Scope in: compare subscriber reports, seller verification, monitoring, Telegram bot, leaderboard as separate product options.
- Scope out: merging with Entropy Core, live execution, broker integration unless a new product is explicitly approved.
- Entry criteria: 10 paid customers or 3 recurring users.
- Exit criteria: written decision: keep/narrow/split/kill.
- Main artifacts: expansion ADR/product memo.
- Engineering tasks: none until decision.
- Validation tasks: segment revenue, retention, legal exposure, support burden.
- Risks: founder confuses traction in adjacent market with reason to bloat SAS.
- Kill/pivot criteria: no segment pays repeatedly or legal/support risk exceeds revenue.

## 13. Pricing And Offer Test

Do not treat these as final pricing. These are validation prices anchored against observed analogs: direct Telegram signal analytics tools publish $9.99 credits, $19.99/mo, $49/mo and $99/mo plans; MQL5 signal subscriptions commonly show $30-50/mo with outliers; trading journals sit around $29-49/mo.

| Offer | Price range to test | Included | Excluded | Payment behavior that validates | Objections that kill |
|---|---:|---|---|---|---|
| One-time manual audit report for one public source | $99-299 | 1 public Telegram source, bounded window, 30-50 extractable signals, exclusions, historical stats, caveats, Telegram delivery | Private groups, X unless memo approved, OCR, future predictions, recommendations | Buyer pays upfront before full report | “I only want it free”, “I need private group”, “I need profitable recommendation” |
| Comparison report across 3 public sources | $249-799 | Same methodology across 3 sources, side-by-side metrics, limitations | Leaderboard, public ranking, advice, automated monitoring | Buyer previously bought one-source report and upgrades | Users cannot name 3 sources or only want browsing curiosity |
| Monthly source monitoring / accountability report | $49-199/mo | Monthly update for already-audited public source, new approved signals, changes since last report | Real-time alerts, copy trading, private sources, bot ingestion | Buyer pays second month after first report | Churn after one month; source activity too ambiguous |
| Seller verification report | $199-999 one-time | Private audit for seller, shareable summary only if methodology accepted | Paid badge marketplace, positive-only report, editorial control | Seller pays and accepts negative/ambiguous findings | Seller demands guaranteed positive rating or hidden failures |

## 14. Final Recommendation

**What to do this week.**

1. Freeze product engineering.
2. Write a one-page paid offer: “Public Telegram Signal Source Audit - 48/72h, no advice, evidence-backed.”
3. Contact 20 qualified prospects manually, starting with trader colleague network.
4. Ask for deposit/payment before producing report.
5. Produce one manual report from an approved public Telegram source and deliver in Telegram.

**What to stop doing.**

- Stop building bot/SaaS/parser/leaderboard ideas.
- Stop treating `SAS-001 acknowledged` as market proof unless actual paid/intent-to-pay users are logged.
- Stop expanding to X, Discord, screenshots, OCR or private groups.
- Stop using “AI extraction” as a selling point; sell trust and decision support.

**What to build next only after validation.**

- A wired operator CLI flow for existing modules.
- Faster manual extraction/review.
- Deterministic report packaging.
- Telegram delivery wrapper, only after paid users demand it.
- Rule/LLM extraction only after manual extraction is measured bottleneck.

**Single metric deciding whether the project advances.**

**3 paid public-source audit reports from 10 qualified conversations within 14 days, with at least 1 repeat source request or referral.**

**Most dangerous founder trap.**

Building the “send link, get stats” Telegram bot because it feels like the killer feature, while the real unproven thing is whether anyone trusts and pays for a negative, caveated, deterministic audit before they buy a signal group.

## 15. Sources

### Internal repo sources read

- `products/signal-analytics-sandbox/README.md`
- `products/signal-analytics-sandbox/docs/PROJECT_BRIEF.md`
- `products/signal-analytics-sandbox/templates/PROJECT_BRIEF.md`
- `products/signal-analytics-sandbox/docs/ARCHITECTURE.md`
- `products/signal-analytics-sandbox/docs/spec.md`
- `products/signal-analytics-sandbox/docs/tasks.md`
- `products/signal-analytics-sandbox/docs/CODEX_PROMPT.md`
- `products/signal-analytics-sandbox/docs/IMPLEMENTATION_CONTRACT.md`
- `products/signal-analytics-sandbox/docs/DECISION_LOG.md`
- `products/signal-analytics-sandbox/docs/IMPLEMENTATION_JOURNAL.md`
- `products/signal-analytics-sandbox/docs/adr/ADR-001-snapshot-serialization.md`
- `products/signal-analytics-sandbox/docs/PILOT_LOG.md`
- `products/signal-analytics-sandbox/docs/legal_risk_memo.md`
- Root `docs/README.md`
- Root `docs/PRODUCT_PORTFOLIO.md`
- Root `docs/AI_DEVELOPMENT_OPERATING_MODEL.md`
- Representative source modules under `products/signal-analytics-sandbox/src/signal_sandbox/`

### External market, competitor, pricing, legal and behavior sources

- SignlyAnalytics - Telegram channel signal analytics, reports, pricing and compliance: https://www.signlyanalytics.com/
- SignalBlink - Telegram signal tracking, leaderboard and pricing: https://www.signalblink.com/
- SignalTrack - Telegram crypto signal provider database claims: https://signaltrack.io/
- TG Parser V2 - public Telegram parser/API and pricing: https://tgparser.cc/
- Telechurn - Telegram channel analytics bot and pricing: https://telechurn.com/
- QuickRecapBot - Telegram AI summaries: https://www.quickrecapbot.com/
- Telepath - Telegram summaries delivery: https://www.trytelepath.com/
- Telegram Content Licensing / AI Scraping Terms: https://telegram.org/tos/content-licensing
- Telegram API Terms of Service: https://core.telegram.org/api/terms
- Telegram Bot API: https://core.telegram.org/bots/api
- X Developer Agreement: https://docs.x.com/developer-terms/agreement
- X Developer Policy: https://docs.x.com/developer-terms/policy
- X API pricing: https://docs.x.com/x-api/getting-started/pricing
- Myfxbook verification docs: https://www.myfxbook.com/help/knowledge-base/verification/
- FX Blue verification docs: https://api.fxblue.com/live/about-verification
- MQL5 Signals marketplace: https://www.mql5.com/en/signals
- MQL5 Signals rules: https://www.mql5.com/en/signals/rules
- MetaTrader 5 trading signals overview: https://www.metatrader5.com/en/trading-platform/trading-signals
- eToro CopyTrader US announcement: https://investors.etoro.com/news-releases/news-release-details/etoro-brings-copytradertm-us-empowering-investors-trade-smarter
- TradingView Ideas: https://www.tradingview.com/ideas/
- Kinfo verified trading performance: https://kinfo.com/
- TraderSync pricing/features: https://tradersync.com/pricing/
- TradeZella pricing: https://help.tradezella.com/en/articles/8911582-our-pricing
- Reddit discussion: “Do trading signal groups actually work?” https://www.reddit.com/r/Forexstrategy/comments/1qry30y/do_trading_signal_groups_actually_work/
- Reddit discussion: “Are These Telegram Gold Trader Signals legit?” https://www.reddit.com/r/Forexstrategy/comments/1f0hhzf/are_these_telegram_gold_trader_signals_legit/
- Reddit discussion: “Has anyone used copy trading...” https://www.reddit.com/r/Daytrading/comments/1rlmy6l/has_anyone_used_copy_trading_to_mirror_successful/
- Reddit discussion: “Have you ever bought VIP signals?” https://www.reddit.com/r/Forex/comments/z089lb/have_you_ever_bought_vip_signals_from_someone/
- Reddit discussion on trading journal subscription sensitivity: https://www.reddit.com/r/saasbuild/comments/1soueoz/i_got_tired_of_trading_journals_charging_30month/
