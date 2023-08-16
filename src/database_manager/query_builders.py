from .connection_manager import create_connection
from sqlalchemy import engine, text


def batch_insert(engine, database, table, columns, args, values_list):
    """
    Insert multiple rows into a specified table in batches.

    Args:
    engine: Database engine or connection object.
    database (str): The name of the database to connect to.
    table (str): The name of the table where the insertion will be performed.
    columns (list): List of column names in the table.
    args (list): List of argument names corresponding to columns in the table.
    values_list (list of tuples): List of tuples, each containing values to be inserted into corresponding columns.

    Raises:
    ValueError: If the database name, table name, columns list, args list, or values_list is not provided,
                or if the number of args does not match the number of columns in the table.
    """
    if not database:
        raise ValueError("The database name is not provided!")
    if not table:
        raise ValueError("The table name is not provided!")
    if not columns:
        raise ValueError("At least one column name is required!")
    if not args:
        raise ValueError("At least one argument name is required!")
    if len(args) != len(columns):
        raise ValueError(
            "Number of args should match the number of columns in the table!"
        )

    columns_string = ", ".join(columns)
    placeholders = ", ".join(
        ["(" + ", ".join(["%s"] * len(args)) + ")"] * len(values_list)
    )
    query = f"INSERT INTO {table} ({columns_string}) VALUES {placeholders}"

    conn = create_connection(database)
    if not conn:
        raise Exception(f"The connection was not formed with this database: {database}")

    try:
        with conn.cursor() as cursor:
            cursor.executemany(query, values_list)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

    columns_string = ", ".join(columns)
    placeholders = ", ".join(
        ["(" + ", ".join(["%s"] * len(args)) + ")"] * len(values_list)
    )
    query = f"INSERT INTO {table} ({columns_string}) VALUES {placeholders}"

    conn = create_connection(database)
    if not conn:
        raise Exception(f"The connection was not formed with this database: {database}")

    try:
        with conn.cursor() as cursor:
            cursor.executemany(query, values_list)
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
