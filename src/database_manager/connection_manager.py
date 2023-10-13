"""Contains database connection logic."""


import os
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine


def engine_factory(database: str = None, *, is_bulk_insert: bool = False) -> Engine:
    """Create an engine object for connecting to a database.

    This function creates a SQLAlchemy Engine connection object to a database.
    It relies on environment variables for the connection parameters,
    including the driver, server, database, and environment type. Database can be
    passed as a parameter to this function, or it can be set as an environment variable.
    Environment variables are loaded from a .env file in the root directory of the project.


    Args:
        database (str): The name of the database to connect to.
        is_bulk_insert (bool): Whether or not to use fast_executemany for bulk inserts.


    !!! tip "Environment Variables"
        driver (str): The driver that connects to the database.

        server (str): The name of the database server.

        database (str, optional): The database to connect to. Can be passed in as a parameter.

    Returns:
        engine (Engine): A SQLAlchemy Engine object.

    Raises:
        ValueError: If any of the environment variables are not set properly.

    Example:
        To just get a SQLAlchemy Engine object, call `create_engine()`:
        ```python
        from Database_Manager import engine_factory

        engine = engine_factory()

        with engine.begin() as connection:
            result = connection.execute("SELECT 1")
            print(result.fetchone())

        with engine.begin() as connection:
            dataframe = pd.read_sql("SELECT 1", connection)
        ```
    """
    load_dotenv()

    server = os.getenv("SERVER")

    driver = os.getenv("DRIVER")

    if database is None or database == "" or database.isspace():
        database = os.getenv("DATABASE")

    if database is None or database == "" or database.isspace():
        raise ValueError(
            "DATABASE is not set please specify a database as an execute function parameter or environment variable."
        )

    if driver is None or driver == "" or driver.isspace():
        raise ValueError("DRIVER environment variable is not properly set.")

    if server is None or server == "" or server.isspace():
        raise ValueError("SERVER environment variable is not properly set.")

    env_type = os.getenv("ENV_TYPE")

    if env_type is None or env_type == "" or env_type.isspace():
        raise ValueError("ENV_TYPE environment variable is not properly set.")

    if env_type == "PROD":
        uid = os.getenv("UID")
        pid = os.getenv("PID")

        if uid is None or uid == "" or uid.isspace():
            raise ValueError("UID environment variable is not properly set.")
        if pid is None or pid == "" or pid.isspace():
            raise ValueError("PID environment variable is not properly set.")

        connection_string = f"mssql+pyodbc://{uid}:{urllib.parse.quote_plus(pid)}@{server}/{database}?driver={urllib.parse.quote_plus(driver)}&Encrypt=no"

    else:
        connection_string = (
            f"mssql+pyodbc://@{server}/{database}?driver={driver}&Encrypt=no"
        )

    engine = (
        create_engine(connection_string, fast_executemany=True)
        if is_bulk_insert
        else create_engine(connection_string)
    )
    return engine
