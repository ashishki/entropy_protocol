# Transcript Draft Run - bablos79

Date: 2026-05-14
Updated: 2026-05-15
Status: complete_draft_transcripts_pending_review

This artifact records the gated voice transcription attempt for acquired
`bablos79` media. It is internal-only and does not approve transcript text,
source joins, ledgers, outcomes, metrics, report claims, or customer-facing
media evidence.

## Summary

- Input manifest: `docs/pilot/bablos79_MEDIA_MANIFEST.json`
- Voice/audio media attempted: 2
- Draft transcript artifacts created: 2
- Skipped rows: 2 in the 2026-05-14 no-provider run
- Provider-failed rows: 2 in the first 2026-05-15 readiness run before
  `OPENAI_API_KEY` was available; 0 in the completed provider run
- Approved transcript refs: 0
- Customer-facing claims created: 0

## Managed Provider Readiness Run

On 2026-05-15 the managed Whisper client and CLI manifest runner were wired
from the previously discussed `Dream_Motif_Interpreter` pattern:

```bash
SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION=1 \
  .venv/bin/signal-sandbox transcribe-media \
  --media-manifest docs/pilot/bablos79_MEDIA_MANIFEST.json \
  --output-dir docs/pilot/transcripts \
  --approve
```

Result:

- Voice/audio rows: 2
- Draft transcripts: 0
- Skipped: 0
- Provider failures: 2
- Reason: `OPENAI_API_KEY` is absent from both the shell environment and `.env`.

The provider path is now configured, but no live transcript can be produced
until a valid OpenAI API key is supplied to the process.

## Completed Managed Provider Run

After `OPENAI_API_KEY` was supplied, the same command completed successfully:

- Voice/audio rows: 2
- Draft transcripts: 2
- Skipped: 0
- Provider failures: 0
- Human-reviewed usable refs: 0

Draft transcript artifacts:

- `docs/pilot/transcripts/transcript_57b6461001b54e10.json`
- `docs/pilot/transcripts/transcript_92ad5bf2e9088056.json`

Human review queue:

- `docs/pilot/bablos79_TRANSCRIPT_REVIEW_QUEUE.md`

## Run Rows

| media_id | source URL/ref | capture_id | source_document_id | provider | model | status | transcript_id | transcript_sha256 | source_media_sha256 | reviewer_id | review_required | raw_media_retention_action | reason |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `public_voice_bablos79_10476` | `https://t.me/bablos79/10476` | `bablos79-10476` | `bablos79:bablos79-10476` | `managed-whisper` | `whisper-1` | draft_pending_review | `transcript_57b6461001b54e10` | `4509a917e93f875642c246421f714c9011d92c3d4e44e0e0bcd27419ca1bb103` | `dc35f04c417d644b603c9336d96108d485682e467e88e1e476500b1add1e115c` | pending | true | retained_by_policy | draft artifact created; human review pending |
| `public_voice_bablos79_10478` | `https://t.me/bablos79/10478` | `bablos79-10478` | `bablos79:bablos79-10478` | `managed-whisper` | `whisper-1` | draft_pending_review | `transcript_92ad5bf2e9088056` | `28d9d9744aa4490a21b6699e6f7d9c7509b56b7fc2708d2533ecca77d07f5561` | `87ae688d3e55e4ab0eed95c2e4ec3d6ec3aa8a8022acc37a70703b255d6e8b00` | pending | true | retained_by_policy | draft artifact created; human review pending |

## Boundary

Draft transcript text exists as provider output only. The two raw media files
remain local temporary operational data for human review:

- `workspace/media/bablos79/bablos79-10476.ogg`
- `workspace/media/bablos79/bablos79-10478.ogg`

Because no draft transcript artifact has been human-reviewed usable, no
media-derived text may be joined into `SourceDocument` records, used in
extraction, used for outcome preparation, or cited in a customer-facing report.
The next step is human review of
`docs/pilot/bablos79_TRANSCRIPT_REVIEW_QUEUE.md`.
