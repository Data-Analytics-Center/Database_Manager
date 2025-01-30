"""Contains some helper functions for querying databases."""

import pandas as pd
from sqlalchemy import Select, Table

from .connection_manager import engine_factory


def insert_sql_pandas(
    df: pd.DataFrame,
    table: str | Table,
    rdbms: str = None,
    server: str = None,
    database: str = None,
    if_exists: str = "append",
    index: bool = False,
) -> None:
    """Insert a pandas DataFrame into a SQL table.

    Args:
        df (pd.DataFrame): The DataFrame to insert.
        table (str or Table): The table to insert the DataFrame into.
        rdbms (str): The type of RDBMS to connect to.
        server (str): The server to connect to.
        database (str): The name of the database to connect to.
        if_exists (str): What to do if the table already exists. Options are 'fail', 'replace', and 'append'.
        index (bool): Whether to write the DataFrame index as a column in the table.

    Raises:
        Exception: If an error occurs during the insert operation.
    """
    if not isinstance(table, str):
        raise ValueError("table must be a string or a Table object")
    table = table.name

    try:
        with engine_factory(rdbms=rdbms, server=server, database=database).begin() as connection:
            df.to_sql(table, connection, if_exists=if_exists, index=index)
    except Exception as e:
        raise e


def select_sql_pandas(sql: str | Select, rdbms: str = None, server: str = None, database: str = None) -> pd.DataFrame:
    """Select data from a SQL database and return it as a pandas DataFrame.

    Args:
        sql (str or Select): The SQL query to execute.
        rdbms (str): The type of RDBMS to connect to.
        server (str): The server to connect to.
        database (str): The name of the database to connect to.

    Returns:
        pd.DataFrame: The results of the query as a pandas DataFrame.

    Raises:
        Exception: If an error occurs during the select operation
    """
    try:
        with engine_factory(rdbms=rdbms, server=server, database=database).begin() as connection:
            results = pd.read_sql(sql, connection)
    except Exception as e:
        raise e
    return results
