"""Test cases for the query builders module."""

import pytest
from src.database_manager.query_builders import build_insert_query, build_select_query

TABLE_NAME = "test"
MAX_INSERT_LIMIT = 80000


def test_build_select_query_invalid_table():
    """Test that the function raises ValueError when table name is invalid."""
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query("", columns=["Id"])
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query(" ", columns=["Id"])
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query(None, columns=["Id"])


def test_build_select_query_no_table():
    """Test that the function raises TypeError when table name is not provided."""
    with pytest.raises(TypeError):
        build_select_query(columns=["Id"])
    with pytest.raises(TypeError):
        build_select_query(columns=["Id"], where="Id = 5")


def test_build_select_query_default_args():
    """Test that the function returns the correct query with default values, when no args are provided."""
    sql_query = build_select_query(table=TABLE_NAME)
    expected_query = f"SELECT * FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_with_all_args_provided():
    """Test that the function returns the correct query with all args provided."""
    sql_query = build_select_query(
        table=TABLE_NAME,
        top=100,
        columns=["Id", "Value"],
        where="Id = 5",
        group_by="Id",
        order_by="Value DESC",
    )
    expected_query = (
        f"SELECT TOP 100 Id, Value FROM {TABLE_NAME} WHERE Id = 5 GROUP BY Id ORDER BY Value DESC"
    )
    assert sql_query == expected_query


def test_build_select_query_no_top():
    """Test that the function returns the correct query when top is not provided."""
    sql_query = build_select_query(table=TABLE_NAME, columns=["Id"])
    expected_query = f"SELECT Id FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_cols():
    """Test that the function returns the correct query when cols is not provided."""
    sql_query = build_select_query(table=TABLE_NAME, top=10)
    expected_query = f"SELECT TOP 10 * FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_where():
    """Test that the function returns the correct query when the 'where' clause is not provided."""
    sql_query = build_select_query(table=TABLE_NAME, columns=["Id", "Value"])
    expected_query = f"SELECT Id, Value FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_group_by():
    """Test that the function returns the correct query when the 'group by' clause is not provided."""
    sql_query = build_select_query(table=TABLE_NAME, columns=[
                                   "Id"], where="Id > 5")
    expected_query = f"SELECT Id FROM {TABLE_NAME} WHERE Id > 5"
    assert sql_query == expected_query


def test_build_select_query_no_order_by():
    """Test that the function returns the correct query when the 'order by' clause is not provided."""
    sql_query = build_select_query(table=TABLE_NAME, columns=[
                                   "Id"], order_by="Id ASC")
    expected_query = f"SELECT Id FROM {TABLE_NAME} ORDER BY Id ASC"
    assert sql_query == expected_query


def test_build_insert_query_invalid_table():
    """Test that the function raises ValueError when table name is invalid."""
    with pytest.raises(ValueError, match="Table name is required."):
        build_insert_query("", ["Id", "Values"], [
                           (1, "Value1"), (2, "Value2")])
    with pytest.raises(ValueError, match="Table name is required."):
        build_insert_query(" ", ["Id", "Values"], [
                           (1, "Value1"), (2, "Value2")])
    with pytest.raises(ValueError, match="Table name is required."):
        build_insert_query(None, ["Id", "Values"], [
                           (1, "Value1"), (2, "Value2")])


def test_build_insert_query_no_table():
    """Test that the function raises TypeError when table name is not provided."""
    with pytest.raises(TypeError):
        build_insert_query(["Id", "Values"], [(1, "Value1"), (2, "Value2")])


def test_build_insert_query_no_columns():
    """Test that the function raises ValueError when an empty list is provided for column names."""
    with pytest.raises(ValueError, match="At least one column is required!"):
        build_insert_query(TABLE_NAME, [], [(1, "Value1"), (2, "Value2")])


def test_build_insert_query_exceeds_limit():
    """Test that the function raises ValueError when the number of values exceeds the maximum limit."""
    with pytest.raises(ValueError, match="Number of values exceeds the maximum limit"):
        build_insert_query(
            TABLE_NAME,
            ["Id", "Value"],
            [(1, "Value1")] * (MAX_INSERT_LIMIT + 1)
        )


def test_build_insert_query_column_mismatch():
    """Test that the function raises ValueError when the number of columns do not match the number of args provided."""
    with pytest.raises(ValueError, match="Number of columns does not match the number of args provided!"):
        build_insert_query(TABLE_NAME, ["Id", "Value"], [
                           (1, "Value1"), (2,)])


def test_build_insert_query():
    """Test that the function returns the correct query."""
    sql_query = build_insert_query(
        TABLE_NAME,
        ["Id", "Value"],
        [(1, "Value1"), (2, "Value2")]
    )
    expected_query = f"INSERT INTO {TABLE_NAME} (Id, Value) VALUES (1, 'Value1'), (2, 'Value2');"
    assert sql_query == expected_query


def test_columns_not_provided():
    """Test that the function raises TypeError when column names are not provided."""
    with pytest.raises(TypeError):
        build_insert_query(TABLE_NAME, [(1, "Value1"), (2, "Value2")])


def test_values_not_provided():
    """Test that the function raises TypeError when values to be inserted are not provided."""
    with pytest.raises(TypeError):
        build_insert_query(TABLE_NAME, ["Id", "Value"])
