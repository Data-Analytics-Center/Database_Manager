"""Tests the insert functions."""
import pandas as pd
from src.database_manager.execute_query import execute_raw_insert, execute_pandas_insert
from src.database_manager.connection_manager import create_engine
from src.database_manager.query_builders import build_insert_query
import pytest

MAX_INSERT_LIMIT = 80000


def test_valid_raw_insert():
    """Tests the execute_raw_insert() function"""
    table_name = "test"
    sql = build_insert_query(table_name, ["filename", "id"], [
                             ("final_final_test", 5000)])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    execute_raw_insert(sql)


def test_valid_pandas_insert():
    """Tests the execute_pandas_insert() function"""
    table_name = "test"
    sql = build_insert_query(table_name, ["filename", "id"], [
                             ("final_final_test", 5000)])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    execute_pandas_insert(table_name, pd.DataFrame(
        [("final_final_test", 5000)]))


def mock_create_engine():
    pass


def mock_validate_engine(engine):
    pass


def test_execute_pandas_insert_normal_case(monkeypatch):
    # Mock create_engine and validate_engine functions
    monkeypatch.setattr(
        "src.database_manager.connection_manager.create_engine", mock_create_engine)

    # Create a sample DataFrame
    data = {'column1': [1, 2, 3], 'column2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)

    # Call the function
    execute_pandas_insert('test_table', df)

    # Assert that create_engine and validate_engine were called
    assert mock_create_engine.called
    assert mock_validate_engine.called

# Test case 2: Exception case - DataFrame size exceeds MAX_INSERT_LIMIT


def test_execute_pandas_insert_max_limit_exceeded(monkeypatch):
    # Mock create_engine and validate_engine functions
    monkeypatch.setattr(
        "src.database_manager.connection_manager.create_engine", mock_create_engine)

    # Create a sample DataFrame with more rows than the maximum limit
    data = {'column1': [1] * (MAX_INSERT_LIMIT + 1),
            'column2': ['A'] * (MAX_INSERT_LIMIT + 1)}
    df = pd.DataFrame(data)

    # Ensure the function raises a ValueError
    with pytest.raises(ValueError) as excinfo:
        execute_pandas_insert('test_table', df)

    # Assert the error message
    assert str(
        excinfo.value) == f"Size of DataFrame exceeds the maximum limit of {MAX_INSERT_LIMIT}"
