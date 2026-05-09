from __future__ import annotations

import logging
from contextlib import nullcontext
from typing import Any


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


class NoopTracer:
    def start_as_current_span(
        self,
        _name: str,
        **_attributes: Any,
    ) -> nullcontext[None]:
        return nullcontext()


_TRACER = NoopTracer()


def get_tracer() -> NoopTracer:
    return _TRACER
