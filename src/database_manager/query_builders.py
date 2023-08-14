"""Defines all the query builders for all database operations."""

from .connection_manager import create_connection, execute

def select(
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
        table (str, optional): Table to select from. Defaults to None.
        top (int, optional): Number of rows to select. Defaults to None, selecting all rows.
        cols (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.
    """
    if database is None:
        raise Exception("Database name is required.")

    try:
        conn = create_connection(database)
    except Exception as e:
        raise Exception(f"Error creating connection to database: {e}")

    if table is None:
        raise Exception("Table name is required.")

    query = f"SELECT {', '.join(cols)} FROM {table}"

    if where is not None:
        query += f" WHERE {where}"

    if group_by is not None:
        query += f" GROUP BY {group_by}"

    if order_by is not None:
        query += f" ORDER BY {order_by}"

    if top is not None:
        query += f" LIMIT {top}"

    execute(conn, query)
