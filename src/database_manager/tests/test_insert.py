"""Tests the insert functions."""
import pandas as pd
from src.database_manager.execute_query import execute_raw_insert
from src.database_manager.query_builders import build_insert_query
import pytest


def test_raw_insert_simple_invalid_insert():
    """Tests the raw_insert() function that is used to insert values into the database."""
    table_name = "test"
    sql = build_insert_query(table_name, ["filename", "id"], [
                             ("final_final_test", 5000)])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    with pytest.raises(ValueError, match="Insert type is not of type InsertType"):
        execute_raw_insert(sql, "insert type")


def test_raw_insert_simple_valid_insert():
    """Tests the raw_insert() function that is used to insert values into the database."""
    table_name = "test"
    sql = build_insert_query(table_name, ["filename", "id"], [
                             ("final_final_test", 5000)])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    execute_raw_insert(sql)


def test_raw_insert_bulk():
    """Tests the raw_insert() function that is used to insert values into the database."""
    table_name = "test"
    sql = build_insert_query(table_name, ["filename", "id"], [(
        "test_1", 5000), ("test_2", 10000), ("test_3", 1000)])

    assert sql is not None
    assert sql != ""
    assert sql != " "

    with pytest.raises(ValueError, match="Insert type is not of type InsertType"):
        execute_raw_insert(sql, "insert type")


def test_pandas_insert():
    """Tests the pandas_insert() function that is used to insert values into the database."""
    # table_name = "test"
    data_frame = pd.DataFrame([["test_5", 5], ["test_6", 6], ["test_7", 7], [
                              "test_8", 8]], columns=["filename", "id"])

    assert data_frame is not None
    assert not data_frame.empty
