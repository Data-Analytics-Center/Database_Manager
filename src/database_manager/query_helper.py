import pandas as pd

from .connection_manager import engine_factory


def insertSQLPandas(
    df,
    table,
    rdbms=None,
    server=None,
    database=None,
    if_exists="append",
    index=False,
):
    with engine_factory(rdbms=rdbms, server=server, database=database).begin() as connection:
        df.to_sql(table, connection, if_exists=if_exists, index=index)


def selectSQLPandas(sql, rdbms=None, server=None, database=None):
    with engine_factory(rdbms=rdbms, server=server, database=database).begin() as connection:
        results = pd.read_sql(sql, connection)
    return results
