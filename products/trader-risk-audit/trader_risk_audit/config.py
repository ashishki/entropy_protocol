from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    """Raised when local runtime configuration violates product guardrails."""


@dataclass(frozen=True)
class Settings:
    env: str
    upload_dir: Path
    report_dir: Path
    log_level: str
    telegram_delivery_enabled: bool
    live_broker_api_enabled: bool
    order_blocking_enabled: bool


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    source = os.environ if env is None else env
    live_broker_api_enabled = _parse_bool(
        source.get("TRA_LIVE_BROKER_API_ENABLED", "false"),
        "TRA_LIVE_BROKER_API_ENABLED",
    )
    order_blocking_enabled = _parse_bool(
        source.get("TRA_ORDER_BLOCKING_ENABLED", "false"),
        "TRA_ORDER_BLOCKING_ENABLED",
    )

    if live_broker_api_enabled:
        raise ConfigError("TRA_LIVE_BROKER_API_ENABLED is forbidden for v1")
    if order_blocking_enabled:
        raise ConfigError("TRA_ORDER_BLOCKING_ENABLED is forbidden for v1")

    return Settings(
        env=source.get("TRA_ENV", "local"),
        upload_dir=Path(source.get("TRA_UPLOAD_DIR", "data/uploads")),
        report_dir=Path(source.get("TRA_REPORT_DIR", "artifacts/reports")),
        log_level=source.get("TRA_LOG_LEVEL", "INFO"),
        telegram_delivery_enabled=_parse_bool(
            source.get("TRA_TELEGRAM_DELIVERY_ENABLED", "false"),
            "TRA_TELEGRAM_DELIVERY_ENABLED",
        ),
        live_broker_api_enabled=live_broker_api_enabled,
        order_blocking_enabled=order_blocking_enabled,
    )


def _parse_bool(value: str, name: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ConfigError(f"{name} must be a boolean value")
