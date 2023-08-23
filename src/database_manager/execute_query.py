"""Defines all the query builders for all database operations."""

from sqlalchemy import CursorResult, Engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .connection_manager import create_engine, create_bulk_engine


def validate_engine(engine: Engine) -> None:
    if engine is None:
        raise ValueError("Engine is None")
    if not isinstance(engine, Engine):
        raise ValueError("Engine is not of type engine")


def validate_sql(sql: str) -> None:
    if sql is None:
        raise ValueError("SQL is None")
    if sql == "":
        raise ValueError("SQL is empty")
    if sql.isspace():
        raise ValueError("SQL is whitespace")


# TODO: Log the error instead of printing it.
# TODO: Create engine
def execute_raw_select(engine: Engine, sql: str) -> CursorResult:
    """Execute a SQL select operation using SQLAlchemy.

    Arguments:
        engine: Engine object.
        sql (str): SQL query to execute.

    Returns:
        Results of the query.
    """
    try:
        validate_engine(engine)
    except ValueError as e:
        print(e)

    try:
        validate_sql(sql)
    except ValueError as e:
        print(e)

    Session = sessionmaker(bind=engine)
    with Session() as session:
        results = session.execute(text(sql)).fetchall()
    return results


# TODO: Log the error instead of printing it.
def execute_pandas_select(
    engine: Engine,
    sql: str,
) -> pd.DataFrame:
    """Execute a SQL select operation using SQLAlchemy.

    Arguments:
        engine: Engine object.
        sql (str): SQL query to execute.

    Returns:
        Results of the query as a pandas DataFrame.
    """
    try:
        validate_engine(engine)
    except ValueError as e:
        print(e)

    try:
        validate_sql(sql)
    except ValueError as e:
        print(e)

    df = pd.read_sql(sql, engine)
    return df


def bulk_pandas_insert():
    pass


def bulk_raw_insert():
    pass


def single_insert(engine: Engine, table: str, columns: list, *values) -> None:
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
