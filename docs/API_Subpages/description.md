# The Database Manager Package

## Overview

The Database Manager currently is an abstraction upon simply creating an SQLAlchemy Engine which is a trivial operation

but there are so many ways to connect to a database it is best we all standardize on one way to do it.

Also, there are pros and cons to different ways but this way is extremely versatile in that it can handle any type of connection

### Goals

Database-Manager is an abstraction on top of python database packages meant to accomplish the following goals:

- normalize the way we interact with databases across all DAC applications and reduce duplicate code
- serve as an adapter between our applications & third party database libraries to facilitate any future underlying library changes (motivated by us switching from pyodbc to sqlalchemy)
- create a unified database library to use across all DAC applications

### Features

- easy engine creation
- guide on best practices for interacting with databases
- support for different types of querying like raw SQL, pandas queries, & sqlalchemy core queries