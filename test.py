"""small test file."""

from src.database_manager.query_builders import build_insert_query


def main():
    """main function."""
    sql_query = build_insert_query(
        table="some_table",
        columns=["col1", "col2"],
        data_rows=[(1, 2), (3, 4)],
    )
    print(sql_query)


if __name__ == "__main__":
    main()
