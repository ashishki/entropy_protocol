from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from trader_risk_audit import __version__
from trader_risk_audit.artifacts.manifest import hash_file

REQUIRED_IMPORT_ARTIFACT_NAMES = ("raw_snapshot", "normalized_trades")


@dataclass(frozen=True)
class ExchangeImportArtifact:
    name: str
    path: str
    sha256: str


@dataclass(frozen=True)
class ExchangeImportManifest:
    manifest_id: str
    package_version: str
    exchange: str
    market: str
    symbols: tuple[str, ...]
    start_time: str
    end_time: str
    generated_at: str
    artifacts: tuple[ExchangeImportArtifact, ...]
    content_hash: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True) + "\n"


class ExchangeImportManifestValidationError(ValueError):
    pass


class MissingExchangeImportArtifactError(ExchangeImportManifestValidationError):
    pass


def build_exchange_import_manifest(
    *,
    raw_snapshot: Path | str,
    normalized_trades: Path | str,
    exchange: str,
    market: str,
    symbols: tuple[str, ...],
    start_time: str,
    end_time: str,
    generated_at: str | None = None,
    package_version: str = __version__,
) -> ExchangeImportManifest:
    artifacts = (
        ExchangeImportArtifact(
            name="raw_snapshot",
            path=str(Path(raw_snapshot)),
            sha256=hash_file(raw_snapshot),
        ),
        ExchangeImportArtifact(
            name="normalized_trades",
            path=str(Path(normalized_trades)),
            sha256=hash_file(normalized_trades),
        ),
    )
    content_hash = compute_exchange_import_content_hash(
        package_version=package_version,
        exchange=exchange,
        market=market,
        symbols=symbols,
        start_time=start_time,
        end_time=end_time,
        artifacts=artifacts,
    )
    return ExchangeImportManifest(
        manifest_id=content_hash[:16],
        package_version=package_version,
        exchange=exchange,
        market=market,
        symbols=tuple(symbols),
        start_time=start_time,
        end_time=end_time,
        generated_at=generated_at or datetime.now(UTC).isoformat(),
        artifacts=artifacts,
        content_hash=content_hash,
    )


def compute_exchange_import_content_hash(
    *,
    package_version: str,
    exchange: str,
    market: str,
    symbols: tuple[str, ...],
    start_time: str,
    end_time: str,
    artifacts: tuple[ExchangeImportArtifact, ...],
) -> str:
    stable_payload = {
        "artifacts": [
            {"name": artifact.name, "sha256": artifact.sha256}
            for artifact in sorted(artifacts, key=lambda item: item.name)
        ],
        "exchange": exchange,
        "market": market,
        "package_version": package_version,
        "symbols": list(symbols),
        "time_range": {"end_time": end_time, "start_time": start_time},
    }
    payload = json.dumps(stable_payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_exchange_import_manifest(manifest: ExchangeImportManifest) -> None:
    records_by_name = {artifact.name: artifact for artifact in manifest.artifacts}
    missing_names = [
        name for name in REQUIRED_IMPORT_ARTIFACT_NAMES if name not in records_by_name
    ]
    if missing_names:
        missing = ", ".join(missing_names)
        raise MissingExchangeImportArtifactError(
            f"Exchange import manifest is missing artifact record: {missing}"
        )

    for artifact in manifest.artifacts:
        path = Path(artifact.path)
        if not path.exists():
            raise MissingExchangeImportArtifactError(
                f"Exchange import artifact is absent: {artifact.path}"
            )
        actual_hash = hash_file(path)
        if actual_hash != artifact.sha256:
            raise ExchangeImportManifestValidationError(
                f"Exchange import artifact hash drift: {artifact.name}"
            )

    expected_content_hash = compute_exchange_import_content_hash(
        package_version=manifest.package_version,
        exchange=manifest.exchange,
        market=manifest.market,
        symbols=manifest.symbols,
        start_time=manifest.start_time,
        end_time=manifest.end_time,
        artifacts=manifest.artifacts,
    )
    if expected_content_hash != manifest.content_hash:
        raise ExchangeImportManifestValidationError(
            "Exchange import manifest content hash drift"
        )
