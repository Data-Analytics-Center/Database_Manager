"""Contains functions used to build queries."""


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
        top (int, optional): Number of rows to select. Defaults to None, selecting all rows.
        cols (list, optional): List of columns to select. Defaults to ["*"].
        where (str, optional): Where clause. Defaults to None.
        group_by (str, optional): Group by clause. Defaults to None.
        order_by (str, optional): Order by clause. Defaults to None.

    Raises:
        Exception: If table name is not provided.

    Returns:
        A select query.
    """

    if table is None:
        raise ValueError("Table name is required.")

    sql_query = (
        f"""SELECT {f"TOP {top}" if top else ""} {", ".join(cols)} FROM {table}"""
    )

    if where is not None:
        query += f" WHERE {where}"

    if group_by is not None:
        query += f" GROUP BY {group_by}"

    if order_by is not None:
        query += f" ORDER BY {order_by}"

    return sql_query
