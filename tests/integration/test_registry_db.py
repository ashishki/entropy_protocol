"""Integration tests for registry database migrations."""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path

import pytest
import polars as pl
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session, sessionmaker

from entropy.data import LocalFixtureAdapter
from entropy.db.models import MarketDataset
from entropy.hashing import compute_dataset_hash
from entropy.models.market import Timeframe
from entropy.models.registry import TrialSpec
from entropy.registry.write import DuplicateTrialError, MissingHashError, register_trial

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ALEMBIC_CONFIG = PROJECT_ROOT / "migrations" / "alembic.ini"
CORE_TABLES = {"trial_registry", "runs", "market_datasets", "fill_logs", "governance_events"}


def database_url_or_skip() -> str:
    """Return DATABASE_URL or skip DB integration tests."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL is not set")
    return database_url


def assert_test_database(database_url: str) -> None:
    """Refuse destructive migration reset against non-test databases."""
    database_name = make_url(database_url).database or ""
    if "test" not in database_name:
        pytest.skip("DATABASE_URL database name must contain 'test' for migration reset")


def alembic_executable() -> str:
    """Return the Alembic executable from PATH or the local virtualenv."""
    return shutil.which("alembic") or str(PROJECT_ROOT / ".venv" / "bin" / "alembic")


def run_alembic(database_url: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Run Alembic with the project migration config."""
    env = os.environ.copy()
    env["DATABASE_URL"] = database_url
    return subprocess.run(
        [alembic_executable(), "-c", str(ALEMBIC_CONFIG), *args],
        cwd=PROJECT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def reset_database(engine: Engine) -> None:
    """Drop migration-managed objects from the test database."""
    drop_statements = [
        text("DROP TABLE IF EXISTS governance_events CASCADE"),
        text("DROP TABLE IF EXISTS fill_logs CASCADE"),
        text("DROP TABLE IF EXISTS market_datasets CASCADE"),
        text("DROP TABLE IF EXISTS runs CASCADE"),
        text("DROP TABLE IF EXISTS trial_registry CASCADE"),
        text("DROP TABLE IF EXISTS alembic_version CASCADE"),
    ]
    with engine.begin() as connection:
        for statement in drop_statements:
            connection.execute(statement)


@pytest.fixture()
def migrated_engine() -> Iterable[Engine]:
    """Run the initial migration against a clean test database."""
    database_url = database_url_or_skip()
    assert_test_database(database_url)
    engine = create_engine(database_url)
    reset_database(engine)

    result = run_alembic(database_url, "upgrade", "head")
    if result.returncode != 0:
        pytest.fail(f"alembic upgrade failed\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")

    try:
        yield engine
    finally:
        reset_database(engine)
        engine.dispose()


def column_names(engine: Engine, table_name: str) -> set[str]:
    """Return column names for a table."""
    return {column["name"] for column in inspect(engine).get_columns(table_name)}


def make_trial_spec(**overrides: object) -> TrialSpec:
    """Create a valid TrialSpec for registry write tests."""
    data = {
        "trial_id": "trial-001",
        "family_tag": "mean-reversion",
        "hypothesis": "Mean reversion after large one-hour moves.",
        "dataset_hash": "dataset-sha",
        "code_hash": "code-sha",
        "policy_hash": "policy-sha",
        "parameter_lock": {"lookback": 24},
        "registered_at": "2026-05-03T12:00:00Z",
    }
    data.update(overrides)
    return TrialSpec(**data)


def trial_registry_count(session: Session) -> int:
    """Return row count in trial_registry."""
    return session.execute(text("SELECT count(*) FROM trial_registry")).scalar_one()


def write_fixture_csv(path: Path) -> None:
    """Write a minimal valid OHLCV fixture file."""
    path.write_text(
        "\n".join(
            [
                "timestamp,open,high,low,close,volume",
                "2026-05-01T00:00:00Z,100,110,95,105,12.5",
                "2026-05-01T01:00:00Z,105,112,101,108,8.0",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_alembic_upgrade_creates_all_tables(migrated_engine: Engine) -> None:
    tables = set(inspect(migrated_engine).get_table_names())

    assert CORE_TABLES.issubset(tables)


def test_trial_registry_schema(migrated_engine: Engine) -> None:
    columns = column_names(migrated_engine, "trial_registry")
    required_columns = {
        "trial_id",
        "family_tag",
        "hypothesis",
        "dataset_hash",
        "code_hash",
        "policy_hash",
        "status",
        "parameter_lock",
        "registered_at",
        "created_at",
    }
    inspector = inspect(migrated_engine)
    parameter_lock = {
        column["name"]: column["type"] for column in inspector.get_columns("trial_registry")
    }["parameter_lock"]

    assert required_columns.issubset(columns)
    assert inspector.get_pk_constraint("trial_registry")["constrained_columns"] == ["trial_id"]
    assert parameter_lock.__class__.__name__ == "JSONB"


def test_runs_table_schema(migrated_engine: Engine) -> None:
    columns = column_names(migrated_engine, "runs")
    required_columns = {
        "run_id",
        "trial_id",
        "dataset_hash",
        "code_hash",
        "policy_hash",
        "simbroker_version",
        "is_start",
        "is_end",
        "oos_start",
        "oos_end",
        "embargo_bars",
        "leakage_status",
        "created_at",
    }
    foreign_keys = inspect(migrated_engine).get_foreign_keys("runs")

    assert required_columns.issubset(columns)
    assert inspect(migrated_engine).get_pk_constraint("runs")["constrained_columns"] == ["run_id"]
    assert any(fk["referred_table"] == "trial_registry" for fk in foreign_keys)


def test_governance_events_schema(migrated_engine: Engine) -> None:
    columns = column_names(migrated_engine, "governance_events")
    required_columns = {
        "event_id",
        "trial_id",
        "event_type",
        "actor",
        "reason",
        "policy_hash",
        "prior_state",
        "next_state",
        "created_at",
    }

    assert required_columns.issubset(columns)
    assert inspect(migrated_engine).get_pk_constraint("governance_events")[
        "constrained_columns"
    ] == ["event_id"]


def test_market_datasets_schema(migrated_engine: Engine) -> None:
    columns = column_names(migrated_engine, "market_datasets")
    required_columns = {
        "dataset_hash",
        "symbol",
        "timeframe",
        "start_ts",
        "end_ts",
        "row_count",
        "source_path",
        "parquet_path",
        "provenance",
        "created_at",
    }
    inspector = inspect(migrated_engine)
    provenance = {
        column["name"]: column["type"] for column in inspector.get_columns("market_datasets")
    }["provenance"]

    assert required_columns.issubset(columns)
    assert inspector.get_pk_constraint("market_datasets")["constrained_columns"] == ["dataset_hash"]
    assert provenance.__class__.__name__ == "JSONB"


def test_fill_logs_schema(migrated_engine: Engine) -> None:
    columns = column_names(migrated_engine, "fill_logs")
    required_columns = {
        "fill_id",
        "run_id",
        "timestamp",
        "symbol",
        "side",
        "quantity",
        "fill_price",
        "commission",
        "slippage",
        "market_impact",
        "borrow_rate",
        "funding_rate",
        "total_cost",
        "constrained",
        "created_at",
    }
    foreign_keys = inspect(migrated_engine).get_foreign_keys("fill_logs")

    assert required_columns.issubset(columns)
    assert inspect(migrated_engine).get_pk_constraint("fill_logs")["constrained_columns"] == [
        "fill_id"
    ]
    assert any(fk["referred_table"] == "runs" for fk in foreign_keys)


def test_alembic_downgrade_reverts_migration() -> None:
    database_url = database_url_or_skip()
    assert_test_database(database_url)
    engine = create_engine(database_url)
    reset_database(engine)

    upgrade = run_alembic(database_url, "upgrade", "head")
    if upgrade.returncode != 0:
        pytest.fail(f"alembic upgrade failed\nSTDOUT:\n{upgrade.stdout}\nSTDERR:\n{upgrade.stderr}")

    downgrade = run_alembic(database_url, "downgrade", "-1")
    if downgrade.returncode != 0:
        pytest.fail(
            f"alembic downgrade failed\nSTDOUT:\n{downgrade.stdout}\nSTDERR:\n{downgrade.stderr}"
        )

    try:
        tables = set(inspect(engine).get_table_names())
        assert CORE_TABLES.isdisjoint(tables)
    finally:
        reset_database(engine)
        engine.dispose()


def test_write_valid_trial_spec_inserts_row(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        trial_id = register_trial(session, make_trial_spec())
        session.commit()

        rows = session.execute(
            text("SELECT trial_id, status FROM trial_registry WHERE trial_id = :trial_id"),
            {"trial_id": trial_id},
        ).all()

    assert trial_id == "trial-001"
    assert rows == [("trial-001", "PENDING")]


def test_write_rejects_missing_dataset_hash(migrated_engine: Engine) -> None:
    trial_spec = TrialSpec.model_construct(
        trial_id="trial-missing-hash",
        family_tag="mean-reversion",
        hypothesis="Mean reversion after large one-hour moves.",
        dataset_hash=None,
        code_hash="code-sha",
        policy_hash="policy-sha",
        parameter_lock={"lookback": 24},
        registered_at=make_trial_spec().registered_at,
    )

    with Session(migrated_engine) as session:
        try:
            with pytest.raises(MissingHashError):
                register_trial(session, trial_spec)
            assert trial_registry_count(session) == 0
        finally:
            session.rollback()


def test_write_rejects_duplicate_trial_id(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        register_trial(session, make_trial_spec())
        session.commit()

        with pytest.raises(DuplicateTrialError):
            register_trial(session, make_trial_spec())

        assert trial_registry_count(session) == 1


def test_fixture_adapter_writes_parquet(migrated_engine: Engine, tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixtures" / "BTC-USD_H1.csv"
    fixture_path.parent.mkdir()
    data_dir = tmp_path / "data"
    write_fixture_csv(fixture_path)
    adapter = LocalFixtureAdapter(
        fixture_path=fixture_path,
        data_dir=data_dir,
        session_factory=sessionmaker(bind=migrated_engine),
    )

    adapter.fetch_ohlcv(
        "BTC-USD",
        Timeframe.H1,
        datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 5, 1, 1, 0, tzinfo=timezone.utc),
    )
    parquet_files = list(data_dir.rglob("*.parquet"))

    assert len(parquet_files) == 1
    assert pl.read_parquet(parquet_files[0]).height == 2


def test_fixture_adapter_records_correct_hash(migrated_engine: Engine, tmp_path: Path) -> None:
    fixture_path = tmp_path / "fixtures" / "BTC-USD_H1.csv"
    fixture_path.parent.mkdir()
    data_dir = tmp_path / "data"
    write_fixture_csv(fixture_path)
    adapter = LocalFixtureAdapter(
        fixture_path=fixture_path,
        data_dir=data_dir,
        session_factory=sessionmaker(bind=migrated_engine),
    )

    adapter.fetch_ohlcv(
        "BTC-USD",
        Timeframe.H1,
        datetime(2026, 5, 1, 0, 0, tzinfo=timezone.utc),
        datetime(2026, 5, 1, 1, 0, tzinfo=timezone.utc),
    )
    parquet_path = next(data_dir.rglob("*.parquet"))
    expected_hash = compute_dataset_hash(parquet_path)

    with Session(migrated_engine) as session:
        record = session.get(MarketDataset, expected_hash)

    assert record is not None
    assert record.dataset_hash == expected_hash
    assert record.parquet_path == str(parquet_path)
    assert record.row_count == 2
