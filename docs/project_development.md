## Overview

Database-Manager is an abstraction on top of python database packages meant to accomplish the following goals:

- create a simple API to do common DB tasks such as selecting data and inserting data
- serve as an adapter between our applications & third party libraries to facilitate any future underlying library changes (motivated by us switching from pyodbc to sqlalchemy)
- abstract away the troublesome logic of writing out the workaround code to execute raw custom SQL instead of using built in ORM features
- create a unified database library to use across all DAC applications

## Getting Started 

To install this package to a DAC project simply run the following command:

`pipenv install https://github.com/Data-Analytics-Center/Database_Manager.git`

To update the package run the following:

`pipenv update database-manager`

## Usage

View the API in depth by running the following commands:

- `pipenv install`
- `pipenv shell` or activate your enviroment
- `mkdocs serve`
- go to `localhost:8000`

## Development

To get started with development clone this repository.
Then run `pipenv install` to generate the required packages in the `.venv` directory
The package code is in `/src/database-manager`
To learn more about the code run the following:
- `pipenv shell` or activate your enviroment
- `mkdocs serve`
- go to `localhost:8000`

## Verifying Package Build

To verify the package builds correctly prior to shipping a new version we can run the following commands:

- `python3 setup.py bdist_wheel sdist`
- `pipenv install .`
- `python3 test_install.py`

If `Hello World` prints to the terminal then the package built and installed successfully.

Make sure to uninstall the package after by doing `pipenv uninstall database-manager`