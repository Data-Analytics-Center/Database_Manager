from src.database_manager.query_builders import build_insert_query

sql = build_insert_query(
    table="dbo.MyTable",
    columns=["ID", "Name"],
    data_rows=[(None, "Sarthak"), (2, "John")],
)

print(sql)