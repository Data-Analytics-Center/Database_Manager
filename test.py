"""small test file."""

from src.database_manager.query_builders import build_select_query

MAX_INSERT_LIMIT = 80000


def main():
    """Main function."""  # noqa: D401
    sql_query = build_select_query(table="Test_Table", cols=["Id"])
    sql_query_2 = build_select_query(
        table="dbo.MyTable", cols=["Col1", "Col2"])
    sql_query_3 = build_select_query(table="dbo.MyTable", top=10)
    print(sql_query)
    print(sql_query_2)
    print(sql_query_3)


if __name__ == "__main__":
    main()
