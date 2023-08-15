"""Contains database connection and execution logic."""

from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Connection


def create_connection(driver: str, server: str, database: str) -> Connection:
    """Create a connection object to a database.

    Arguments:
        driver: The driver that connects to the database.
        server: The name of the database server.
        database: The database to connect to.

    Returns:
        A SQLAlchemy engine connection object.
    """
    params = {'Driver': driver, 'Server': server, 'Database': database}
    
    for name, value in params.items():
        if value is None or value == "":
            raise ValueError(f"{name} cannot be None or empty")
    
    connection_string = f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;Encrypt=no;"
    engine = create_engine(connection_string)
    return engine.begin()



def execute_query(connection: Connection, query: str, values:tuple[any, ...]=None) -> None:
    """Execute an SQL query.

    Arguments:
        connection: The connnection object to the database.
        query: The query to execute.
        values: The values to pass to the query if any.
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
