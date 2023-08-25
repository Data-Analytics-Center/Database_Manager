"""Defines all the query builders for all database operations."""

from sqlalchemy import CursorResult, Engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .connection_manager import create_engine, InsertType

""" TODO:
    - Add logging
    - add docstrings
    - test
"""


def validate_engine(engine: Engine) -> None:
    """Validate an engine object was initialized properly.

    Arguments:
        engine (Engine): Engine object to validate.
    """
    if engine is None:
        raise ValueError("Engine is None")
    if not isinstance(engine, Engine):
        raise ValueError("Engine is not of type engine")


def validate_sql(sql: str) -> None:
    """Validate a SQL query is not garbage.

    Arguments:
        sql (str): SQL query to validate.
    """
    if sql is None:
        raise ValueError("SQL is None")
    if sql == "":
        raise ValueError("SQL is empty")
    if sql.isspace():
        raise ValueError("SQL is whitespace")


def execute_raw_select(sql: str) -> CursorResult:
    """Create and engine and executes a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.

    Returns:
        CursorResult: Results of the query.
    """
    engine = create_engine()

    validate_engine(engine)
    validate_sql(sql)

    session_initializer = sessionmaker(bind=engine)
    with session_initializer() as session:
        results = session.execute(text(sql)).fetchall()
    return results


def execute_pandas_select(
    sql: str,
) -> pd.DataFrame:
    """Create an engine and executes a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.

    Returns:
        DataFrame: Results of the query.
    """
    engine = create_engine()

    validate_engine(engine)
    validate_sql(sql)

    dataframe = pd.read_sql(sql, engine)
    return dataframe


def execute_raw_insert(
    columns: list, *values, insert_type: InsertType = InsertType.BULK_INSERT
):
    engine = create_engine(insert_type)
    validate_engine(engine)

    if not columns:
        raise ValueError("At least one column is required!")
    if len(columns) != len(values):
        raise ValueError(
            "Number of columns does not match the number of args provided!"
        )


def pandas_insert(table: str, columns: list, *values, bulk=InsertType.BULK_INSERT):
    pass


def execute_single_insert(engine: Engine, table: str, columns: list, *values) -> None:
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
