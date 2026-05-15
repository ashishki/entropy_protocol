from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


class TelegramBotConfigError(ValueError):
    pass


@dataclass(frozen=True)
class TelegramBotConfig:
    enabled: bool
    token: str
    workspace_dir: Path


def load_bot_config(env: Mapping[str, str] | None = None) -> TelegramBotConfig:
    source = os.environ if env is None else env
    enabled = _parse_bool(source.get("TRA_TELEGRAM_BOT_ENABLED", "false"))
    token = source.get("TRA_TELEGRAM_BOT_TOKEN", "").strip()
    workspace_dir = Path(
        source.get("TRA_TELEGRAM_WORKSPACE_DIR", "data/telegram_audits")
    )

    if not enabled:
        raise TelegramBotConfigError("TRA_TELEGRAM_BOT_ENABLED must be true")
    if not token:
        raise TelegramBotConfigError("TRA_TELEGRAM_BOT_TOKEN must be set")

    return TelegramBotConfig(
        enabled=enabled,
        token=token,
        workspace_dir=workspace_dir,
    )


def _parse_bool(value: str) -> bool:
    normalized = value.strip().casefold()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise TelegramBotConfigError("TRA_TELEGRAM_BOT_ENABLED must be a boolean value")
