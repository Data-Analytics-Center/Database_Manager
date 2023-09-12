Each function is a different way to execute a SQL query using SQLAlchemy.
For each SQL operation we offer a pandas function and a raw SQL function.

Defaultly the functions will use the database specified in the environment variable `DATABASE`. 
But you can also pass a database name as a parameter to any of the quury execution functions below.
Generally, if you want to work with multiple databases then use the database parameter to specify the database name.
otherwise, you can set the `DATABASE` environment variable and not pass the database parameter.
The following example demonstrates this with the assumption that the first code block has set the 
`DATABASE` environment variable:

Example:
        ```python
        sql = "SELECT * FROM table"
        results = execute_pandas_select(sql)
        ```

        ```python
        sql = "SELECT * FROM table"
        results = execute_pandas_select(sql, database=MY_DATABASE)
        ```

::: src.database_manager.query_execution
    options:
        members:
        - execute_raw_select
        - execute_pandas_select
        - execute_raw_insert
        - execute_pandas_insert

## Insert Type Enum

::: src.database_manager.connection_manager.InsertType