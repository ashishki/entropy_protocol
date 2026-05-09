from __future__ import annotations

import json
from io import StringIO

from signal_sandbox.observability import (
    configure_json_logger,
    get_tracer,
    log_event,
)


def test_get_tracer_is_singleton() -> None:
    assert get_tracer() is get_tracer()


def test_logger_is_json() -> None:
    stream = StringIO()
    logger = configure_json_logger(stream)

    log_event(logger, subcommand="status", result="ok")

    payload = json.loads(stream.getvalue())
    assert payload["subcommand"] == "status"
    assert payload["result"] == "ok"
    assert isinstance(payload["timestamp"], str)
