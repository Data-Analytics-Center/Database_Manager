## Overview

Database-Manager is an abstraction on top of python database packages meant to accomplish the following goals:

- create a simple API to do common DB tasks such as selecting data and inserting data
- serve as an adapter between our applications & third party libraries to facilitate any future underlying library changes (motivated by us switching from pyodbc to sqlalchemy)
- abstract away the troublesome logic of writing out the workaround code to execute raw custom SQL instead of using built in ORM features
- create a unified database library to use across all DAC applications

## Getting Started 

### How to install this package?

#### Make sure you have a github access token. If not, follow these steps -

1. Generate a Personal Access Token:
- Go to your GitHub account settings.
- Click on "Developer settings" > "Personal access tokens" > "Generate token."
- Give it a name, select the appropriate scopes (e.g., repo for full access to private repositories), and generate the token.

2. Save the token somewhere secure and do not share it with anyone. You will not be able to view the token again so make sure you copy and save it.

#### Use the following link to install the package into your pipenv environment - 

`pipenv install git+https://<ACCESS_TOKEN>@github.com/Data-Analytics-Center/Database_Manager.git#egg=Database_Manager`

Replace ``<ACCESS_TOKEN>`` with your access token.

#### Use the following link to install the package into your venv environment (assuming you have the environment created and activated)-

`pip install git+https://<ACCESS_TOKEN>@github.com/Data-Analytics-Center/Database_Manager.git#egg=Database_Manager`

Replace ``<ACCESS_TOKEN>`` with your access token.
#### To update the package run the following:

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

## Testing

Run tests using VSCode built-in testing or run PyTest in your terminal.

# TODO: talk about the testing database/tables