"""Tests the insert functions."""
import pandas as pd
import pytest

from src.database_manager.connection_manager import InsertType
from src.database_manager.execute_query import execute_pandas_insert, execute_raw_insert
from src.database_manager.query_builders import build_insert_query

from .test_utils import delete_env_variables

MAX_INSERT_LIMIT = 80000
TABLE_NAME = "test"


def test_valid_raw_insert_for_single_insert():
    """Tests the execute_raw_insert() function for single insert."""
    delete_env_variables()
    sql = build_insert_query(TABLE_NAME, ["id", "val"], [(1, "Adam")])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    execute_raw_insert(sql, insert_type=InsertType.SINGLE_INSERT)


def test_valid_raw_insert_for_bulk_insert():
    """Tests the execute_raw_insert() function for bulk insert."""
    delete_env_variables()
    sql = build_insert_query(TABLE_NAME, ["id", "val"], [(1, "Adam"), (2, "Bob")])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    execute_raw_insert(sql, insert_type=InsertType.BULK_INSERT)


def test_invalid_insert_type_for_raw_insert():
    """Tests the execute_raw_insert() function for invalid insert type."""
    delete_env_variables()
    sql = build_insert_query(TABLE_NAME, ["id", "val"], [(1, "Adam")])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    with pytest.raises(
        ValueError, match="Insert type parameter given is not of type InsertType"
    ):
        execute_raw_insert(sql, "invalid insert type")


def test_invalid_custom_sql_for_raw_insert():
    """Tests the execute_raw_insert() function for invalid custom SQL."""
    with pytest.raises(ValueError, match="SQL is None"):
        execute_raw_insert(sql=None)
    with pytest.raises(ValueError, match="SQL is empty"):
        execute_raw_insert(sql="")
    with pytest.raises(ValueError, match="SQL is whitespace"):
        execute_raw_insert(sql=" ")


def test_sql_not_provided_for_raw_insert():
    """Tests the execute_raw_insert() function for sql not provided."""
    with pytest.raises(TypeError):
        execute_raw_insert()


def test_valid_raw_insert_for_single_insert_with_custom_sql():
    """Tests the execute_raw_insert() function for single insert with custom SQL."""
    sql = "INSERT INTO test (id, val) VALUES (1, 'Adam')"
    execute_raw_insert(sql, insert_type=InsertType.SINGLE_INSERT)


def test_valid_pandas_insert():
    """Tests the execute_pandas_insert() function."""
    delete_env_variables()
    data_frame = pd.DataFrame({"id": [1, 2, 3], "val": ["Adam", "Bob", "Charlie"]})

    assert data_frame is not None
    assert not data_frame.empty

    execute_pandas_insert(TABLE_NAME, data_frame)


def test_pandas_insert_for_exceeding_dataframe_size():
    """Tests the execute_pandas_insert() function for exceeding dataframe size."""
    delete_env_variables()
    ids = list(range(MAX_INSERT_LIMIT + 1))
    vals = [f"val_{i}" for i in range(MAX_INSERT_LIMIT + 1)]

    data_frame = pd.DataFrame({"id": ids, "val": vals})

    assert data_frame is not None
    assert not data_frame.empty

    with pytest.raises(
        ValueError, match="Dataframe size exceeds the maximum insert limit"
    ):
        execute_pandas_insert(TABLE_NAME, data_frame)


def test_pandas_insert_for_empty_dataframe():
    """Tests the execute_pandas_insert() function for empty dataframe."""
    data_frame = pd.DataFrame()

    with pytest.raises(ValueError, match="Dataframe is empty"):
        execute_pandas_insert(TABLE_NAME, data_frame)


def test_pandas_insert_for_invalid_dataframe():
    """Tests the execute_pandas_insert() function for invalid dataframe."""
    data_frame = None

    with pytest.raises(ValueError, match="Dataframe is not of type pd.DataFrame"):
        execute_pandas_insert(TABLE_NAME, data_frame)


def test_pandas_insert_for_invalid_table_name():
    """Tests the execute_pandas_insert() function for invalid table name."""
    table_names = ["", " ", None]
    data_frame = pd.DataFrame({"id": [1, 2, 3], "val": ["Adam", "Bob", "Charlie"]})

    assert data_frame is not None
    assert not data_frame.empty

    for table_name in table_names:
        with pytest.raises(ValueError, match="Table name is None"):
            execute_pandas_insert(table_name, data_frame)
