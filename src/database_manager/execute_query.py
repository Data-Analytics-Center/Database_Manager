"""Defines all the query builders for all database operations."""

from .connection_manager import execute_query
from sqlalchemy import engine, text


# TODO: add return type - figure it out
def execute_raw_select(
    engine: engine,
    table: str,
    top: int = None,
    cols: list = ["*"],
    where: str = None,
) -> None:
    """Execute a SQL select operation using SQLAlchemy.

    Arguments:
        engine: Engine object.
        table (str, optional): Table to select from. Defaults to None.
        top (int, optional): Number of rows to select. Defaults to None, selecting all rows.
        cols (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.

    Raises:
        ValueError: If database name is not provided.

    Returns:
        A Pyodbc cursor object.
    """
    if table is None:
        raise Exception("Table name is required.")

    query = f"""SELECT {", ".join(cols)} FROM {table}"""

    if top is not None:
        query += f" TOP={top}"

    if where is not None:
        query += f" WHERE {where}"

    with engine.begin() as connection:
        results = connection.execute(text(query))
    return results


# TODO add pandas dataframe return type
def execute_pandas_select(
    engine: engine,
    table: str,
    top: int = None,
    cols: list = ["*"],
    where: str = None,
) -> None:
    """Select data from a table using pandas.

    Arguments:
        engine: Engine object.
        table (str, optional): Table to select from. Defaults to None.
        top (int, optional): Number of rows to select. Defaults to None, selecting all rows.
        cols (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.

    Raises:
        ValueError: If database name is not provided.

    Returns:
        A pandas dataframe.
    """
    if table is None:
        raise ValueError("Table name parameter is None")

    query = f"""SELECT {", ".join(cols)} FROM {table}"""

    if top is not None:
        query += f" TOP={top}"

    if where is not None:
        query += f" WHERE {where}"

    # TODO: Brandon switch for pandas
    with engine.begin() as connection:
        results = connection.execute(text(query))
    return results


def bulk_pandas_insert():
    pass


def bulk_raw_insert():
    pass


def single_insert(engine: engine, table: str, columns: list, *values) -> None:
    """Insert a single row into a specified table.

    Arguments:
        engine: Engine object.
        table: The name of the table where the insertion will be performed.
        columns: List of column names in the table.
        values: Values to be inserted into corresponding columns.

    Raises:
        ValueError: If the database name, table name, or columns list is not provided,
            or if the number of columns does not match the number of arguments provided.
    """
    if not table:
        raise ValueError("The table name is not provided!")
    if not columns:
        raise ValueError("At least one column is required!")
    if len(columns) != len(values):
        raise ValueError(
            "Number of columns does not match the number of args provided!"
        )

    column_string = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in values])
    query = f"""INSERT INTO {table} ({column_string}) VALUES ({placeholders});"""

    execute_query(engine, query, values)
