"""Contains database connection and execution logic."""

from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection
import os

def create_connection() -> Connection:
    """Create a connection object to a database.

    The function relies on enviroment variables for the connection parameters
    Returns:
        A SQLAlchemy engine connection object.
    """
    environment_type = os.environ.get('ENV_TYPE')
    database = os.environ.get('DATABASE')
    driver = os.environ.get(f'{environment_type}_DRIVER', '')
    server = os.environ.get(f'{environment_type}_SERVER', '')
    
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


def execute_query(conn, sql, values=None):
    """Execute an SQL query."""
    # Brandon TODO: need to update properly
    conn.execute(text(sql))
    conn.close()
