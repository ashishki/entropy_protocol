"""Shared pytest fixtures for the test suite."""

from __future__ import annotations

import os
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection


@pytest.fixture()
def postgres_connection() -> Iterator[Connection]:
    """Connect to PostgreSQL from DATABASE_URL and verify basic query execution."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL is not set")

    engine = create_engine(database_url)
    connection = engine.connect()

    try:
        connection.execute(text("SELECT 1"))
        yield connection
    finally:
        connection.close()
        engine.dispose()
