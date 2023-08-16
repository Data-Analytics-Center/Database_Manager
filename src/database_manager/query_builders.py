"""Defines all the query builders for all database operations."""

from .connection_manager import create_connection, execute_query
from sqlalchemy import engine


def simple_select(
    engine: engine,
    database: str = None,
    table: str = None,
    top: int = None,
    cols: list = ["*"],
    where: str = None,
    group_by: str = None,
    order_by: str = None,
) -> None:
    """Selects data from a table.

    Args:
        engine (engine): engine object.
        table (str, optional): Table to select from. Defaults to None.
        top (int, optional): Number of rows to select. Defaults to None, selecting all rows.
        cols (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.

    Raises:
        ValueError: If database name is not provided.

    Returns:
        None
    """
    if database is None:
        raise ValueError("Database name is required.")

    if table is None:
        raise Exception("Table name is required.")

    query = f"""SELECT {", ".join(cols)} FROM {table}"""

    if where is not None:
        query += f" WHERE {where}"

    if group_by is not None:
        query += f" GROUP BY {group_by}"

    if order_by is not None:
        query += f" ORDER BY {order_by}"

    if top is not None:
        query += f" LIMIT {top}"

    execute_query(engine, query)

def simple_insert(
    engine: engine, database: str, table: str, columns: list, *args
) -> None:
    """
    Insert a single row into a specified table.

    Args:
        database (str): The name of the database to connect to.
        table (str): The name of the table where the insertion will be performed.
        columns (list): List of column names in the table.
        *args: Values to be inserted into corresponding columns.

    Raises:
        ValueError: If the database name, table name, or columns list is not provided,
            or if the number of columns does not match the number of arguments provided.
    """

    if not database:
        raise ValueError("The database name is not provided!")
    if not table:
        raise ValueError("The table name is not provided!")
    if not columns:
        raise ValueError("At least one column is required!")
    if len(columns) != len(args):
        raise ValueError(
            f"Number of columns does not match the number of args provided!"
        )

    conn = create_connection(engine, database)
    if not conn:
        raise Exception(f"The connection was not formed with this database: {database}")

    column_string = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in args])
    query = f"""INSERT INTO {table} ({column_string}) VALUES ({placeholders});"""

    conn.execute(query)
    conn.commit()
