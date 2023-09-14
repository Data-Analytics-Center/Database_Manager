"""tests."""

from src.database_manager.query_builders import build_select_query


def main():
    sql = build_select_query(
        table="test",
        database="sandbox",
        schema="dbo",
        top=100,
        columns=["Col1", "Col2"],
        where="Col1 = 1",
    )
    print(sql)


if __name__ == "__main__":
    main()
