"""
Database utilities
Simple SQLite database helpers for the practice exercise
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional


def get_db_path() -> str:
    """
    Get the database file path from environment variable

    Returns:
        str: Path to SQLite database file
    """
    return os.getenv('DATABASE_URL', 'practice_exercise.db')


@contextmanager
def get_db_connection():
    """
    Context manager for database connections
    Ensures connections are properly closed

    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks")

    Yields:
        sqlite3.Connection: Database connection
    """
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """
    Initialize the database schema
    Creates the tasks table if it doesn't exist

    TODO: Implement this function
    Hint: Create a table with columns: id, title, description, status, created_at, updated_at
    Hint: Use TEXT, INTEGER, and TIMESTAMP types
    """
    pass


# TODO: Optional helper functions you might want to add:
# - execute_query(query: str, params: tuple) -> list
# - execute_one(query: str, params: tuple) -> Optional[dict]
# - execute_update(query: str, params: tuple) -> int (returns rows affected)
