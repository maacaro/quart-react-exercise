"""
Database utilities
Simple SQLite database helpers for the practice exercise
"""
import sqlite3
import os
from contextlib import contextmanager
from typing import Optional
from datetime import datetime  # 👈 nuevo import para timestamps


def get_db_path() -> str:
    """
    Get the database file path from environment variable

    Returns:
        str: Path to SQLite database file
    """
    # Usamos una ruta simple de archivo SQLite.
    # Si defines DATABASE_URL en el entorno, usa eso.
    return os.getenv("DATABASE_URL", "practice_exercise.db")


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

    Columns:
        id          INTEGER PRIMARY KEY AUTOINCREMENT
        title       TEXT NOT NULL
        description TEXT NOT NULL
        status      TEXT NOT NULL (pending|in_progress|completed)
        created_at  TEXT NOT NULL (ISO datetime string)
        updated_at  TEXT NOT NULL (ISO datetime string)
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        # commit lo hace el context manager al salir sin excepciones


# TODO: Optional helper functions you might want to add:
# - execute_query(query: str, params: tuple) -> list
# - execute_one(query: str, params: tuple) -> Optional[dict]
# - execute_update(query: str, params: tuple) -> int (returns rows affected)


def seed_sample_data() -> None:
    """
    Optional: seed the database with sample data.

    Por ahora insertamos algunas tareas de ejemplo en la tabla `tasks`.
    Si llamas varias veces a esta función, se duplicarán los registros.
    """
    now = datetime.utcnow().isoformat()

    sample_tasks = [
        (
            "Learn Quart framework",
            "Follow the assignment and build the Task API",
            "pending",
            now,
            now,
        ),
        (
            "Build REST API",
            "Implement CRUD endpoints for tasks",
            "in_progress",
            now,
            now,
        ),
        (
            "Write unit tests",
            "Add pytest unit tests for the task endpoints",
            "completed",
            now,
            now,
        ),
    ]

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(
            """
            INSERT INTO tasks (title, description, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            sample_tasks,
        )
        # commit lo hace el context manager
