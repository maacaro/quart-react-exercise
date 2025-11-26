"""
Task Models
Database operations for tasks
"""
from typing import Optional, List, Dict, Any
from datetime import datetime
from backend.core.database import get_db_connection


def create_task(data: dict) -> dict:
    """
    Create a new task in the database.

    Args:
        data: Dictionary with task fields (title, description, status)

    Returns:
        dict: Created task with generated ID and timestamps
    """
    title = data["title"]
    description = data["description"]
    status = data.get("status", "pending")

    with get_db_connection() as conn:
        cursor = conn.cursor()
        # Insertar la nueva tarea
        cursor.execute(
            """
            INSERT INTO tasks (title, description, status, created_at, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (title, description, status),
        )
        task_id = cursor.lastrowid

        # Recuperar la fila recién insertada
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

    # row es un sqlite3.Row → lo convertimos a dict
    return dict(row)



def get_all_tasks() -> List[Dict[str, Any]]:
    """
    Retrieve all tasks from the database

    Returns:
        list: List of all tasks as dictionaries

    TODO: Implement this function
    Hints:
    - Use get_db_connection() from app.backend.core.database
    - SELECT all tasks and convert rows to dictionaries
    - Return empty list if no tasks exist
    """
    pass


def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single task by ID

    Args:
        task_id: The task ID to retrieve

    Returns:
        dict or None: Task dictionary if found, None otherwise

    TODO: Implement this function
    Hints:
    - Use get_db_connection() from app.backend.core.database
    - SELECT the task WHERE id = task_id
    - Return None if task doesn't exist
    """
    pass


def update_task(task_id: int, title: Optional[str] = None,
                description: Optional[str] = None,
                status: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Update an existing task

    Args:
        task_id: The task ID to update
        title: New title (optional)
        description: New description (optional)
        status: New status (optional)

    Returns:
        dict or None: Updated task if found, None otherwise

    TODO: Implement this function
    Hints:
    - First check if task exists using get_task_by_id()
    - Build UPDATE query dynamically based on which fields are provided
    - Always update the updated_at timestamp
    - Return the updated task
    """
    pass


def delete_task(task_id: int) -> bool:
    """
    Delete a task by ID

    Args:
        task_id: The task ID to delete

    Returns:
        bool: True if task was deleted, False if not found

    TODO: Implement this function
    Hints:
    - Use get_db_connection() from app.backend.core.database
    - DELETE FROM tasks WHERE id = task_id
    - Check cursor.rowcount to see if a row was deleted
    - Return True if deleted, False if task didn't exist
    """
    pass
