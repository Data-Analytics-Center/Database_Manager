"""Query Builders module contains functions to build SQL queries."""
import os

from dotenv import load_dotenv


def build_select_query(
    table: str,
    database: str = None,
    schema: str = "dbo",
    top: int = None,
    columns: list = ["*"],
    where: str = None,
    group_by: str = None,
    order_by: str = None,
) -> str:
    """Build a select query.

    Arguments:
        table (str): Table to select from.
        database (str, optional): Database to connect to. Defaults to None. Can be set as an environment variable.
        schema (str, optional): Schema to connect to. Defaults to "dbo".
        top (int, optional): Number of rows to select. Defaults selecting all rows.
        columns (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.

    Raises:
        ValueError: If table name is not provided.
        ValueError: If database name is not provided and is not set as an environment variable.

    Returns:
        sql_query (str): A select query.

    Example:
        To use this function, call `build_select_query()`:
        ```python
        sql_query = build_select_query(
            table="dbo.MyTable",
            top=100,
            cols=["Col1", "Col2"],
            where="Col1 = 1",
        )
        ```
    """
    load_dotenv()

    if not table or table.isspace():
        raise ValueError("Table name is required.")

    if database is None or database == "" or database.isspace():
        if not os.getenv("DATABASE"):
            raise ValueError(
                "Database name is required to build a query. Pass as an argument or set as an environment variable."
            )
        database = os.getenv("DATABASE")

    sql_query = f"""SELECT {f"TOP {top} " if top else ""}{", ".join(columns)} FROM [{database}].[{schema}].[{table}]"""

    if where is not None:
        sql_query += f" WHERE {where}"

    if group_by is not None:
        sql_query += f" GROUP BY {group_by}"

    if order_by is not None:
        sql_query += f" ORDER BY {order_by}"

    return sql_query


def build_insert_query(
    table: str,
    columns: list,
    data_rows: list[tuple],
    database: str = None,
    schema: str = "dbo",
) -> str:
    """Build an insert query.

    Arguments:
        table (str): Table to insert into.
        columns (list): List of columns to insert into.
        data_rows (list[tuple]): List of values to insert where each tuple represents a row.
        database (str, optional): Database to connect to. Defaults to None. Can be set as an environment variable.
        schema (str, optional): Schema to connect to. Defaults to "dbo".

    Raises:
        ValueError: If table name is not provided.
        ValueError: If columns list is not provided.
        ValueError: If number of values exceeds the maximum insert limit.
        ValueError: If number of columns does not match the number of args provided.
        ValueError: If database name is not provided and is not set as an environment variable.

    Returns:
        sql_query (str): An insert query.

    Example:
        To use this function, call `build_insert_query()`:
        ```python
        sql_query = build_insert_query(
            table="dbo.MyTable",
            cols=["Col1", "Col2"],
            values=[(1, "Value1"), (2, "Value2")],
            schema="dbo",
        )
        ```
    """
    if not table or table.isspace():
        raise ValueError("Table name is required.")

    if not columns:
        raise ValueError("At least one column is required!")

    if database is None or database == "" or database.isspace():
        if not os.getenv("DATABASE"):
            raise ValueError(
                "Database name is required to build a query. Pass as an argument or set as an environment variable."
            )
        database = os.getenv("DATABASE")

    modified_data_rows = []
    for row in data_rows:
        if len(columns) != len(row):
            raise ValueError(
                "Number of columns does not match the number of args provided!"
            )
        new_row = []
        for i in range(len(row)):
            if isinstance(row[i], str):
                new_row.append(f"{row[i]}")
            else:
                new_row.append(row[i])
        modified_data_rows.append(str(new_row).replace("[", "(").replace("]", ")"))

    sql_query = f"""INSERT INTO [{database}].[{schema}].[{table}] ({", ".join(columns)}) VALUES {', '.join(modified_data_rows)};"""  # noqa: E501

    return sql_query
