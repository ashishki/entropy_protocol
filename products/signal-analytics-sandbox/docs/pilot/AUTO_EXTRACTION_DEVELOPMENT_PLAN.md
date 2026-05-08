# Auto Extraction Development Plan - bablos79 Machine-First Draft Extraction

Дата: 2026-05-08
Статус: Phase 10 execution plan aligned with audit-grade automation roadmap
Scope: `bablos79` public text captures only

Roadmap reference: `docs/pilot/AUDIT_GRADE_AUTOMATION_ROADMAP.md`

## Why This Is Now Justified

До capture автоматизация была преждевременной: не было данных, форматов и
измеримого bottleneck. Сейчас bottleneck конкретный:

- `workspace/captures/bablos79/` содержит 60 public text captures;
- `docs/pilot/EXTRACTION_LOG.md` содержит `pending_manual_extraction=60`;
- ручная классификация всех строк будет первым повторяющимся labor step.

Поэтому допустим узкий engineering phase: не "автоматическая истина", а
machine-first draft extraction pipeline. Frontier model сначала генерирует
pseudo-labels и author-specific vocabulary, deterministic validators проверяют
evidence, а человек смотрит только exception queue и строки, которые попадут в
customer-facing report.

## Product Boundary

Разрешено:

- читать только operator/public captures из local workspace;
- использовать frontier model offline для pseudo-labels и lexicon discovery;
- строить deterministic validators/parser profile для captured text;
- заполнять draft suggestions в pilot extraction artifact;
- помечать confidence/reason codes;
- оставлять `reviewer_id=pending` до exception/customer-facing review.

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
  -> offline frontier-model pseudo-label bootstrap
  -> evidence-span verifier
  -> deterministic draft validators
  -> author-specific lexicon/profile draft
  -> deterministic parser profile
  -> exception review queue
  -> docs/pilot/EXTRACTION_DRAFTS_BABLOS79.md
  -> reviewed rows update docs/pilot/EXTRACTION_LOG.md
```

The pipeline does not mutate the approved ledger. It creates reviewable drafts.
Frontier-model output may propose pseudo-labels, evidence spans, field
candidates, and author-specific lexicon terms. It cannot approve records, report
metrics, or become the final source of truth.

## Pipeline Responsibilities

### 1. Pseudo-Label Bootstrap

For every captured post, generate a draft row with:

- `capture_id`;
- `suggested_status`;
- `asset_candidates`;
- `direction_candidate`;
- `entry_candidate`;
- `stop_candidate`;
- `target_candidate`;
- `missing_fields`;
- `evidence_spans`;
- `confidence`;
- `uncertainty_reason`;
- `lexicon_terms_found`;
- `draft_only=true`.

### 2. Evidence Preservation And Verification

- preserve raw capture files unchanged;
- preserve `capture_id`, `evidence_url`, `capture_timestamp_utc`, and
  `text_sha256` in every draft row;
- verify that every evidence span exists in raw text;
- reject numbers, tickers, or directions that have no text evidence.

### 3. Ticker Detection

Detect:

- hashtag tickers: `#MAGN`, `#VTBR`, `#UPRO`;
- plain uppercase MOEX-style tickers when surrounded by word boundaries;
- repeated ticker mentions across adjacent posts.

Output:

- `asset_symbol_candidates`;
- `ticker_confidence`;
- `ticker_reason`.

### 4. Trade-Intent Lexicon

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
machine-discovered author-specific terms that cite evidence and pass validators.

### 5. Level Extraction

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

### 6. Draft Classification

The pipeline suggests one of:

| Suggested status | Rule |
|------------------|------|
| `not_a_signal` | No ticker + no trade intent, or clearly news/meme/commentary. |
| `insufficient_fields` | Ticker/trade intent exists, but entry/stop/target is missing. |
| `ambiguous` | Multiple symbols/directions/levels or unclear linked follow-up. |
| `needs_rule_template` | Repeated structured syntax appears but parser cannot safely map all fields. |
| `review_candidate` | Asset, direction, entry, stop, target, timestamp, and evidence are all detected; still not approved until human review. |
| `needs_review` | Model/parser disagreement, low confidence, risky lexicon, or customer-facing relevance. |
| `rejected_draft` | Validator found hallucinated span, unsupported number, or unsupported field. |

`review_candidate` is not a final ledger status. Human reviewer must convert it
to `approved` or another final extraction status.

## Development Phases

### Phase 10.1 - Machine-First Pseudo-Label Bootstrap

