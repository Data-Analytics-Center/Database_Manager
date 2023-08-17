"""Connection Manager tests."""

import os

import pytest
from dotenv import load_dotenv

from ..connection_manager import create_engine


load_dotenv()

DRIVER = os.getenv("DRIVER")
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")


def test_valid_engine_test():
    """Test a valid engine is created."""
    engine = create_engine(SERVER, DATABASE, DRIVER, bulk_insert=False)
    assert engine is not None


def test_missing_engine_parameters():
    """Test invalid engine parameters raise an exception."""
    with pytest.raises(ValueError, match="Server parameter cannot be None or empty."):
        create_engine(None, DATABASE, DRIVER, bulk_insert=False)

    with pytest.raises(ValueError, match="Database parameter cannot be None or empty."):
        create_engine(SERVER, None, DRIVER, bulk_insert=False)

    with pytest.raises(ValueError, match="Driver parameter cannot be None or empty."):
        create_engine(SERVER, DATABASE, None, bulk_insert=False)


def test_invalid_engine_parameters():
    """Test invalid engine parameters raise an exception."""
    pytest.raises(
        ValueError,
        create_engine,
        "",
        DATABASE,
        DRIVER,
        bulk_insert=False,
        match="Server parameter cannot be None or empty.",
    )
    # pytest.raises(ValueError, create_engine, SERVER, "", DRIVER, match="Database parameter cannot be None or empty.")
    # pytest.raises(ValueError, create_engine, SERVER, DATABASE, "", match="Driver parameter cannot be None or empty.")
