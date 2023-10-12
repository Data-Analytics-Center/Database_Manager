# Examples & Best Practices

Some database terms to be familiar with:

- **Connection:** a connection to the database
- **Engine:** an object that manages connections to the database
- **Transaction:** a series of database operations that are treated as a single unit of work
- **Query:** a request for data from the database
- **Statement:** a string of SQL code that is sent to the database to be executed

## Environment Variables

!!! info "Enviroment Variables"
    **Always Required**
    
    ***ENV_TYPE:*** used to determine the environment, can be either `DEV` or `PROD` 

    ***SERVER:*** the server to connect to

    ***DRIVER:*** the driver used to connect to the database

    --------------------------------------------

    **Optional**

    ***DATABASE:*** the database to connect to (can be set as environment variable or passed in as a parameter)

    --------------------------------------------

    **Production Only**

    ***UID:*** the username of the user to connect as

    ***PID:*** the password of the user to connect as

## Creating an Engine

The most basic function of the Engine is to provide access to a Connection, which can then invoke SQL statements.

The engine has 2 main parts, the connection pool and the DBAPI connection.

The connection pool is a pool of DBAPI connections that are ready to be used, these only become active on demand.

The DBAPI (Database API) is a set of standards in Python for accessing and manipulating databases, so for Microsoft SQL Server it is the API for interacting with the database.

[SQLAlchemy Engine & Connections Reference](https://docs.sqlalchemy.org/en/20/core/connections.html)

!!! tip "Best Practice"
    Typical usage for engines to create one per lifetime of a single application.



```python
from Database_Manager import engine_factory

engine = engine_factory()
```

The above example will create an engine by pulling the database from the environment.

If you want to specify the database you can do so by passing it in as a parameter.

```python
from Database_Manager import engine_factory

database_name = "my_database"
engine = engine_factory(database=database_name)
```

## Executing & Managing Transactions

A transaction is a series of database operations that are treated as a single unit of work.

You can execute multiple queries in one transaction.

When executing queries with an engine use the engine.begin() method to start a transaction.

If any of the queries fail, the entire transaction will fail and the database will be rolled back to its previous state.

[SQLAlchemy Reference](https://docs.sqlalchemy.org/en/20/core/connections.html#using-transactions:~:text=for%20a%20tutorial.-,Using%20Transactions%C2%B6,-Note)

```python
from Database_Manager import engine_factory

engine = engine_factory()

with engine.begin() as connection:
    connection.execute("INSERT INTO my_table VALUES (1, 'test')")
    connection.execute("INSERT INTO my_table VALUES (2, 'test')")
```

For the above code example if there is *ANY* exception then the entire transaction will be rolled back automatically since we used the `with` statement aka the engine context manager.

## Security

The below shows how to use parameterized queries to prevent SQL injection attacks but view the
[SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html#sql-injection-prevention-cheat-sheet) for more SQL Injection Prevention best practices.

### Parameterized Queries

!!! Warning "SQL Injection Prevention"
    When you need to execute a query that has parameters you should *ALWAYS* use parameterized queries.
    
    This will prevent SQL injection attacks so if you do not do this any pull requests will be rejected.

```python
from Database_Manager import engine_factory
from datetime import datetime

engine = engine_factory()

current_time = datetime.now()

with engine.begin() as connection:
        dataframe = pd.read_sql(
            "select * from [Tables_Meta] where [dtg]=?;",
            connection,
            params=(current_time,),
        )
```

## Executing Pandas Operations

### Pandas Select

Generally it will be better for queries to be executed using Pandas operations instead of raw SQL queries.

```python
from Database_Manager import engine_factory

engine = engine_factory()

with engine.begin() as connection:
    dataframe = pd.read_sql("SELECT * FROM my_table", connection)
```

### Pandas Insert

```python
from Database_Manager import engine_factory

engine = engine_factory()

dataframe = pd.DataFrame({"id": [1, 2], "name": ["test1", "test2"]})

with engine.begin() as connection:
    dataframe.to_sql("my_table", connection, if_exists="append", index=False, pa)
```

## Executing Raw Queries

!!! Warning "SQL Injection Prevention"
    Database, schema, and table cannot be parameterized so you must use string formatting to insert them into the query.
    
    Never trust user input so you should validate the database, schema, and table before using them in the query.

```python
from Database_Manager import engine_factory
from config import Config

engine = engine_factory()
config = Config()

database = config.DATABASE
schema = config.SCHEMA
table = "MyTable"

with engine.begin() as connection:
    result = connection.execute("SELECT * FROM [{database}].[{schema}].[{table}]")
```



