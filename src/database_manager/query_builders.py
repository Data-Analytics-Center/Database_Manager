"""Query Builders module contains functions to build SQL queries."""

MAX_INSERT_LIMIT = 80000


def build_select_query(
    table: str,
    top: int = None,
    cols: list = ["*"],
    where: str = None,
    group_by: str = None,
    order_by: str = None,
) -> str:
    """Build a select query.

    Arguments:
        table (str): Table to select from.
        top (int, optional): Number of rows to select. Defaults selecting all rows.
        cols (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.

    Raises:
        Exception: If table name is not provided.

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
        ```
    """
    if table is None or table == "" or table == " ":
        raise ValueError("Table name is required.")

    sql_query = (
        f"""SELECT {f"TOP {top} " if top else ""}{", ".join(cols)} FROM {table}"""
    )

    if where is not None:
        sql_query += f" WHERE {where}"

    if group_by is not None:
        sql_query += f" GROUP BY {group_by}"

    if order_by is not None:
        sql_query += f" ORDER BY {order_by}"

    return sql_query


def build_insert_query(table: str, columns: list, data_rows: list[tuple]) -> str:
    """Build an insert query.

    Arguments:
        table (str): Table to insert into.
        columns (list): List of columns to insert into.
        data_rows (list[tuple]): List of values to insert where each tuple represents a row.

    Raises:
        Exception: If table name is not provided.
        Exception: If columns list is not provided.
        Exception: If number of values exceeds the maximum insert limit.
        Exception: If number of columns does not match the number of args provided.

    Returns:
        sql_query (str): An insert query.

    Example:
        To use this function, call `build_insert_query()`:
        ```python
        sql_query = build_insert_query(
            table="dbo.MyTable",
            cols=["Col1", "Col2"],
            values=[(1, "Value1"), (2, "Value2")],
        )
        ```
    """
    if not table:
        raise ValueError("Table name is required.")

    if not columns:
        raise ValueError("At least one column is required!")

    if len(data_rows) > MAX_INSERT_LIMIT:
        raise ValueError(
            f"Number of values exceeds the maximum limit of {MAX_INSERT_LIMIT}"
        )

    modified_data_rows = []
    for row in data_rows:
        if len(columns) != len(row):
            raise ValueError(
                "Number of columns does not match the number of args provided!"
            )
        new_row = []
        for i in range(len(row)):
            if isinstance(row[i], str):
                new_row.append(f'{row[i]}')
            else:
                new_row.append(row[i])
        modified_data_rows.append(
            str(new_row).replace("[", "(").replace("]", ")"))

    sql_query = f"""INSERT INTO {table} ({", ".join(columns)}) VALUES {', '.join(modified_data_rows)};"""

    return sql_query
