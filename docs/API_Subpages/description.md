# The Database Manager Package

## Overview

### Goals

Database-Manager is an abstraction on top of python database packages meant to accomplish the following goals:

- create a simple API to do common DB tasks such as selecting data and inserting data
- serve as an adapter between our applications & third party database libraries to facilitate any future underlying library changes (motivated by us switching from pyodbc to sqlalchemy)
- create a unified database library to use across all DAC applications

### Structure

The package currently contains 2 main modules:

- Query Builders: functions to build SQL queries for you based on the parameters you pass in
- Query Executors: functions to execute SQL queries for you

!!! tip "Enviroment Variables"

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


## Some Code Examples

- Getting all the rows from a given table 
```python
from Database_Manager import  build_select_query, execute_raw_select

# Specify the name of the table to get the data from.
table = "db.test_table"
sql = build_select_query(table, columns=["id", "name"])
result = execute_raw_select(sql)

# 'result' here will be a list of tuples. Each tuple is a row from the table.
for row in result:
    print(row)
```
Example Output
```
(1, 'Adam')   
(2, 'Bob')    
(3, 'Charlie')
```

- Getting all the rows from a given table as a pandas dataframe
```python
from Database_Manager import  build_select_query, execute_pandas_select

table = "db.test_table"
cols = ["id", "name"]
sql = build_select_query(table, columns=cols)
results = execute_pandas_select(sql)

# 'results' here will be a pandas dataframe.
print(results)
```
Example Output
```
     id   val
0     1  Adam
1     2  Travis
2     3  Kevin
```

- Performing a single insert into a table
```python
from Database_Manager import execute_raw_insert, build_insert_query, InsertType

table = "db.test_table"
cols = ["id", "name"]
values = [(1, "Kevin")]
sql = build_insert_query(table, columns=cols, data_rows=values)
execute_raw_insert(sql, InsertType.SINGLE_INSERT)
```

- Performing bulk insert into a table
```python
from Database_Manager import execute_raw_insert, build_insert_query, InsertType 

table = "db.test_table"
cols = ["id", "name"]
values = [(1, "Kevin"), (2, "John"), (3, "Jane"), (4, "Matt")]
sql = build_insert_query(table, columns=cols, data_rows=values)
execute_raw_insert(sql, InsertType.BULK_INSERT)
```

- Inserting a pandas data frame into a table
```python
from Database_Manager import execute_pandas_insert
import pandas as pd

table = "db.test_table"
df = pd.DataFrame({"id": [1, 2, 3], "name": ["Brandon", "Jeremy", "Grace"]})

execute_pandas_insert(table, df)
```