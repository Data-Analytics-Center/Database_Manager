"""Contains functions used to build queries."""

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
    """
    if table is None:
        raise ValueError("Table name is required.")

    sql_query = (
        f"""SELECT {f"TOP {top}" if top else ""} {", ".join(cols)} FROM {table}"""
    )

    if where is not None:
        sql_query += f" WHERE {where}"

    if group_by is not None:
        sql_query += f" GROUP BY {group_by}"

    if order_by is not None:
        sql_query += f" ORDER BY {order_by}"

    return sql_query


def build_insert_query(table: str, cols: list, values: list[tuple]) -> str:
    """Build an insert query.

    Arguments:
        table (str): Table to insert into.
        cols (list): List of columns to insert into.
        values (list[tuple]): List of values to insert.

    Raises:
        Exception: If table name is not provided.
        Exception: If columns list is not provided.
        Exception: If number of values exceeds the maximum insert limit.
        Exception: If number of columns does not match the number of args provided.

    Returns:
        sql_query (str): An insert query.
    """
    if not table:
        raise ValueError("Table name is required.")

    if not cols:
        raise ValueError("At least one column is required!")

    if len(values) > MAX_INSERT_LIMIT:
        raise ValueError(
            f"Number of values exceeds the maximum limit of {MAX_INSERT_LIMIT}"
        )

    vals = []
    for val in values:
        if len(cols) != len(val):
            raise ValueError(
                "Number of columns does not match the number of args provided!"
            )
        if isinstance(val, str):
            vals.append(f"'{val}'")
        else:
            vals.append(str(val))
    
    sql_query = f"""INSERT INTO {table} ({", ".join(cols)}) VALUES {', '.join(vals)};"""

    return sql_query