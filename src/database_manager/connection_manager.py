"""Contains database connection and execution logic."""

from sqlalchemy import create_engine, text


def create_connection(driver: str, server: str, database: str):
    """Create a connection object to a database."""
    conn_string = f"Driver={driver};Server={server};Database={database};Trusted_Connection=yes;Encrypt=no;"
    engine = create_engine()
    # Brandon TODO: need to make sure this is the correct way
    return engine.begin(conn_string)


def execute_query(conn, sql, values=None):
    """Execute an SQL query."""
    # Brandon TODO: need to update properly
    conn.execute(text(sql))
    conn.close()

    conn.commit()


def simple_insert(database: str, table: str, columns: list, *args) -> None:
    """Insert a single row into a table"""
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
