"""Contains database connection logic."""

import os
import urllib.parse
from enum import Enum

from dotenv import load_dotenv
from sqlalchemy import Engine
from sqlalchemy import create_engine as sqlalchemy_create_engine


class InsertType(Enum):
    """Enum to define the type of engine to create.

    Attributes:
        BULK_INSERT (int): Engine is for bulk inserts only.
        SINGLE_INSERT (int): Engine is for single inserts only.
    """

    BULK_INSERT = 1
    SINGLE_INSERT = 2


def create_engine(database: str = None, insert_type: InsertType = None) -> Engine:
    """Create a connection object to a database.

    This function creates a SQLAlchemy Engine connection object to a database.
    It relies on environment variables for the connection parameters,
    including the driver, server, database, and environment type. Database can be
    passed as a parameter to this function, or it can be set as an environment variable.

    Arguments:
        database (str): The name of the database to connect to.
        insert_type: True if Engine is for bulk inserts only

    !!! tip "Environment Variables"
        driver (str): The driver that connects to the database.

        server (str): The name of the database server.

        database (str): The database to connect to.

    Returns:
        engine (Engine): A SQLAlchemy Engine object.

    Raises:
        ValueError: If any of the environment variables are not set properly.

    Example:
        To just get a SQLAlchemy Engine object, call `create_engine()`:
        ```python
        engine = create_engine()
        ```
        If you want to execute a query, you can use the engine object to connect to the database:
        ```python
        with engine.connect() as conn:
            result = conn.execute("SELECT * FROM dbo.MyTable")

            for row in result:
                print(row)
        ```
    """
    load_dotenv()

    server = os.getenv("SERVER")
    if database is None or database == "" or database.isspace():
        database = os.getenv("DATABASE")
    driver = os.getenv("DRIVER")

    if database is None or database == "" or database.isspace():
        raise ValueError(
            "Database is not set please specify a database as an execute function parameter or environment variable."
        )
    if driver is None or driver == "" or driver.isspace():
        raise ValueError("Driver environment variable is not properly set.")
    if server is None or server == "" or server.isspace():
        raise ValueError("Server environment variable is not properly set.")

    env_type = os.getenv("ENV_TYPE")

    if env_type == "PROD":
        uid = os.getenv("UID")
        pid = os.getenv("PID")
        connection_string = f"mssql+pyodbc://{uid}:{urllib.parse.quote_plus(pid)}@{server}/{database}?driver={urllib.parse.quote_plus(driver)}&Encrypt=no"
    else:
        connection_string = (
            f"mssql+pyodbc://@{server}/{database}?driver={driver}&Encrypt=no"
        )

    if insert_type == InsertType.BULK_INSERT:
        engine = sqlalchemy_create_engine(connection_string, fast_executemany=True)
    else:
        engine = sqlalchemy_create_engine(connection_string)
    return engine
