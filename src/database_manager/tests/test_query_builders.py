"""Used to test that the package builds and installs correctly, run after building th eproject and installing the package."""

import pytest
from src.database_manager.query_builders import build_insert_query, build_select_query

TABLE_NAME = "test"
MAX_INSERT_LIMIT = 80000


def test_build_select_query_invalid_table():
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query("", cols=["Id"])
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query(" ", cols=["Id"])
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query(None, cols=["Id"])


def test_build_select_query_no_table():
    with pytest.raises(TypeError):
        build_select_query(cols=["Id"])
    with pytest.raises(TypeError):
        build_select_query(cols=["Id"], where="Id = 5")


def test_build_select_query_default_args():
    sql_query = build_select_query(table=TABLE_NAME)
    expected_query = f"SELECT * FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_with_all_args_provided():
    sql_query = build_select_query(
        table=TABLE_NAME,
        top=100,
        cols=["Id", "Value"],
        where="Id = 5",
        group_by="Id",
        order_by="Value DESC",
    )
    expected_query = (
        f"SELECT TOP 100 Id, Value FROM {TABLE_NAME} WHERE Id = 5 GROUP BY Id ORDER BY Value DESC"
    )
    assert sql_query == expected_query


def test_build_select_query_no_top():
    sql_query = build_select_query(table=TABLE_NAME, cols=["Id"])
    expected_query = f"SELECT Id FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_cols():
    sql_query = build_select_query(table=TABLE_NAME, top=10)
    expected_query = f"SELECT TOP 10 * FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_where():
    sql_query = build_select_query(table=TABLE_NAME, cols=["Id", "Value"])
    expected_query = f"SELECT Id, Value FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_group_by():
    sql_query = build_select_query(table=TABLE_NAME, cols=[
                                   "Id"], where="Id > 5")
    expected_query = f"SELECT Id FROM {TABLE_NAME} WHERE Id > 5"
    assert sql_query == expected_query


def test_build_select_query_no_order_by():
    sql_query = build_select_query(table=TABLE_NAME, cols=[
                                   "Id"], order_by="Id ASC")
    expected_query = f"SELECT Id FROM {TABLE_NAME} ORDER BY Id ASC"
    assert sql_query == expected_query


def test_build_insert_query_invalid_table():
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
    with pytest.raises(TypeError):
        build_insert_query(["Id", "Values"], [(1, "Value1"), (2, "Value2")])


def test_build_insert_query_no_columns():
    with pytest.raises(ValueError, match="At least one column is required!"):
        build_insert_query(TABLE_NAME, [], [(1, "Value1"), (2, "Value2")])


def test_build_insert_query_exceeds_limit():
    with pytest.raises(ValueError, match="Number of values exceeds the maximum limit"):
        build_insert_query(
            TABLE_NAME,
            ["Id", "Value"],
            [(1, "Value1")] * (MAX_INSERT_LIMIT + 1)
        )


def test_build_insert_query_column_mismatch():
    with pytest.raises(ValueError, match="Number of columns does not match the number of args provided!"):
        build_insert_query(TABLE_NAME, ["Id", "Value"], [
                           (1, "Value1"), (2,)])


def test_build_insert_query():
    sql_query = build_insert_query(
        TABLE_NAME,
        ["Id", "Value"],
        [(1, "Value1"), (2, "Value2")]
    )
    expected_query = f"INSERT INTO {TABLE_NAME} (Id, Value) VALUES (1, 'Value1'), (2, 'Value2');"
    assert sql_query == expected_query


def test_columns_not_provided():
    with pytest.raises(TypeError):
        build_insert_query(TABLE_NAME, [(1, "Value1"), (2, "Value2")])
