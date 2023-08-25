"""Defines all the query builders for all database operations."""

from sqlalchemy import CursorResult, Engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .connection_manager import create_engine, create_bulk_insert_engine
from enum import Enum
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")
driver = os.getenv("DRIVER")
table = os.getenv("TABLE")


class Insert_Engine(Enum):
    """Enum to define the type of engine to create."""

    BULK_INSERT = 1
    SINGLE_INSERT = 2


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
def execute_raw_select(sql: str) -> CursorResult:
    """Creates and engine and executes a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.

    Returns:
        Results of the query.
    """
    engine = create_engine(server, database, driver)

    validate_engine(engine)
    validate_sql(sql)

    Session = sessionmaker(bind=engine)
    with Session() as session:
        results = session.execute(text(sql)).fetchall()
    return results


# TODO: Log the error instead of printing it.
def execute_pandas_select(
    sql: str,
) -> pd.DataFrame:
    """Creates an engine and executes a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.

    Returns:
        Results of the query as a pandas DataFrame.
    """
    engine = create_engine(server, database, driver)

    validate_engine(engine)
    validate_sql(sql)

    df = pd.read_sql(sql, engine)
    return df


def raw_insert(columns: list, *values, bulk=Insert_Engine.BULK_INSERT):
    if bulk == Insert_Engine.BULK_INSERT:
        engine = create_bulk_insert_engine(server, database, driver)
    elif bulk == Insert_Engine.SINGLE_INSERT:
        engine = create_engine(server, database, driver)
    else:
        raise ValueError("Invalid bulk insert type")

    validate_engine(engine)

    if not table:
        raise ValueError("The table name is not provided!")
    if not columns:
        raise ValueError("At least one column is required!")
    if len(columns) != len(values):
        raise ValueError(
            "Number of columns does not match the number of args provided!"
        )


def pandas_insert(table: str, columns: list, *values, bulk=Insert_Engine.BULK_INSERT):
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
