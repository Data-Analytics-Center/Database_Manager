"""Utility functiosn for unit tests."""

import os

def delete_env_variables() -> None:
    """Delete environment variables."""
    del os.environ["SERVER"]
    del os.environ["DATABASE"]
    del os.environ["DRIVER"]
    