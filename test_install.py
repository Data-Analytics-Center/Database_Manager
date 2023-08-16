"""Test that the package is working as expected.

Run this file to test that the package is working as expected.
Steps:
- python3 setup.py bdist_wheel sdist
- pipenv install .
- run this file

It should print hello world, if not something is wrong.
"""

from database_manager.tests import test_build

print(test_build())