"""Shared tracing helpers for Entropy Protocol."""

from opentelemetry.trace import Tracer, get_tracer_provider

_TRACER_NAME = "entropy"


def get_tracer(name: str = _TRACER_NAME) -> Tracer:
    """Return the shared application tracer."""
    return get_tracer_provider().get_tracer(name)
