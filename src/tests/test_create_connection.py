"""
This module contains the unit tests for the database_manager module.

In this case, the create_engine() function is an external dependency, so you can use unittest.mock to replace it with a mock object during testing.

- Kevin Henderson 2023 8/15/2023
TODO: Figure out how to mock the return value of create_connection() to return a fake Connection object
- Connection Object Docs
https://docs.sqlalchemy.org/en/20/core/engines.html

- Mocking SQLAlchemy
https://pypi.org/project/mock-alchemy/

"""
from unittest.mock import MagicMock, patch, mock
from ..database_manager import create_connection
@mock.patch('database_manager.connection_manager.create_connection', return_value='test_connection')
def test_create_connection(self, mock_create_connection):
    # Define fake environment variables
    fake_env = {
        'ENV_TYPE': 'TEST',
        'DATABASE': 'test_db',
        'TEST_DRIVER': 'test_driver',
        'TEST_SERVER': 'test_server'
    }
    
    # Define the expected connection string
    expected_connection_string = "mssql://@test_server/test_db?driver=test_driver&Encrypt=no"
    
    # Create the MagicMock object for the engine and set up the begin method to return the fake connection as a context manager
    mock_engine = MagicMock(spec=Connection)
    mock_engine.begin.return_value.__enter__.return_value = 'test_connection'

