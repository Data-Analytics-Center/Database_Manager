"""Tests the insert functions."""
import pandas as pd
from src.database_manager.execute_query import execute_raw_insert, execute_pandas_insert
from src.database_manager.query_builders import build_insert_query
from src.database_manager.connection_manager import InsertType
import pytest

MAX_INSERT_LIMIT = 80000


def test_valid_raw_insert():
    """Tests the execute_raw_insert() function."""
    table_name = "test"
    sql = build_insert_query(table_name, ["id", "val"], [(1, "Adam")])
    sql2 = build_insert_query(table_name, ["id", "val"], [
                              (1, "Adam"), (2, "Bob")])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    assert sql2 is not None
    assert sql2 != ""
    assert sql2 != " "

    execute_raw_insert(sql, insert_type=InsertType.SINGLE_INSERT)
    execute_raw_insert(sql2, insert_type=InsertType.BULK_INSERT)


def test_valid_pandas_insert():
    """Tests the execute_pandas_insert() function."""
    table_name = "test"
    data_frame = pd.DataFrame(
        {"id": [1, 2, 3], "val": ["Adam", "Bob", "Charlie"]})

    assert data_frame is not None
    assert not data_frame.empty

    execute_pandas_insert(table_name, data_frame)
    execute_pandas_insert(table_name, data_frame)


def test_invalid_insert_type_for_raw_insert():
    """Tests the execute_raw_insert() function for invalid insert type."""
    table_name = "test"
    sql = build_insert_query(table_name, ["id", "val"], [(1, "Adam")])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    with pytest.raises(ValueError, match="Insert type is not of type InsertType"):
        execute_raw_insert(sql, "invalid insert type")


def test_pandas_insert_for_exceeding_dataframe_size():
    """Tests the execute_pandas_insert() function for exceeding dataframe size."""
    max_insert_limit = 80000
    table_name = "test"

    ids = list(range(max_insert_limit + 1))
    vals = [f"val_{i}" for i in range(MAX_INSERT_LIMIT + 1)]

    data_frame = pd.DataFrame({"id": ids, "val": vals})

    assert data_frame is not None
    assert not data_frame.empty

    with pytest.raises(ValueError):
        execute_pandas_insert(table_name, data_frame)
