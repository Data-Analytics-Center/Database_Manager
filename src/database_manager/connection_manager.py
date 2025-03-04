"""Contains database connection logic."""

import os
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine


def engine_factory(
    rdbms: str = None,
    server: str = None,
    database: str = None,
) -> Engine:
    """Create an engine object for connecting to a database.

    This function creates a SQLAlchemy Engine connection object to a database.
    It relies on environment variables for the connection parameters.
    UID and PID are always required, while RDBMS, SERVER, and DATABASE are optional.
    If the optional parameters are not set as environment variables, they have to be passed in as function parameters.


    Args:
        rdbms (str): The flavor of rdbms. Valid value options = ['mssql','mysql','postgres','sqlite']
        server (str): The name of the server to connect to. In many RDBMS environments this is congruous with the concept of an RDBMS instance. This can come int the form of IP or servername, and may also include a port specification.
        database (str): The name of the database to connect to.


    !!! info "Enviroment Variables"
        **Always Required**

        ***UID:*** the username of the user to connect as

        ***PID:*** the password of the user to connect as

        --------------------------------------------

        **Optional**

        ***RDBMS:*** the type of RDBMS to connect to (can be set as environment variable or passed in as a parameter)

        ***SERVER:*** the server to connect to (can be set as environment variable or passed in as a parameter) NOTE: For rdbms = 'sqlite' this corresponds to the full path where the sqlite db file is located

        ***DATABASE:*** the database to connect to (can be set as environment variable or passed in as a parameter) NOTE: For rdbms = 'sqlite' this corresponds to the file name of the sqlite db file

        ***MSSQL_DRIVER:*** the MSSQL Driver to use. Will only be considered if rdbms is 'mssql'. If specified, takes precedence over pymssql.

    Returns:
        engine (Engine): A SQLAlchemy Engine object.

    Raises:
        ValueError: If any of the environment variables are not set properly and no alternative value was passed in by the caller.

    Example:
        To just get a SQLAlchemy Engine object, call `engine_factory()`:
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

    uid = os.getenv("UID")
    pid = os.getenv("PID")

    if uid is None or uid == "" or uid.isspace():
        raise ValueError("UID environment variable is not properly set.")
    if pid is None or pid == "" or pid.isspace():
        raise ValueError("PID environment variable is not properly set.")

    if rdbms is None or rdbms == "" or rdbms.isspace():
        rdbms = os.getenv("RDBMS")

    if rdbms is None or rdbms == "" or rdbms.isspace():
        raise ValueError("RDBMS is not set please specify a RDBMS as an execute function parameter or environment variable.")

    if server is None or server == "" or server.isspace():
        server = os.getenv("SERVER")

    if server is None or server == "" or server.isspace():
        raise ValueError(
            "SERVER is not set please specify a server as an execute function parameter or environment variable."
        )

    if database is None or database == "" or database.isspace():
        database = os.getenv("DATABASE")

    if database is None or database == "" or database.isspace():
        raise ValueError(
            "DATABASE is not set please specify a database as an execute function parameter or environment variable."
        )

    match rdbms:
        case "mssql":
            mssql_driver = os.getenv("MSSQL_DRIVER")
            if mssql_driver:
                connection_string = f"mssql+pyodbc://{uid}:{urllib.parse.quote_plus(pid)}@{server}/{database}?driver={mssql_driver}&TrustServerCertificate=yes"
            else:
                connection_string = f"mssql+pymssql://{uid}:{urllib.parse.quote_plus(pid)}@{server}/{database}"
        case "mysql":
            connection_string = f"mysql+pymysql://{uid}:{urllib.parse.quote_plus(pid)}@{server}/{database}"
        case "postgres":
            connection_string = f"postgresql+psycopg2://{uid}:{urllib.parse.quote_plus(pid)}@{server}/{database}"
        case "sqlite":
            connection_string = f"sqlite:///{server}/{database}"
        case _:
            raise ValueError("Invalid rdbms specified! Valid options: 'mssql' | 'mysql' | 'postgres' | 'sqlite'")

    engine = create_engine(connection_string)
    return engine
