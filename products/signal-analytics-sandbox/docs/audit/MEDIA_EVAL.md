# Media Evaluation

Date: 2026-05-09
Eval Source: `.venv/bin/python -m pytest tests/unit/test_whisper_transcript_adapter.py -q`, run 2026-05-09
Status: PASS

## Scope

Evaluation for `SAS-MEDIA-004: Whisper Transcript Draft Adapter`.

## Results

### Managed Whisper Provider Readiness - 2026-05-15

- Eval Source: `.venv/bin/python -m pytest tests/unit/test_whisper_transcript_adapter.py tests/integration/test_cli_smoke.py -q --tb=short`, run 2026-05-15
- Provider reference: `Dream_Motif_Interpreter` managed Whisper boundary
- CLI command: `signal-sandbox transcribe-media`
- Acquired media input: `docs/pilot/bablos79_MEDIA_MANIFEST.json`
- Attempted voice/audio rows: 2
- Draft transcript artifacts created: 0
- Provider failures: 2 (`WhisperTranscriptionClientError`)
- Root cause: `OPENAI_API_KEY` absent from shell environment and `.env`
- Boundary: PASS; no transcript text was invented and raw media was retained by policy.

### Managed Whisper Provider Completion - 2026-05-15

- Command: `SIGNAL_SANDBOX_ENABLE_MEDIA_TRANSCRIPTION=1 signal-sandbox transcribe-media --media-manifest docs/pilot/bablos79_MEDIA_MANIFEST.json --output-dir docs/pilot/transcripts --approve`
- Acquired media input: `docs/pilot/bablos79_MEDIA_MANIFEST.json`
- Attempted voice/audio rows: 2
- Draft transcript artifacts created: 2
- Provider failures: 0
- Human-reviewed usable refs: 0
- Review queue: `docs/pilot/bablos79_TRANSCRIPT_REVIEW_QUEUE.md`
- Boundary: PASS; transcript output remains draft evidence pending human review.

### SAS-LIVE-003

- Eval Source: `.venv/bin/python -m pytest tests/unit/test_whisper_transcript_adapter.py -q`, run 2026-05-14
- Acquired media input: `docs/pilot/bablos79_MEDIA_MANIFEST.json`
- Attempted voice/audio rows: 2
- Draft transcript artifacts created: 0
- Skipped rows: 2 (`skipped_provider_not_configured`)
- Provider failures: 0
- Boundary: PASS; no transcript text was invented and raw media was retained by policy.

### SAS-LIVE-004

- Eval Source: `.venv/bin/python -m pytest tests/unit/test_ocr_draft_adapter.py -q`, run 2026-05-14
- Acquired media input: `docs/pilot/bablos79_MEDIA_MANIFEST.json`
- Attempted image/screenshot rows: 0
- Skipped non-image media rows: 2
- Draft OCR artifacts created: 0
- Provider failures: 0
- Boundary: PASS; no OCR text or chart interpretation was invented.

### SAS-MEDIA-006

- Eval Source: `.venv/bin/python -m pytest tests/unit/test_ocr_draft_adapter.py -q`, run 2026-05-09
- Injected OCR client: PASS
- Provenance preservation: PASS
- Chart claims review-required: PASS

### SAS-MEDIA-004

- Double gate: PASS
- Provenance preservation: PASS
- Provider failure is not truth: PASS
- Retention/logging policy: PASS

## Boundary Notes

Transcript artifacts are draft evidence only with `reviewer_id="pending"` and
`review_required=true`. The adapter does not approve ledger rows, compute
metrics, render reports, or create customer-facing claims.
