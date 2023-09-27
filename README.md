
## Overview

Database-Manager is an abstraction on top of Python database packages meant to accomplish the following goals:

- Create a simple API to do common DB tasks such as selecting data and inserting data.
- Serve as an adapter between our applications & third-party libraries to facilitate any future underlying library changes.
- Abstract away the troublesome logic of writing out the workaround code to execute raw custom SQL instead of using built-in ORM features.
- Create a unified database library to use across all DAC applications.

## Getting Started

### How to install this package?

#### Make sure you have a GitHub access token. If not, follow these steps -

1. **Generate a Personal Access Token:**
  - Go to your GitHub account settings.
  - Click on "Developer settings" > "Personal access tokens" > "Generate token."
  - Give it a name, select the appropriate scopes (e.g., repo for full access to private repositories), and generate the token.

2. **Save the token somewhere secure** and do not share it with anyone. You will not be able to view the token again, so make sure you copy and save it.

#### Use the following link to install the package into your venv environment (assuming you have the environment created and activated) -

```bash
pip install git+https://<ACCESS_TOKEN>@github.com/Data-Analytics-Center/Database_Manager.git#egg=Database_Manager
```

Replace `<ACCESS_TOKEN>` with your access token.

#### To update the package, run the following:

```bash
pip install --upgrade git+https://<ACCESS_TOKEN>@github.com/Data-Analytics-Center/Database_Manager.git#egg=Database_Manager
```

## Usage

View the API in depth by running the following commands:
- Activate your virtual environment (`source venv/bin/activate` for macOS/Linux or `.\venv\Scripts\Activate` for Windows)
- `mkdocs serve`
- Go to `localhost:8000`

## Development

To get started with development, clone this repository.
Then run `python -m venv venv` to create a virtual environment in the `.venv` directory.
Activate the virtual environment and install the required packages.
The package code is in `/src/database-manager`.
To learn more about the code, run the following:

- Activate your virtual environment
- `mkdocs serve`
- Go to `localhost:8000`

## Verifying Package Build

To verify the package builds correctly prior to shipping a new version, we can run the following commands:

- `python3 setup.py bdist_wheel sdist`
- Activate your virtual environment
- `pip install .`
- `python3 test_install.py`

If `Hello World` prints to the terminal, then the package built and installed successfully.

Make sure to uninstall the package afterward by doing `pip uninstall database-manager`.

## Testing

Run tests using VSCode built-in testing or run PyTest in your terminal.

# TODO: talk about the testing database/tables
```
