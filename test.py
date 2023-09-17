"""test.py."""

import pandas as pd

from src.database_manager.connection_manager import ReturnLastID

# from src.database_manager.query_builders import build_insert_query
from src.database_manager.query_execution import execute_pandas_insert


def main():
    """Main function."""  # noqa: D401
    table = "test"
    dataframe = pd.DataFrame({"id": [1, 2, 3], "val": ["Adam", "Bob", "Charlie"]})
    last_id = execute_pandas_insert(table, dataframe, return_id=ReturnLastID.FALSE)
    print(last_id)


if __name__ == "__main__":
    main()
