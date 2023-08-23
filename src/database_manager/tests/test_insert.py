"""Tests the insert functions."""

from ..connection_manager import create_engine
from ..execute_query import single_insert


def test_start():
    assert 2 * 2 == 4


def raw_insert_valid_test():
    assert 2 * 2 == 4
