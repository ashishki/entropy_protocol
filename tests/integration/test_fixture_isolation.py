"""Integration tests for PostgreSQL fixture transaction isolation."""

from __future__ import annotations

import os

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url

from tests.conftest import postgres_rollback_connection


def database_url_or_skip() -> str:
    """Return DATABASE_URL or skip DB integration tests."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL is not set")
    database_name = make_url(database_url).database or ""
    if "test" not in database_name:
        pytest.skip("DATABASE_URL database name must contain 'test' for fixture isolation test")
    return database_url


def test_postgres_fixture_rolls_back_on_teardown() -> None:
    database_url = database_url_or_skip()
    engine = create_engine(database_url)

    try:
        with engine.begin() as setup_connection:
            setup_connection.execute(text("DROP TABLE IF EXISTS fixture_rollback_check"))
            setup_connection.execute(text("CREATE TABLE fixture_rollback_check (value TEXT)"))

        with postgres_rollback_connection(database_url) as connection:
            connection.execute(
                text("INSERT INTO fixture_rollback_check (value) VALUES (:value)"),
                {"value": "should_rollback"},
            )

        with engine.connect() as check_connection:
            count = check_connection.execute(
                text("SELECT count(*) FROM fixture_rollback_check WHERE value = :value"),
                {"value": "should_rollback"},
            ).scalar_one()

        assert count == 0
    finally:
        with engine.begin() as teardown_connection:
            teardown_connection.execute(text("DROP TABLE IF EXISTS fixture_rollback_check"))
        engine.dispose()
