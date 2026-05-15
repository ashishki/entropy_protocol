# Second Research Archive Dataset Manifest

Status: ARCHIVE_ONLY_NO_HOLDOUT
Schema version: archive-dataset-manifest/v1
Candidate id: SRC-001-STRUCTURE-RETEST-BOUNCE
Formation scope: archive fixture formation rows only
Evaluation scope: archive fixture evaluation rows only; no holdout
Holdout exclusion: holdout_locked_not_read
Aggregate dataset hash: PENDING_T21_ARCHIVE_DATASET_HASH_FROM_LOCAL_FIXTURE
Manifest hash: PENDING_T21_ARCHIVE_DATASET_MANIFEST_HASH_FROM_LOCAL_FIXTURE

## Dataset Bindings

| Dataset id | Role | Path | Dataset hash | Row count |
|------------|------|------|--------------|-----------|
| eth-archive-formation | formation | `archive/eth/formation.parquet` | `PENDING_T21_FORMATION_DATASET_HASH` | 0 |
| eth-archive-evaluation-probe | evaluation_probe | `archive/eth/evaluation_probe.parquet` | `PENDING_T21_EVALUATION_PROBE_DATASET_HASH` | 0 |

## Holdout Boundary

- Holdout remains locked.
- No holdout path is listed in this manifest.
- No holdout read, unlock, OOS/performance, production, or capital-ready claim is approved.
