"""test.py."""

from src.database_manager.connection_manager import ReturnLastID
from src.database_manager.query_builders import build_insert_query
from src.database_manager.query_execution import (
    execute_pandas_insert,
    execute_raw_insert,
)


def main():
    """Main function."""  # noqa: D401
    table = "test"
    schema = "jgj891"
    cols = ["id", "val"]
    values = [[1, "John"], [2, "Jane"]]
    sql = build_insert_query(table, cols, values, schema=schema)
    # print(sql)
    last_id = execute_raw_insert(sql)
    print(last_id)

    # data_frame = pd.DataFrame(values, columns=cols)
    # execute_pandas_insert(data_frame, table)


if __name__ == "__main__":
    main()
