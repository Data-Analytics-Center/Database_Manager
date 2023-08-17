"""Contains database connection and execution logic."""

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy import engine


def create_engine(
    server: str, database: list, driver: str, bulk_insert: bool  # noqa: FBT001
) -> engine:
    """Create a connection object to a database.

    This function creates a SQLAlchemy engine connection object to a database.
    It relies on environment variables for the connection parameters,
    including the driver, server, database, and environment type.

    Arguments:
        driver: The driver that connects to the database.
        server: The name of the database server.
        database: The database to connect to.
        bulk_insert: True if engine is for bulk inserts only

    Returns:
        Connection: A SQLAlchemy engine connection object.

    Raises:
        ValueError: If any of the parameters are empty or not set.

    Example:
        To use this function, set the environment variables and then call `create_connection()`:
        ```python
        import os
        os.environ['DATABASE'] = 'my_database'
        os.environ['development_DRIVER'] = 'ODBC Driver 17 for SQL Server'
        os.environ['development_SERVER'] = 'my_server_address'

        connection = create_connection(server, database, driver)
        ```
    """
    if database is None or database == "":
        raise ValueError("Database parameter cannot be None or empty.")
    if driver is None or driver == "":
        raise ValueError("Driver parameter cannot be None or empty.")
    if server is None or server == "":
        raise ValueError("Server parameter cannot be None or empty.")

    connection_string = (
        f"mssql+pyodbc://@{server}/{database}?driver={driver}&Encrypt=no"
    )
    engine = (
        sqlalchemy_create_engine(connection_string, fast_executemany=True)
        if bulk_insert
        else sqlalchemy_create_engine(connection_string)
    )
    return engine


def execute_query(engine: engine, query: str, values: tuple[any, ...] = None) -> None:
    """Execute an SQL query.

    Arguments:
        engine: The engine object to connect to the database.
        query: The query to execute.
        values: The values to pass to the query if any.

    Returns:
        last_id: The id of the last row inserted.

    Raises:
        Exception: If anything goes wrong with the database transaction.
        ValueError: If the engine or query is not set.
    """
    if engine is None:
        raise ValueError("Engine cannot be None.")
    if query is None or query == "":
        raise ValueError("Query cannot be None or empty.")

    with engine.begin() as connection:
        if values:
            connection.execute(query, values)
        else:
            connection.execute(query)
