"""test.py."""

import pandas as pd

# from src.database_manager.query_builders import build_insert_query
from src.database_manager.query_execution import execute_pandas_insert


def main():
    """Main function."""  # noqa: D401
    table = "test"
    dataframe = pd.DataFrame({"id": [5, 6, 7], "val": ["Adam", "Bob", "Charlie"]})
    execute_pandas_insert(table, dataframe, schema="jgj891")


if __name__ == "__main__":
    main()
