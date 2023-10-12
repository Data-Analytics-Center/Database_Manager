# SQLAlchemy Core

SQLAlchemy core is the way we can perform basic CRUD operations on the database.

Core provides:

- a Pythonic SQL language that allows you to construct SQL queries using Python objects and functions that closely resemble SQL syntax.
- Database agnostic, works with different DB systems
- Build complex queries (with conditions, joins, etc.)

[Dwiki Reference](https://github.com/Data-Analytics-Center/Dwiki/blob/main/guides/sqlalchemy/building_queries.md)
[SQLAlchemyCore CRUD API Reference](https://docs.sqlalchemy.org/en/20/core/dml.html)

## Getting Started

To build SQL Queries using SQLAlchemy Core, you first need to define the structure of your tables.

```python
from sqlalchemy import Table, Integer, String, Column, MetaData

meta_data = MetaData(schema="dbo")

table_1 = Table(
    "user_table",
    meta_data,
    Column("index", Integer)
    Column("name", String)
    Column("grade", String)
)

table_2 = Table(
    "info_table",
    meta_data,
    Column("email", String),
    Column("address", String)
)
```

Some examples on how to build SQL queries using this: 
#### Basic Select Query

```python
from sqlalchemy import select

query = select(table)
print(query)
```
```
Output
SELECT dbo.user_table.index, dbo.user_table.name, dbo.user_table.grade
FROM dbo.user_table
```

#### Select Query with desired columns specified
```python
from sqlalchemy import select

query = select(table.c.name, table.c.grade)
print(query)
```
or
```python
query = select(table.c["name","grade"])
print(query)
```
```
Output
SELECT dbo.user_table.name, dbo.user_table.grade 
FROM dbo.user_table
```

#### Select columns from multiple tables
```python
select_query = select(table.c.name, table.c.grade, table_2)
print(select_query)
```
```
Output
SELECT dbo.user_table.name, dbo.user_table.grade, dbo.info_table.email, dbo.info_table.address 
FROM dbo.user_table, dbo.info_table
```

#### Select query with a 'WHERE' clause
```python
select_query = select(table_1).where(table_1.c.name == "John")
print(select_query)
```
```
Output
SELECT dbo.user_table.index, dbo.user_table.name, dbo.user_table.grade 
FROM dbo.user_table 
WHERE dbo.user_table.name = :name_1
```

#### Basic Insert Query
```python
from sqlalchemy import insert

insert_query = insert(table_1).values(index=10, name="Adam", grade="A")
print(insert_query)
```
```
Output
INSERT INTO dbo.user_table (index, name, grade) VALUES (:index, :name, :grade)
```

#### Bulk Insert

A bulk insert is a single query that inserts multiple rows into a table. This is more efficient than inserting each row individually.

```python
data_to_insert = [
    {"index": 1, "name": "John", "grade": "A"},
    {"index": 2, "name": "Jane", "grade": "B"},
    {"index": 3, "name": "Adam", "grade": "A"},
]
    
insert_query = insert(table_1).values(data_to_insert)
print(insert_query)
```
```
Output
INSERT INTO dbo.user_table (index, name, grade) VALUES (:index_m0, :name_m0, :grade_m0), (:index_m1, :name_m1, :grade_m1), (:index_m2, :name_m2, :grade_m2)
```