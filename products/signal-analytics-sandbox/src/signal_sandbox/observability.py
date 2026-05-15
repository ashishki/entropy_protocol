"""Shared tracing and logging primitives.

The project has a single tracing module by contract. v1 exposes a no-op tracer
so future instrumentation imports from one stable place instead of scattering
inline no-op span implementations.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import TextIO


class NoOpTracer:
    """Minimal tracer compatible with context-manager span usage."""

    @contextmanager
    def start_as_current_span(self, _name: str) -> Iterator[None]:
        yield None


_TRACER = NoOpTracer()
LOGGER_NAME = "signal_sandbox"


def get_tracer() -> NoOpTracer:
    return _TRACER


class JsonLogFormatter(logging.Formatter):
    """Format log records as compact JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, UTC).isoformat()
        payload: dict[str, object] = {
            "timestamp": timestamp,
            "level": record.levelname,
            "message": record.getMessage(),
        }
        event_fields = getattr(record, "event_fields", None)
        if isinstance(event_fields, dict):
            payload.update(event_fields)
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def configure_json_logger(stream: TextIO) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.handlers.clear()
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonLogFormatter())
    logger.addHandler(handler)
    return logger


def log_event(logger: logging.Logger, *, subcommand: str, result: str) -> None:
    logger.info(
        "signal_sandbox_event",
        extra={"event_fields": {"subcommand": subcommand, "result": result}},
    )
