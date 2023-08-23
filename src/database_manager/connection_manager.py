"""Contains database connection and execution logic."""

from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy import Engine


def create_engine(server: str, database: list, driver: str) -> Engine:  # noqa: FBT001
    """Create a connection object to a database.

    This function creates a SQLAlchemy Engine connection object to a database.
    It relies on environment variables for the connection parameters,
    including the driver, server, database, and environment type.

    Arguments:
        driver: The driver that connects to the database.
        server: The name of the database server.
        database: The database to connect to.
        bulk_insert: True if Engine is for bulk inserts only

    Returns:
        Connection: A SQLAlchemy Engine connection object.

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
    engine = sqlalchemy_create_engine(connection_string)
    return engine


def create_bulk_engine(server: str, database: list, driver: str):
    """Create a connection object to a database.

    This function creates a SQLAlchemy Engine connection object to a database.
    It relies on environment variables for the connection parameters,
    including the driver, server, database, and environment type.

    Arguments:
        driver: The driver that connects to the database.
        server: The name of the database server.
        database: The database to connect to.
        bulk_insert: True if Engine is for bulk inserts only

    Returns:
        Connection: A SQLAlchemy Engine connection object.

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
        raise ValueError("Database name cannot be empty.")
    if driver is None or driver == "":
        raise ValueError("Driver cannot be empty.")
    if server is None or server == "":
        raise ValueError("Server cannot be empty.")

    connection_string = (
        f"mssql+pyodbc://@{server}/{database}?driver={driver}&Encrypt=no"
    )
    engine = sqlalchemy_create_engine(connection_string, fast_executemany=True)
    return engine
