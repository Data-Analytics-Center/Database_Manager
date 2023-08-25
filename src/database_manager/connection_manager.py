"""Contains database connection logic."""

from enum import Enum
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine as sqlalchemy_create_engine
from sqlalchemy import Engine


class InsertType(Enum):
    """Enum to define the type of engine to create."""

    BULK_INSERT = 1
    SINGLE_INSERT = 2


def create_engine(insert_type: InsertType = None) -> Engine:  # noqa: FBT001
    """Create a connection object to a database.

    This function creates a SQLAlchemy Engine connection object to a database.
    It relies on environment variables for the connection parameters,
    including the driver, server, database, and environment type.

    Arguments:
        insert_type: True if Engine is for bulk inserts only

    Environment Variables:
        driver (str): The driver that connects to the database.
        server (str): The name of the database server.
        database (str): The database to connect to.

    Returns:
        Engine: A SQLAlchemy Engine object.

    Raises:
        ValueError: If any of the environment variables are not set properly.

    Example:
        To use this function, set the environment variables and then call `create_connection()`:
        ```python
        engine = create_engine()
        ```
    """
    load_dotenv()

    server = os.getenv("SERVER")
    database = os.getenv("DATABASE")
    driver = os.getenv("DRIVER")

    if database is None or database == "" or database.isspace():
        raise ValueError("Database environment variable is not properly set.")
    if driver is None or driver == "" or driver.isspace():
        raise ValueError("Driver environment variable is not properly set.")
    if server is None or server == "" or server.isspace():
        raise ValueError("Server environment variable is not properly set.")

    connection_string = (
        f"mssql+pyodbc://@{server}/{database}?driver={driver}&Encrypt=no"
    )
    if insert_type == InsertType.BULK_INSERT:
        engine = sqlalchemy_create_engine(connection_string, fast_executemany=True)
    else:
        engine = sqlalchemy_create_engine(connection_string)
    return engine
