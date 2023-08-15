"""Contains database connection and execution logic."""

import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection


def create_connection() -> Connection:
    """Create a connection object to a database.

    This function creates a SQLAlchemy engine connection object to a database. 
    It relies on environment variables for the connection parameters, 
    including the driver, server, database, and environment type.

    Environment Variables:
        - `ENV_TYPE`: The environment type (e.g., 'DEV', 'PROD', 'TEST').
        - `DATABASE`: The name of the database to connect to.
        - `{ENV_TYPE}_DRIVER`: The driver for the connection (e.g., 'ODBC Driver 17 for SQL Server').
        - `{ENV_TYPE}_SERVER`: The server name or address for the connection.

    Returns:
        Connection: A SQLAlchemy engine connection object.

    Raises:
        ValueError: If any of the required environment variables are empty or not set.

    Example:
        To use this function, set the environment variables and then call `create_connection()`:
        ```python
        import os
        os.environ['ENV_TYPE'] = 'development'
        os.environ['DATABASE'] = 'my_database'
        os.environ['development_DRIVER'] = 'ODBC Driver 17 for SQL Server'
        os.environ['development_SERVER'] = 'my_server_address'
        
        connection = create_connection()
        ```
    """
    environment_type = os.environ.get('ENV_TYPE')
    database = os.environ.get('DATABASE')
    driver = os.environ.get(f'{environment_type}_DRIVER')
    server = os.environ.get(f'{environment_type}_SERVER')
    
    if database is None or database == '':
        raise ValueError('Database name cannot be empty.')
    if driver is None or driver == '':
        raise ValueError('Driver cannot be empty.')
    if server is None or server == '':
        raise ValueError('Server cannot be empty.')
    if environment_type is None or environment_type == '':
        raise ValueError('Environment type cannot be empty.')
    
    connection_string = f"mssql://@{server}/{database}?driver={driver}&Encrypt=no"
    engine = create_engine(connection_string)
    return engine.begin()



def execute_query(connection: Connection, query: str, values:tuple[any, ...]=None) -> None:
    """Execute an SQL query.

    Arguments:
        connection: The connnection object to the database.
        query: The query to execute.
        values: The values to pass to the query if any.

    Raises:
        Exception: If anything goes wrong with the database transaction.
    """
    try:
        if values is not None:
            connection.execute(text(query), **values)
        else:
            connection.execute(text(query))
    except Exception as e:
        print(e)
        raise e
    finally:
        connection.close()
