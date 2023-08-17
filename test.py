"""Test the select function."""

from src.database_manager.connection_manager import create_engine
from src.database_manager.execute_query import execute_raw_select
from src.database_manager.query_builders import build_select_query
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
    # assert engine is not None
    sql = build_select_query(table, 10, ["filepath", "id"])
    # assert sql is not None
    # print(sql)
    result = execute_raw_select(engine, sql)
    # assert result is not None
    print(result)


test_sql_query()
