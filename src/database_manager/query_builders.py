"""Defines all the query builders for all database operations."""

from .connection_manager import execute_query
from sqlalchemy import engine


def simple_select(
    conn: engine,
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
        conn (engine): Connection object.
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

    execute_query(conn, query)
