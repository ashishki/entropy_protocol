# Auto Extraction Development Plan - bablos79 Draft Parser

Дата: 2026-05-07
Статус: proposed engineering phase after public capture
Scope: `bablos79` public text captures only

## Why This Is Now Justified

До capture автоматизация была преждевременной: не было данных, форматов и
измеримого bottleneck. Сейчас bottleneck конкретный:

- `workspace/captures/bablos79/` содержит 60 public text captures;
- `docs/pilot/EXTRACTION_LOG.md` содержит `pending_manual_extraction=60`;
- ручная классификация всех строк будет первым повторяющимся labor step.

Поэтому допустим узкий engineering phase: не "автоматическая истина", а
deterministic draft parser, который предлагает статусы и поля для human review.

## Product Boundary

Разрешено:

- читать только operator/public captures из local workspace;
- строить deterministic parser/classifier для captured text;
- заполнять draft suggestions в pilot extraction artifact;
- помечать confidence/reason codes;
- оставлять `reviewer_id=pending` до human approval.

Запрещено:

- private/authenticated Telegram scraping;
- OCR/screenshots;
- Telegram bot ingestion;
- LLM output as final truth;
- auto-write в approved ledger;
- report metrics без approved/evaluable records;
- public leaderboard, marketplace, copy trading, broker integration.

## Target Architecture

```text
workspace/captures/bablos79/*.json
  -> load_captures()
  -> optional offline frontier-model lexicon discovery
  -> human-approved author lexicon
  -> deterministic text normalizer
  -> lexical feature extractor
  -> draft status classifier
  -> field candidate extractor
  -> docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  -> human review updates docs/pilot/EXTRACTION_LOG.md
```

The parser does not mutate the approved ledger. It creates reviewable drafts.
Frontier-model output may be used only before parser implementation to propose
author-specific lexicon candidates with evidence. It cannot classify final
records, approve ledger rows, or become a runtime dependency.

## Parser Responsibilities

### 1. Text Normalization

- preserve raw capture files unchanged;
- normalize only an in-memory copy for parsing;
- preserve `capture_id`, `evidence_url`, `capture_timestamp_utc`, and
  `text_sha256` byte-identically in every draft row.

### 2. Ticker Detection

Detect:

- hashtag tickers: `#MAGN`, `#VTBR`, `#UPRO`;
- plain uppercase MOEX-style tickers when surrounded by word boundaries;
- repeated ticker mentions across adjacent posts.

Output:

- `asset_symbol_candidates`;
- `ticker_confidence`;
- `ticker_reason`.

### 3. Trade-Intent Lexicon

Detect Russian trading intent terms:

- short intent: `шорт`, `шорта`, `шортов`, `зашортил`, `добавил шорта`;
- long/buy intent: `лонг`, `купил`, `покупаю`, `набрал`, `добавил`, `откуп`;
- close/reduce intent: `закрыл`, `прикрыл`, `сократил`, `вышел`;
- watch/commentary terms: `похоже`, `кажется`, `негативный признак`,
  `разбор`, `новости`, `дивиденды`.

Output:

- `direction_candidate`: `long`, `short`, `close_or_reduce`, `unknown`;
- `intent_confidence`;
- `intent_reason`.

The initial term list is intentionally incomplete. It must be extended through
hand labels and reviewed author-specific lexicon discovery rather than by
silently widening parser rules.

### 4. Level Extraction

Detect numeric levels only when tied to trade terms:

- entry-like: `взял по`, `купил по`, `шорт от`, `добавил по`;
- stop-like: `стоп`, `инвалидация`, `отмена сценария`;
- target-like: `цель`, `таргет`, `тейк`, `фикс`;
- ranges: `100-105`, `100 – 105`, `100/105`.

Output:

- `entry_candidate`;
- `stop_candidate`;
- `target_candidate`;
- `level_confidence`;
- `missing_required_fields`.

### 5. Draft Classification

The parser suggests one of:

| Suggested status | Rule |
|------------------|------|
| `not_a_signal` | No ticker + no trade intent, or clearly news/meme/commentary. |
| `insufficient_fields` | Ticker/trade intent exists, but entry/stop/target is missing. |
| `ambiguous` | Multiple symbols/directions/levels or unclear linked follow-up. |
| `needs_rule_template` | Repeated structured syntax appears but parser cannot safely map all fields. |
| `review_candidate` | Asset, direction, entry, stop, target, timestamp, and evidence are all detected; still not approved until human review. |

`review_candidate` is not a final ledger status. Human reviewer must convert it
to `approved` or another final extraction status.

## Development Phases

### Phase 10.1 - Seed Labels And Fixtures

Goal: create a small gold-label seed from the 60 captures before coding parser
behavior.

Artifacts:

- `docs/pilot/BABLOS79_LABEL_SEED.md`
- `tests/fixtures/bablos79_captures/` with 10-15 representative public captures

