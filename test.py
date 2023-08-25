"""Test the select function."""

from sqlalchemy import CursorResult
from src.database_manager.connection_manager import create_engine
from src.database_manager.execute_query import execute_raw_select, execute_pandas_select
from src.database_manager.query_builders import build_select_query, build_insert_query
from dotenv import load_dotenv
import os

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")
driver = os.getenv("DRIVER")
table = os.getenv("TABLE")


def test_sql_query():
    """Test that a valid engine is created."""
    engine = create_engine(server, database, driver, False)
    sql = build_select_query(table, 10, ["filepath", "id"])
    result: CursorResult = execute_raw_select(engine, sql)
    rows = result

    for row in rows:
        print(row)


def pandas_Print():
    engine = create_engine(server, database, driver, False)
    sql = build_select_query(table, 10, ["filepath", "id"])
    result = execute_pandas_select(engine, sql)
    print(result)


def insert_query():
    sql = build_insert_query(table, ["filename", "id"], "test", 1)
    print(sql)


insert_query()


# test_sql_query()
# pandas_Print()
