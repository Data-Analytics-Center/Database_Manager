"""Defines the package's API aka what functions the user may access."""

from .connection_manager import create_connection, execute_query

__all__ = ["create_connection", "execute_query"]
