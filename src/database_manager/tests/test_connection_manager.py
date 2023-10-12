"""Connection Manager tests."""

import os

import pytest
from sqlalchemy import Engine

from ..connection_manager import engine_factory
from .test_utils import delete_env_variables


def test_valid_engine_with_env_database():
    """Test a valid engine is created with pulling the database from an environment variable."""
    engine = engine_factory()
    assert engine is not None
    assert isinstance(engine, Engine)


def test_valid_engine_with_param_database():
    """Test a valid engine is created with passing database as param."""
    delete_env_variables()

    os.environ["DATABASE"] = ""

    engine = engine_factory(database="test")
    assert engine is not None
    assert isinstance(engine, Engine)


def test_engine_missing_server():
    """Test creating engine with missing server environment variable."""
    delete_env_variables()

    os.environ["SERVER"] = ""

    with pytest.raises(
        ValueError, match=r"SERVER environment variable is not properly set."
    ):
        engine_factory()


def test_engine_missing_database():
    """Test creating engine with missing database environment variable."""
    delete_env_variables()

    os.environ["DATABASE"] = ""

    with pytest.raises(
        ValueError,
        match=r"DATABASE is not set please specify a database as an execute function parameter or environment variable.",
    ):
        engine_factory()


def test_engine_missing_driver():
    """Test creating engine with missing driver environment variable."""
    delete_env_variables()

    os.environ["DRIVER"] = ""

    with pytest.raises(
        ValueError, match=r"DRIVER environment variable is not properly set."
    ):
        engine_factory()


def test_engine_missing_env_type():
    """Test creating engine with missing env_type environment variable."""
    delete_env_variables()

    os.environ["ENV_TYPE"] = ""

    with pytest.raises(
        ValueError, match=r"ENV_TYPE environment variable is not properly set."
    ):
        engine_factory()


def test_engine_missing_uid():
    """Test creating engine with missing uid environment variable."""
    delete_env_variables()

    os.environ["ENV_TYPE"] = "PROD"
    os.environ["UID"] = ""

    with pytest.raises(
        ValueError, match=r"UID environment variable is not properly set."
    ):
        engine_factory()


def test_engine_missing_pid():
    """Test creating engine with missing pid environment variable."""
    delete_env_variables()

    os.environ["ENV_TYPE"] = "PROD"
    os.environ["UID"] = "test"
    os.environ["PID"] = ""

    with pytest.raises(
        ValueError, match=r"PID environment variable is not properly set."
    ):
        engine_factory()
