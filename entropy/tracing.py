"""Shared tracing helpers for Entropy Protocol."""

from opentelemetry.trace import NoOpTracer, get_tracer_provider

_TRACER_NAME = "entropy"


def get_tracer() -> NoOpTracer:
    """Return the shared application tracer."""
    return get_tracer_provider().get_tracer(_TRACER_NAME)
