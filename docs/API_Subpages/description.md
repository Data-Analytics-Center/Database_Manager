# The Database Manager Package

## Overview

### Goals

Database-Manager is an abstraction on top of python database packages meant to accomplish the following goals:

- normalize the way we interact with databases across all DAC applications and reduce duplicate code
- serve as an adapter between our applications & third party database libraries to facilitate any future underlying library changes (motivated by us switching from pyodbc to sqlalchemy)
- create a unified database library to use across all DAC applications

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


## Quick Examples

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
