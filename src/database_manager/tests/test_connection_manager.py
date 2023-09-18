"""Connection Manager tests."""

import os

import pytest
from sqlalchemy import Engine

from ..connection_manager import create_engine
from .test_utils import delete_env_variables


def test_valid_engine_with_env_database():
    """Test a valid engine is created with pulling the database from an environment variable."""
    engine = create_engine()
    assert engine is not None
    assert isinstance(engine, Engine)


def test_valid_engine_with_param_database():
    """Test a valid engine is created with passing database as param."""
    delete_env_variables()
    os.environ["DATABASE"] = ""
    engine = create_engine(database="test")
    assert engine is not None
    assert isinstance(engine, Engine)


def test_engine_missing_server():
    """Test creating engine with missing server environment variable."""
    delete_env_variables()
    os.environ["SERVER"] = ""
    with pytest.raises(
        ValueError, match=r"Server environment variable is not properly set."
    ):
        create_engine()


def test_engine_missing_database():
    """Test creating engine with missing database environment variable."""
    delete_env_variables()
    os.environ["DATABASE"] = ""
    with pytest.raises(
        ValueError,
        match=r"Database is not set please specify a database as an execute function parameter or environment variable.",
    ):
        create_engine()


def test_engine_missing_driver():
    """Test creating engine with missing driver environment variable."""
    delete_env_variables()
    os.environ["DRIVER"] = ""
    with pytest.raises(
        ValueError, match=r"Driver environment variable is not properly set."
    ):
        create_engine()
