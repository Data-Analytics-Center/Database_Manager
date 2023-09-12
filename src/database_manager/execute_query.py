"""Execute Queries module.

Each function is a different way to execute a SQL query using SQLAlchemy.
For each SQL operation we offer a pandas function and a raw function
"""

import pandas as pd
from sqlalchemy import Engine, text
from sqlalchemy.orm import sessionmaker

from .connection_manager import InsertType, create_engine

""" TODO:
    - Add logging
"""
MAX_INSERT_LIMIT = 80000


def validate_engine(engine: Engine) -> None:
    """Validate an engine object was initialized properly.

    Arguments:
        engine (Engine): Engine object to validate.

    Raises:
        ValueError: If engine is None.
        ValueError: If engine is not of type Engine.

    Returns:
        None

    Examples:
        To use this function, call `validate_engine()`:
        ```python
        engine = create_engine()
        validate_engine(engine)
        ```
    """
    if engine is None:
        raise ValueError("Engine is None")
    if not isinstance(engine, Engine):
        raise ValueError("Object passed as engine is not of type Engine")


def validate_sql(sql: str) -> None:
    """Validate a SQL query is not garbage.

    Arguments:
        sql (str): SQL query to validate.

    Raises:
        ValueError: If sql is None.
        ValueError: If sql is empty.
        ValueError: If sql is whitespace.

    Returns:
        None

    Examples:
        To use this function, call `validate_sql()`:
        ```python
        sql = "SELECT * FROM table"
        validate_sql(sql)
        ```

        To use this function with a query built using `build_select_query()`:
        ```python
        table = "table"
        sql = build_select_query(table, top=10, cols=["id", "name"])
        validate_sql(sql)
        ```
    """
    if sql is None:
        raise ValueError("SQL is None")
    if sql == "":
        raise ValueError("SQL is empty")
    if sql.isspace():
        raise ValueError("SQL is whitespace")


def execute_raw_select(sql: str, database: str = None) -> list[tuple]:
    """Create an engine and execute a SQL select operation using SQLAlchemy, returning a list of tuples.

    Arguments:
        sql (str): SQL query to execute.
        database (str, optional): Database to connect to. Defaults to None. Can be set as an environment variable.

    Returns:
        results (list[tuple]): Result of the query.

    Examples:
        To use this function with a custom sql query:
        ```python
        sql = "SELECT * FROM table"
        results = execute_raw_select(sql)
        ```

        To use this function with a query built using `build_select_query()`:
        ```python
        table = "table"
        sql = build_select_query(table, top=10, cols=["id", "name"])
        results = execute_raw_select(sql)
        ```

    """
    engine = create_engine(database=database)

    validate_engine(engine)
    validate_sql(sql)

    session_initializer = sessionmaker(bind=engine)
    with session_initializer() as session:
        results = session.execute(text(sql)).fetchall()
    return list(results)


def execute_pandas_select(
    sql: str,
    database: str = None,
) -> pd.DataFrame:
    """Create an engine and execute a SQL select operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.
        database (str, optional): Database to connect to. Defaults to None. Can be set as an environment variable.

    Returns:
        data_frame: Result of the query.

    Examples:
        To use this function with a custom sql query:
        ```python
        sql = "SELECT * FROM table"
        results = execute_pandas_select(sql)
        ```

        To use this function with a query built using `build_select_query()`:
        ```python
        table = "table"
        sql = build_select_query(table, top=10, cols=["id", "name"])
        results = execute_pandas_select(sql)
        ```
    """
    engine = create_engine(database=database)

    validate_engine(engine)
    validate_sql(sql)

    data_frame = pd.read_sql(sql, engine)
    return data_frame


def execute_raw_insert(
    sql: str, insert_type: InsertType = InsertType.BULK_INSERT, database: str = None
) -> None:
    """Create an engine and execute a SQL insert operation using SQLAlchemy.

    Arguments:
        sql (str): SQL query to execute.
        insert_type (InsertType, optional): Type of insert operation to execute. Defaults to InsertType.BULK_INSERT.
        database (str, optional): Database to connect to. Defaults to None. Can be set as an environment variable.

    Raises:
        ValueError: If insert_type is not of type InsertType.

    Returns:
        None

    Examples:
        To use this function with a custom sql query:
        ```python
        sql = "INSERT INTO table VALUES (1, 'name')"
        execute_raw_insert(sql)
        ```

        To use this function with a query built using `build_insert_query()`:
        ```python
        table = "table"
        columns = ["id", "name"]
        data_rows = [(1, "name")]
        sql = build_insert_query(table, columns, data_rows)
        execute_raw_insert(sql)
        ```
    """
    if not isinstance(insert_type, InsertType):
        raise ValueError("Insert type parameter given is not of type InsertType")

    validate_sql(sql)

    engine = create_engine(database, insert_type)
    validate_engine(engine)

    session_initializer = sessionmaker(bind=engine)
    with session_initializer() as session:
        session.execute(text(sql))
        session.commit()


def execute_pandas_insert(
    table: str, data_frame: pd.DataFrame, database: str = None
) -> None:
    """Create an engine and execute a SQL insert operation using SQLAlchemy.

    Arguments:
        table (str): Table to insert into.
        data_frame (pd.DataFrame): DataFrame to insert into the database.
        database (str, optional): Database to connect to. Defaults to None. Can be set as an environment variable.

    Raises:
        ValueError: If table is None.
        ValueError: If data_frame is not of type pd.DataFrame.
        ValueError: If the DataFrame has more rows than the maximum insert limit.
        ValueError: If the DataFrame is empty.

    Returns:
        None

    Examples:
        To use this function, call `execute_pandas_insert()`:
        ```python
        table = "dbo.MyTable"
        data_frame = pd.DataFrame(
            {
                "Col1": [1, 2],
                "Col2": ["Value1", "Value2"],
            }
        )
        execute_pandas_insert(table, data_frame)
        ```
    """
    if not table or table.isspace():
        raise ValueError("Table name is None")

    if not isinstance(data_frame, pd.DataFrame):
        raise ValueError("Dataframe is not of type pd.DataFrame")

    if len(data_frame) > MAX_INSERT_LIMIT:
        raise ValueError("Dataframe size exceeds the maximum insert limit")

    if data_frame.empty:
        raise ValueError("Dataframe is empty")

    engine = create_engine(database)
    validate_engine(engine)

    data_frame.to_sql(table, engine, if_exists="append", index=False)
