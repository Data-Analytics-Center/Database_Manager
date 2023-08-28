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

def _validate_engine(engine: Engine) -> None:
    """Validate an engine object was initialized properly.

    Arguments:
        engine (Engine): Engine object to validate.
    """
    if engine is None:
        raise ValueError("Engine is None")
    if not isinstance(engine, Engine):
        raise ValueError("Object passed as engine is not of type Engine")


def _validate_sql(sql: str) -> None:
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
    """Create an engine and execute a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.

    Returns:
        CursorResult: Results of the query.
    """
    engine = create_engine()

    _validate_engine(engine)
    _validate_sql(sql)

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

    _validate_engine(engine)
    _validate_sql(sql)

    dataframe = pd.read_sql(sql, engine)
    return dataframe


def execute_raw_insert(sql: str, insert_type: InsertType = InsertType.BULK_INSERT):
    """Create an engine and executes a SQL insert operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.
        insert_type (InsertType, optional): Type of insert operation to execute. Defaults to InsertType.BULK_INSERT.
        

    Raises:
        ValueError: If insert_type is not of type InsertType.
    

    Returns:
        None
    """
    engine = create_engine(insert_type)
    _validate_engine(engine)

    session_initializer = sessionmaker(bind=engine)
    with session_initializer() as session:
        session.execute(text(sql))
        session.commit()


def execute_pandas_insert(df: pd.DataFrame):
    """Create an engine and executes a SQL insert operation using SQLAlchemy.

    Arguments:
        df (DataFrame): DataFrame to insert into the database.
        insert_type (InsertType, optional): Type of insert operation to execute. Defaults to InsertType.BULK_INSERT.

    Raises:
        ValueError: If insert_type is not of type InsertType.


    Returns:
        None
    """
    engine = create_engine(InsertType.BULK_INSERT)
    _validate_engine(engine)

    if len(df) > MAX_INSERT_LIMIT:
        raise ValueError(
            f"DataFrame has {len(df)} rows, which is greater than the maximum insert limit of {MAX_INSERT_LIMIT}."
        )

    df.to_sql("test", engine, if_exists="append", index=False)
