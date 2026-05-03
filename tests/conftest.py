"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

import os
from contextlib import contextmanager
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection


@contextmanager
def postgres_rollback_connection(database_url: str) -> Iterator[Connection]:
    """Yield a PostgreSQL connection wrapped in a rollback-only transaction."""
    engine = create_engine(database_url)
    connection = engine.connect()
    transaction = connection.begin()

    try:
        connection.execute(text("SELECT 1"))
        yield connection
    finally:
        if transaction.is_active:
            transaction.rollback()
        connection.close()
        engine.dispose()


@pytest.fixture()
def postgres_connection() -> Iterator[Connection]:
    """Connect to PostgreSQL from DATABASE_URL and roll back test writes."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL is not set")

    with postgres_rollback_connection(database_url) as connection:
        yield connection