Acceptance criteria:

- seed includes examples for `not_a_signal`, `insufficient_fields`, `ambiguous`,
  and any obvious `review_candidate`;
- each seed row cites `capture_id`, evidence URL, text hash, expected suggested
  status, and reason;
- no approved ledger rows are created.

### Phase 10.2 - LLM-Assisted Author Lexicon Discovery

Goal: use a frontier model offline to propose `bablos79`-specific extraction
terms from the 60 captured posts, then require human approval before any term
can influence deterministic parser behavior.

Artifacts:

- `docs/pilot/bablos79_LEXICON_DRAFT.md`
- `docs/pilot/bablos79_APPROVED_LEXICON.md`
- `workspace/lexicons/bablos79_lexicon_draft.json`

Prompt constraints:

- input is limited to local public captures and seed-label context;
- output is lexicon candidates only, not final extraction rows;
- every candidate must include `term`, `category`, `evidence_capture_ids`,
  short evidence excerpt, false-positive risk, and confidence;
- the model must mark uncertain candidates instead of inventing meanings;
- the operator must approve, reject, or defer every candidate.

Candidate categories:

- `entry_intent`
- `direction_long`
- `direction_short`
- `close_or_reduce`
- `target_or_take_profit`
- `stop_or_invalidation`
- `watch_or_commentary`
- `uncertainty`
- `noise_or_promo`
- `asset_alias`

Acceptance criteria:

- draft lexicon cites evidence from captured posts for every candidate;
- approved lexicon records human decision for every candidate;
- rejected/deferred terms cannot affect parser tests or parser output;
- no LLM call is added to parser runtime, CLI export, ledger writing, or tests.

### Phase 10.3 - Deterministic Draft Parser Library

Goal: implement pure parser functions over `CapturedPost`.

Likely files:

- `src/signal_sandbox/extraction/draft_parser.py`
- `tests/unit/test_draft_parser.py`
- `docs/pilot/bablos79_APPROVED_LEXICON.md`

Acceptance criteria:

- parser preserves evidence fields exactly;
- parser returns structured draft object with suggested status, candidates,
  missing fields, reason codes, and confidence;
- parser classifies seed fixtures deterministically;
- parser has no network calls and no LLM calls.

### Phase 10.4 - Draft Export Artifact

Goal: generate reviewable draft rows without mutating approved ledger.

Likely files:

- `src/signal_sandbox/extraction/draft_export.py`
- `tests/unit/test_draft_export.py`
- `docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md`

Acceptance criteria:

- export reads `workspace/captures/bablos79/`;
- export writes deterministic Markdown/CSV-style rows sorted by source
  timestamp and capture ID;
- export includes `reviewer_id=pending`;
- export never writes to `ledger/`.

### Phase 10.5 - Pilot Extraction Log Merge

Goal: let the operator copy/merge parser suggestions into
`docs/pilot/EXTRACTION_LOG.md` while preserving human review boundary.

Likely files:

- `docs/pilot/EXTRACTION_LOG.md`
- optional helper script or CLI subcommand only if it stays local and T0

Acceptance criteria:

- 60 captured rows receive suggested statuses;
- rows with missing fields stay non-approved;
- any `review_candidate` row still requires `reviewer_id`;
- summary counts update to show draft classifications separately from approved
  final records.

### Phase 10.6 - Evaluation And Decision Gate

Goal: decide whether parser automation is useful enough to keep.

Artifacts:

- `docs/pilot/AUTO_EXTRACTION_EVAL.md`
- update `docs/pilot/PILOT_DECISION.md`

Metrics:

- precision of `not_a_signal` suggestions on reviewed rows;
- number of `review_candidate` rows that human reviewer approves;
- operator minutes saved per 60 captures;
- false-positive count where parser suggested trade intent but reviewer rejects;
- repeated patterns suitable for future `RuleExtractionAdapter` templates.

Acceptance criteria:

- no parser output becomes approved ledger truth without review;
- if false positives are high, parser remains a triage helper only;
- any next engineering task cites measured eval evidence.

## Implementation Order

1. Label 10-15 rows by hand.
2. Run offline frontier-model lexicon discovery over the 60 public captures.
3. Approve/reject/defer author-specific lexicon candidates by hand.
4. Implement parser against labels plus the approved lexicon.
5. Run parser over all 60 captures.
6. Review suggestions manually.
7. Only then decide whether to wire this into CLI or keep it as a pilot helper.

## Stop Conditions

Stop parser development if:

- most captured posts are not trade signals;
- parser cannot distinguish commentary from trade intent without high false
  positives;
- useful posts require screenshots/OCR;
- source format is too inconsistent for deterministic templates;
- customer/payment feedback remains absent after a real report.

## Next Concrete Task

Create `docs/pilot/BABLOS79_LABEL_SEED.md` for 10-15 representative captures
from the 60 captured public posts. This is the required first step before
implementing parser code.
