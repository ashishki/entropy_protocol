"""CLI entry point for Entropy Protocol."""

import json
import os
from typing import Any

import duckdb
import typer
from sqlalchemy import create_engine, text

from entropy import __version__

app = typer.Typer(
    help="Entropy Protocol command-line interface.",
    no_args_is_help=True,
    rich_markup_mode=None,
)


@app.callback()
def callback() -> None:
    """Operate Entropy Protocol from the command line."""


@app.command()
def version() -> None:
    """Print the installed package version."""
    typer.echo(__version__)


def check_postgres() -> dict[str, str]:
    """Check PostgreSQL connectivity without exposing connection details."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        return {"name": "postgres", "status": "fail", "error": "DATABASE_URL is not set"}

    engine = create_engine(database_url)
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        return {"name": "postgres", "status": "fail", "error": exc.__class__.__name__}
    finally:
        engine.dispose()

    return {"name": "postgres", "status": "ok"}


def check_duckdb() -> dict[str, str]:
    """Check embedded DuckDB availability."""
    try:
        with duckdb.connect(":memory:") as connection:
            connection.execute("SELECT 1").fetchone()
    except Exception as exc:
        return {"name": "duckdb", "status": "fail", "error": exc.__class__.__name__}

    return {"name": "duckdb", "status": "ok"}


@app.command()
def health() -> None:
    """Print machine-readable health status."""
    checks = [check_postgres(), check_duckdb()]
    failed_checks = [check for check in checks if check["status"] != "ok"]

    if failed_checks:
        payload: dict[str, Any] = {"status": "degraded", "checks": failed_checks}
        typer.echo(json.dumps(payload, sort_keys=True))
        raise typer.Exit(code=1)

    typer.echo(json.dumps({"status": "ok"}, sort_keys=True))


def main() -> None:
    """Run the CLI application."""
    app()
