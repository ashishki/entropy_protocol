# Methodology V0 - Telegram Public Signal Audit

Дата: 2026-05-07
Статус: v0 для `SAS-PILOT-002`
Scope source first: `https://t.me/bablos79`

## Purpose

Эта методология фиксирует, как оператор вручную собирает публичные captures,
извлекает сигналы, помечает ambiguity, считает outcomes и формулирует отчет до
начала работы с первым источником. Методология нужна, чтобы результат был
защищаемым для заказчика и не превращался в прогноз, рекомендацию или
автоматический ingestion product.

## Capture Fields

Каждый capture row или capture file должен содержать:

| Field | Required | Rule |
|-------|----------|------|
| `source_id` | yes | Stable ID from `docs/pilot/PILOT_SCOPE.md`, first source is `bablos79`. |
| `public_url` | yes | Public `https://t.me/...` URL or public post reference. No private, paywalled, login-walled, or access-controlled URL. |
| `capture_timestamp_utc` | yes | ISO-8601 UTC timestamp for when the operator captured the public text. |
| `raw_text` | yes | Public post text exactly as captured. Do not rewrite, translate, summarize, or enrich it in the raw field. |
| `raw_text_sha256` | yes | SHA-256 over the exact `raw_text` bytes used for the capture. |
| `operator_notes` | yes | Short notes for context, limitations, skipped content, or manual capture caveats. |

Capture rules:

- captures are operator-supplied only;
- do not authenticate, impersonate, bypass controls, or collect private groups;
- do not use screenshots/OCR in this pilot;
- if a post is inaccessible, screenshot-only, deleted, edited beyond public
  verification, or login-walled, record a skipped/blocked row instead of trying
  to recover it through another method.

## Signal Qualification

A candidate becomes an approved signal only when all required fields are
defensible from the public capture.

| Field | Qualification rule |
|-------|--------------------|
| `asset_symbol` | Must identify a tradable asset or pair clearly enough to map to price data. |
| `direction` | Must be explicit or defensibly implied as `long` or `short`; `flat` and `unknown` are not evaluable. |
| `entry` | Must include an entry price, range, or deterministic entry rule. |
| `stop` | Must include a stop price, invalidation price, or deterministic invalidation rule. |
| `target` | Must include at least one target/take-profit level or deterministic target rule. |
| `source_timestamp_utc` | Must be tied to the public post timestamp or another defensible source timestamp. |
| `evidence_reference` | Must point to the public URL or local capture path plus `raw_text_sha256`. |

Do not infer missing trade fields from later performance claims. Do not convert
market commentary into a signal unless it contains the fields above.

## Extraction Statuses

| Status | Meaning | Counts in win/loss stats? |
|--------|---------|---------------------------|
| `approved` | All required signal fields are present and reviewer approves the record. | yes, if price data exists |
| `ambiguous` | Looks like a signal, but one or more fields/rules are disputed or under-specified. | no |
| `not_a_signal` | Commentary, education, marketing, result brag, or non-trade content. | no |
| `insufficient_fields` | Trade intent exists, but asset/direction/entry/stop/target/timestamp/evidence is incomplete. | no |
| `duplicate` | Same defensible trade as another record or same canonical dedup key. | no unless explicitly force-included later |
| `needs_rule_template` | Repeated format exists, but current manual methodology needs a future deterministic parser/rule template before scaling. | no |

Every non-approved status must include a short reason. Reasons should be useful
for customer discussion and for deciding whether a future rule template is
worth building.

## Ambiguity Handling

Ambiguity is preserved, not hidden. The operator records ambiguity flags when a
candidate has:

- multiple entry zones without a deterministic fill rule;
- partial targets or trailing stops that cannot be evaluated consistently;
- follow-up posts that may alter the setup but are not clearly linked;
- edited/deleted context that cannot be verified publicly;
- asset ticker ambiguity;
- timeframe ambiguity;
- screenshot-only content;
- language that is promotional rather than actionable.

Ambiguous and excluded records contribute to coverage/exclusion counts, but do
not contribute to win/loss, average return, median return, or drawdown.

## Outcome Semantics

Outcome matching is deterministic and historical-only.

Approved/evaluable records may produce:

- `target_hit`;
- `stop_hit`;
- `timeout_no_hit`;
- `excluded_ambiguous`;
- `excluded_no_price`.

Rules:

- outcome matching uses an approved ledger plus immutable price snapshot;
- each outcome must cite an `outcome_rule_id` from the append-only rule registry;
- re-running the same ledger and same snapshot must produce byte-identical
  outcomes and reports;
- excluded/ambiguous records stay visible in the report but never count as wins
  or losses;
- no slippage, fee, leverage, position sizing, or execution-model claim is added
  unless a later approved methodology version explicitly introduces it.

## Price Provenance

Each report must record:

- price provider ID;
- provider status (`canonical`, `public_exchange`, `prototype`, or equivalent
  current code value);
- snapshot `as_of_utc`;
- `range_start_utc` and `range_end_utc`;
- asset list;
- snapshot SHA-256;
- any non-canonical/prototype warning required by the report generator.

If price data is missing, too ambiguous, or too expensive, write a blocker or
limitation section rather than fabricating outcomes.

## Report Guardrails

Every pilot report and customer summary must preserve these claims:

- historical-only: the report describes what was publicly posted and what would
  have happened under deterministic assumptions;
- non-advice: the report is not investment, trading, financial, legal, or tax
  advice;
- no future prediction: the report must not imply future profitability,
  expected return, projected win rate, or probability of a next signal;
- public-source-only: no private scraping, login-wall bypass, paywall bypass,
  impersonation, credential sharing, or hidden capture path;
- no Entropy Core contamination: pilot source records and reports are not
  evidence for Entropy Core research or trading decisions;
- LLM output is never truth: if an LLM draft is ever used in a later pilot step,
  a human reviewer must approve the final signal record before ledger write.

## Operator Workflow

1. Confirm the source is still in scope and public.
2. Record captures with the required fields above.
3. Mark inaccessible, screenshot-only, private, paywalled, or insufficient-text
   posts as skipped/blocked.
4. Extract signal candidates manually.
5. Assign one extraction status to every candidate.
6. Human-review approved records before they enter the ledger.
7. Match outcomes only for approved/evaluable records and immutable snapshots.
8. Render a private historical report with exclusions, limitations, provenance,
   and non-advice language.
9. Capture customer feedback and payment/repeat/referral signal before
   recommending automation.

## Methodology Change Rule

Do not change this methodology silently during the first source audit. If a
capture or extraction issue requires a rule change, record it as a limitation or
`needs_rule_template` candidate first. A later methodology version can be
created only after the pilot logs show the bottleneck clearly.
