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
MAX_INSERT_LIMIT = 80000

def validate_engine(engine: Engine) -> None:
    """Validate an engine object was initialized properly.

    Arguments:
        engine (Engine): Engine object to validate.

    Raises:
        ValueError: If engine is None.
        ValueError: If engine is not of type Engine.

    Returns:
        None
    """
    if engine is None:
        raise ValueError("Engine is None")
    if not isinstance(engine, Engine):
        raise ValueError("Object passed as engine is not of type Engine")


def validate_sql(sql: str) -> None:
    """Validate a SQL query is not garbage.

    Arguments:
        sql (str): SQL query to validate.

    Raises:
        ValueError: If sql is None.
        ValueError: If sql is empty.
        ValueError: If sql is whitespace.

    Returns:
        None
    """
    if sql is None:
        raise ValueError("SQL is None")
    if sql == "":
        raise ValueError("SQL is empty")
    if sql.isspace():
        raise ValueError("SQL is whitespace")


def execute_raw_select(sql: str) -> CursorResult:
    """Create an engine and execute a SQL select operation using SQLAlchemy.

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
    """Create an engine and execute a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.

    Returns:
        data_frame: Result of the query.
    """
    engine = create_engine()

    validate_engine(engine)
    validate_sql(sql)

    data_frame = pd.read_sql(sql, engine)
    return data_frame


def execute_raw_insert(sql: str, insert_type: InsertType = InsertType.BULK_INSERT) -> None:
    """Create an engine and execute a SQL insert operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.
        insert_type (InsertType, optional): Type of insert operation to execute. Defaults to InsertType.BULK_INSERT.

    Raises:
        ValueError: If insert_type is not of type InsertType.

    Returns:
        None
    """
    if not isinstance(insert_type, InsertType):
        raise ValueError("Insert type is not of type InsertType")
    
    engine = create_engine(insert_type)
    validate_engine(engine)

    session_initializer = sessionmaker(bind=engine)
    with session_initializer() as session:
        session.execute(text(sql))
        session.commit()


def execute_pandas_insert(table: str, data_frame: pd.DataFrame) -> None:
    """Create an engine and execute a SQL insert operation using SQLAlchemy.

    Arguments:
        table (str): Table to insert into.
        data_frame (pd.DataFrame): DataFrame to insert into the database.

    Raises:
        ValueError: If the DataFrame has more rows than the maximum insert limit.

    Returns:
        None
    """
    engine = create_engine()
    validate_engine(engine)

    if len(data_frame) > MAX_INSERT_LIMIT:
        raise ValueError(
            f"Size of DataFrame exceeds the maximum limit of {MAX_INSERT_LIMIT}"
        )

    data_frame.to_sql(table, engine, if_exists="append", index=False)
