# Phase 21 Error Register

Date: 2026-05-14
Updated: 2026-05-15
Status: external_delivery_blocking_findings_open

| id | severity | status | scope | description | required fix |
|---|---|---|---|---|---|
| P21-E01 | P1 | closed | media evidence | Two public voice files were acquired and managed Whisper produced draft transcript artifacts. | Closed by `docs/pilot/transcripts/transcript_57b6461001b54e10.json` and `docs/pilot/transcripts/transcript_92ad5bf2e9088056.json`. |
| P21-E02 | P1 | mitigated_internal_open_external | media review | LLM review marked 2 transcript refs usable for internal source join; zero refs are human/operator accepted for external delivery. | Accept an LLM-review policy for external use or add human/operator acceptance before external delivery. |
| P21-E03 | P1 | mitigated_internal_open_external | report readiness | Media-backed internal report now has 3 LLM-reviewed broad-market claims and 0 deterministic outcome metrics. | Keep as internal evidence report or gather explicit ticker/proxy outcome support before external delivery. |
| P21-E04 | P2 | open | source linkage | `bablos79-10465` promises a video, but the exact follow-up media item is not identified. | Link the specific public video or leave the gap as unresolved. |
