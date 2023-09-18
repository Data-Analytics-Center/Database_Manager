"""Test the select function."""
import os

import pytest

from ..query_builders import build_select_query
from ..query_execution import (
    execute_pandas_select,
    execute_raw_select,
    validate_engine,
    validate_sql,
)
from .test_utils import delete_env_variables


def test_sql_raw_select():
    """Test a valid raw select is executed."""
    table = "test_select"
    sql = build_select_query(table, top=10, columns=["id", "name"])
    assert sql is not None
    assert sql != ""
    assert sql != " "
    result = execute_raw_select(sql)
    assert result is not None
    assert len(result) == 2


def test_sql_select_pandas():
    """Test a valid pandas select is executed."""
    delete_env_variables()
    table = "test_select"
    sql = build_select_query(table=table, top=10, columns=["id", "name"])
    assert sql is not None
    assert sql != ""
    assert sql != " "
    dataframe = execute_pandas_select(sql)
    assert dataframe is not None
    assert dataframe.shape[0] == 2


def test_validate_engine_none():
    """Test that a None engine is rejected."""
    with pytest.raises(ValueError, match="Engine is None"):
        validate_engine(None)


def test_validate_engine_invalid_type():
    """Test that an invalid type is rejected."""
    with pytest.raises(
        ValueError, match="Object passed as engine is not of type Engine"
    ):
        validate_engine("not an engine")


def test_validate_sql_none():
    """Test that a None SQL query is rejected."""
    with pytest.raises(ValueError, match="SQL is None"):
        validate_sql(None)


def test_validate_sql_empty():
    """Test that an empty SQL query is rejected."""
    with pytest.raises(ValueError, match="SQL is empty"):
        validate_sql("")


def test_validate_sql_whitespace():
    """Test that a whitespace SQL query is rejected."""
    with pytest.raises(ValueError, match="SQL is whitespace"):
        validate_sql("     ")


# You'll need to mock 'create_engine' to return a valid engine and possibly the session to simulate actual behavior.
def test_execute_raw_select_invalid_sql():
    """Test that an invalid SQL query is rejected for a raw select."""
    delete_env_variables()
    with pytest.raises(ValueError, match="SQL is whitespace"):
        execute_raw_select(" ")


# Again, you'll likely need to mock 'create_engine' and possibly other methods for this test.
def test_execute_pandas_select_invalid_sql():
    """Test that an invalid SQL query is rejected for a pandas select."""
    delete_env_variables()
    with pytest.raises(ValueError, match="SQL is whitespace"):
        execute_pandas_select(" ")


def test_execute_pandas_select_database_param():
    """Test that an invalid SQL query is rejected for a pandas select."""
    delete_env_variables()
    os.environ["DATABASE"] = ""
    execute_pandas_select("SELECT * FROM test_select", database="test")


def test_execute_raw_select_database_param():
    """Test that an invalid SQL query is rejected for a pandas select."""
    delete_env_variables()
    os.environ["DATABASE"] = ""
    execute_raw_select("SELECT * FROM test_select", database="test")
