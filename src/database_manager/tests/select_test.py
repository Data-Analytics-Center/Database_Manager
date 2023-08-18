"""Test the select function."""

from ..connection_manager import create_engine
from ..execute_query import execute_raw_select, execute_pandas_select
from ..query_builders import build_select_query
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")
driver = os.getenv("DRIVER")
table = os.getenv("TABLE")


def test_sql_raw_select():
    """Test that a valid engine is created."""
    engine = create_engine(server, database, driver, bulk_insert=False)
    assert engine is not None
    sql = build_select_query(table, 10, ["filepath", "id"])
    assert sql is not None
    result = execute_raw_select(engine, sql)
    assert result is not None


def test_sql_select_pandas():
    engine = create_engine(server, database, driver, bulk_insert=False)
    assert engine is not None
    sql = build_select_query(table, 10, ["filepath", "id"])
    assert sql is not None
    result = execute_pandas_select(engine, sql)
    assert result is not None
