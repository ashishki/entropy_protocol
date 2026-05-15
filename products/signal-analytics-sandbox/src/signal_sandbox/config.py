"""Configuration helpers for the local CLI."""

from __future__ import annotations

import os
from pathlib import Path


def get_workspace() -> Path:
    """Return the configured workspace path, defaulting to the current directory."""

    return Path(os.environ.get("SIGNAL_SANDBOX_WORKSPACE", ".")).expanduser()
