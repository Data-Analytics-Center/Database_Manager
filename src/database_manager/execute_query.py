"""Defines all the query builders for all database operations."""

from .connection_manager import execute_query
from sqlalchemy import Engine, text

# from sqlalchemy.engine.result import ResultProxy


# TODO: is_instance() - engine type (find best way to do this)
def validate_engine(engine: Engine) -> None:
    if engine is None:
        raise ValueError("Engine is None")
    if not isinstance(engine, Engine):
        raise ValueError("Engine is not of type engine")


# TODO: not none, not empty, not whitespace
def validate_sql(sql: str) -> None:
    if sql is None:
        raise ValueError("SQL is None")
    if sql == "":
        raise ValueError("SQL is empty")
    if sql.isspace():
        raise ValueError("SQL is whitespace")


# TODO: add return type - figure it out
def execute_raw_select(engine: Engine, sql: str) -> str:
    """Execute a SQL select operation using SQLAlchemy.

    Arguments:
        engine: Engine object.
        sql (str): SQL query to execute.

    Returns:
        Results of the query.
    """
    try:
        vaildate_engine(engine)
    except ValueError as e:
        print(e)

    try:
        validate_sql(sql)
    except ValueError as e:
        print(e)

    with engine.begin() as connection:
        results = connection.execute(text(sql))
    return results


# TODO add pandas dataframe return type
def execute_pandas_select(
    engine: Engine,
    table: str,
    top: int = None,
    cols: list = ["*"],
    where: str = None,
) -> None:
    if table is None:
        raise ValueError("Table name parameter is None")

    query = f"""SELECT {", ".join(cols)} FROM {table}"""

    if top is not None:
        query += f" TOP={top}"

    if where is not None:
        query += f" WHERE {where}"

    # TODO: Brandon switch for pandas
    with engine.begin() as connection:
        results = connection.execute(text(query))
    return results


def single_insert(engine: Engine, table: str, columns: list, *values) -> None:
    """Insert a single row into a specified table.

    Arguments:
        engine: Engine object.
        table: The name of the table where the insertion will be performed.
        columns: List of column names in the table.
        values: Values to be inserted into corresponding columns.

    Raises:
        ValueError: If the database name, table name, or columns list is not provided,
            or if the number of columns does not match the number of arguments provided.
    """
    if not table:
        raise ValueError("The table name is not provided!")
    if not columns:
        raise ValueError("At least one column is required!")
    if len(columns) != len(values):
        raise ValueError(
            "Number of columns does not match the number of args provided!"
        )

    column_string = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in values])
    query = f"""INSERT INTO {table} ({column_string}) VALUES ({placeholders});"""

    execute_query(engine, query, values)
