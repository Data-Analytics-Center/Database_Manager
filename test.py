"""Test the select function."""

from sqlalchemy import CursorResult
from src.database_manager.connection_manager import InsertType
from src.database_manager.execute_query import execute_raw_select, execute_pandas_select, execute_raw_insert, execute_pandas_insert
from src.database_manager.query_builders import build_select_query, build_insert_query
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

server = os.getenv("SERVER")
database = os.getenv("DATABASE")
driver = os.getenv("DRIVER")
table_name = os.getenv("TABLE")


def test_raw_select():
    sql = build_select_query(table_name, 10, ["filename", "id"])
    result: CursorResult = execute_raw_select(sql)
    rows = result

    for row in rows:
        print(row)

def test_pandas_select():
    sql = build_select_query(table_name,cols=["filename", "id"])
    result = execute_pandas_select(sql)
    print(result)

def test_raw_insert():
    sql = build_insert_query(table_name, ["filename", "id"], [("final_final_test", 5000), ("hehe", 2000), ("hehe", 2000), ("hehe", 2000), ("hehe", 2000), ("hehe", 2000), ("hehe", 2000)])
    execute_raw_insert(sql, InsertType.SINGLE_INSERT)
    # execute_raw_insert(sql)zz

def test_pandas_insert():
    df = pd.DataFrame([["test_5", 5], ["test_6", 6],["test_7", 7],["test_8", 8] ], columns=["filename", "id"])
    execute_pandas_insert(table_name, df)

def insert_query():
    sql = build_insert_query(table_name, ["filename", "id"], [("final_final_test", 5000), ("hehe", 2000)])
    print(sql)


# test_raw_select()
# test_pandas_select()
# test_raw_insert()
# test_pandas_insert()
# insert_query()
