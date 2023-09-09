"""Used to test that the package builds and installs correctly, run after building th eproject and installing the package."""

import pytest
from src.database_manager.query_builders import build_insert_query, build_select_query

TABLE_NAME = "test"


def test_build_select_query_invalid_table_name():
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query("", cols=["Id"])
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query(" ", cols=["Id"])
    with pytest.raises(ValueError, match="Table name is required."):
        build_select_query(None, cols=["Id"])
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
    sql_query = build_select_query(table=TABLE_NAME, cols=["Col1", "Col2"])
    expected_query = f"SELECT Col1, Col2 FROM {TABLE_NAME}"
    assert sql_query == expected_query


def test_build_select_query_no_group_by():
    sql_query = build_select_query(table=TABLE_NAME, cols=[
                                   "Col1"], where="Col1 > 5")
    expected_query = f"SELECT Col1 FROM {TABLE_NAME} WHERE Col1 > 5"
    assert sql_query == expected_query


def test_build_select_query_no_order_by():
    sql_query = build_select_query(table=TABLE_NAME, cols=[
                                   "Col1"], order_by="Col1 ASC")
    expected_query = f"SELECT Col1 FROM {TABLE_NAME} ORDER BY Col1 ASC"
    assert sql_query == expected_query
