"""Metric stubs for future observability activation."""

from collections.abc import Mapping
from typing import Any


def increment_counter(
    name: str, value: int = 1, attributes: Mapping[str, Any] | None = None
) -> None:
    """No-op counter stub."""
    _ = (name, value, attributes)


def record_histogram(
    name: str,
    value: float,
    attributes: Mapping[str, Any] | None = None,
) -> None:
    """No-op histogram stub."""
    _ = (name, value, attributes)
