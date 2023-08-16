from .connection_manager import create_connection

"""Defines all the query builders for all database operations."""


def simple_insert(database: str, table: str, columns: list, *args) -> None:
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

    conn = create_connection(database)
    if not conn:
        raise Exception(f"The connection was not formed with this database: {database}")

    column_string = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in args])
    query = f"""INSERT INTO {table} ({column_string}) VALUES ({placeholders});"""

    conn.execute(query)
    conn.commit()
