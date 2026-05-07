"""Unit tests for observability helper stubs."""

from __future__ import annotations

from typing import get_type_hints

from opentelemetry.trace import Tracer

from entropy.metrics import increment_counter, record_histogram
from entropy.tracing import get_tracer


def test_get_tracer_does_not_raise() -> None:
    tracer = get_tracer("entropy.test")

    assert tracer is not None


def test_increment_counter_does_not_raise() -> None:
    increment_counter("test_counter", 2, {"component": "unit-test"})


def test_record_histogram_does_not_raise() -> None:
    record_histogram("test_histogram", 1.25, {"component": "unit-test"})


def test_get_tracer_return_annotation_is_tracer_interface() -> None:
    annotations = get_type_hints(get_tracer)

    assert annotations["return"] is Tracer
