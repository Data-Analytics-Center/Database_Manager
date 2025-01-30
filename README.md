## Overview

Database_Manager is an abstraction on top of python database packages meant to accomplish the following goals:

- create a simple API to do common DB tasks such as selecting data and inserting data
- serve as an adapter between our applications & third party libraries to facilitate any future underlying library changes (motivated by us switching from pyodbc to sqlalchemy)
- abstract away the troublesome logic of writing out the workaround code to execute raw custom SQL instead of using built in ORM features
- create a unified database library to use across all DAC applications

## Getting Started

### How to install this package?

#### Make sure you have a virtual env created and activated.

```sh
python -m venv menv
.\menv\Scripts\activate
```

```sh
pip install git+https://github.com/Data-Analytics-Center/Database_Manager.git
```

#### To update the package run the following:

```sh
pip install --upgrade git+https://github.com/Data-Analytics-Center/Database_Manager.git
```

## Development

To get started with development clone this repository.
create and activate the venv

```sh
git clone git@github.com:Data-Analytics-Center/Database_Manager.git
```

```sh
python -m venv menv
.\menv\Scripts\activate
```

Then run `pip install -r requirements.txt` to generate the required packages in the `.venv` directory
The package code is in `/src/database-manager`
To learn more about the code run the following:

- `mkdocs serve`
- go to `localhost:8000`
