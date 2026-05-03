"""Database engine and session helpers."""

from __future__ import annotations

import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_database_url() -> str:
    """Return DATABASE_URL from the environment."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set")
    return database_url


def create_database_engine(database_url: str | None = None) -> Engine:
    """Create a SQLAlchemy engine for the configured PostgreSQL database."""
    return create_engine(database_url or get_database_url())


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Create a SQLAlchemy Session factory bound to the given engine."""
    return sessionmaker(bind=engine, expire_on_commit=False)
