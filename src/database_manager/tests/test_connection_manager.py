"""Connection Manager tests."""

import os

import pytest
from sqlalchemy import Engine

from ..connection_manager import create_engine


def test_valid_engine_test():
    """Test a valid engine is created."""
    engine = create_engine()
    assert engine is not None
    assert isinstance(engine, Engine)


def test_engine_missing_server():
    """Test creating engine with missing server environment variable."""
    os.environ["SERVER"] = ""
    with pytest.raises(
        ValueError, match=r"Server environment variable is not properly set."
    ):
        create_engine()


def test_engine_missing_database():
    """Test creating engine with missing database environment variable."""
    os.environ["DATABASE"] = ""
    with pytest.raises(
        ValueError, match=r"Database environment variable is not properly set."
    ):
        create_engine()


def test_engine_missing_driver():
    """Test creating engine with missing driver environment variable."""
    os.environ["DRIVER"] = ""
    with pytest.raises(
        ValueError, match=r"Driver environment variable is not properly set."
    ):
        create_engine()