Goal: generate structured pseudo-labels for all 60 captures before hand-labeling
anything.

Artifacts:

- `docs/pilot/bablos79_PSEUDO_LABELS.md`
- `workspace/extraction/bablos79_pseudo_labels.jsonl`

Acceptance criteria:

- every capture has one pseudo-label row;
- every extracted field cites an evidence span;
- low-confidence rows are explicitly marked;
- no approved ledger rows are created.

### Phase 10.2 - Deterministic Draft Validation

Goal: validate pseudo-labels against raw captures and reject unsupported fields.

Artifacts:

- `src/signal_sandbox/extraction/draft_validation.py`
- `tests/unit/test_draft_validation.py`
- `docs/pilot/bablos79_VALIDATION_SUMMARY.md`

Acceptance criteria:

- evidence spans must exist in raw text;
- unsupported numbers/tickers/directions are rejected;
- rows are classified as `validated_draft`, `needs_review`,
  `rejected_draft`, or `not_a_signal`;
- validator has no network calls and no LLM calls.

### Phase 10.3 - Author Lexicon And Parser Profile

Goal: derive a reusable author-specific profile from validated pseudo-labels and
lexicon terms.

Artifacts:

- `workspace/lexicons/bablos79_lexicon_draft.json`
- `docs/pilot/bablos79_AUTHOR_PROFILE.md`
- `src/signal_sandbox/extraction/parser_profile.py`
- `tests/unit/test_parser_profile.py`

Lexicon constraints:

- input is limited to local public captures, pseudo-labels, and methodology
  context;
- output is lexicon/profile candidates only, not final extraction rows;
- every candidate must include `term`, `category`, `evidence_capture_ids`,
  short evidence excerpt, false-positive risk, and confidence;
- uncertain candidates are marked `needs_review` or `excluded`;
- only `accepted_for_draft` terms may affect parser draft behavior.

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

- lexicon cites evidence from captured posts for every candidate;
- profile records term state: `accepted_for_draft`, `needs_review`, or
  `excluded`;
- excluded terms cannot affect parser tests or parser output;
- no LLM call is added to parser runtime, CLI export, ledger writing, or tests.

### Phase 10.4 - Deterministic Draft Parser Library

Goal: implement pure parser functions over `CapturedPost`.

Likely files:

- `src/signal_sandbox/extraction/draft_parser.py`
- `tests/unit/test_draft_parser.py`
- `docs/pilot/bablos79_AUTHOR_PROFILE.md`

Acceptance criteria:

- parser preserves evidence fields exactly;
- parser returns structured draft object with suggested status, candidates,
  missing fields, reason codes, and confidence;
- parser classifies pseudo-label fixtures deterministically;
- parser has no network calls and no LLM calls.

### Phase 10.5 - Draft Export Artifact

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

### Phase 10.6 - Exception Review Queue And Extraction Log Merge

Goal: create an exception review queue and merge only review-relevant parser
suggestions into `docs/pilot/EXTRACTION_LOG.md`.

Likely files:

- `docs/pilot/EXTRACTION_LOG.md`
- optional helper script or CLI subcommand only if it stays local and T0

Acceptance criteria:

- 60 captured rows receive suggested statuses;
- rows with missing fields stay non-approved;
- any `review_candidate` row still requires `reviewer_id`;
- low-confidence, contradictory, customer-facing, and sampled non-signal rows
  enter the review queue;
- summary counts update to show draft classifications separately from approved
  final records.

### Phase 10.7 - Evaluation And Decision Gate

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

1. Generate pseudo-labels for all 60 public captures.
2. Validate evidence spans and reject unsupported fields.
3. Derive author-specific lexicon/profile from validated drafts.
4. Implement deterministic validators and parser profile support.
5. Export draft suggestions for all 60 captures.
6. Review only the exception queue and customer-facing rows.
7. Only then decide whether to build approved ledger/report automation.

## Stop Conditions

Stop parser development if:

- most captured posts are not trade signals;
- parser cannot distinguish commentary from trade intent without high false
  positives;
- useful posts require screenshots/OCR;
- source format is too inconsistent for deterministic templates;
- customer/payment feedback remains absent after a real report.

## Next Concrete Task

Create `docs/pilot/bablos79_PSEUDO_LABELS.md` and
`workspace/extraction/bablos79_pseudo_labels.jsonl` for all 60 captured public
posts. This is the required first step before implementing deterministic
validators or parser code.
