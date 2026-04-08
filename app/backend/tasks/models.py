"""
Task Models
Database operations for tasks
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from backend.core.database import get_db_connection


def init_db() -> None:
    """Crear la tabla tasks si no existe.

    Esta función se ejecuta una sola vez para inicializar la base de datos SQLite.
    """
    # 👇 IMPORTANTE: usar get_db_connection() como context manager
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('pending', 'in_progress', 'completed')),
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


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
        # Insert new task
        cursor.execute(
            """
            INSERT INTO tasks (title, description, status, created_at, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (title, description, status),
        )
        task_id = cursor.lastrowid

        # Fetch inserted row
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

    return dict(row)


def get_all_tasks() -> List[Dict[str, Any]]:
    """
    Retrieve all tasks from the database.

    Returns:
        list: List of all tasks as dictionaries.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY id")
        rows = cursor.fetchall()

    return [dict(row) for row in rows]


def get_task_by_id(task_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve a single task by ID.

    Args:
        task_id: The task ID to retrieve.

    Returns:
        dict or None: Task dictionary if found, None otherwise.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

    if row is None:
        return None

    return dict(row)


def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Update an existing task.

    Args:
        task_id: The task ID to update
        title: New title (optional)
        description: New description (optional)
        status: New status (optional)

    Returns:
        dict or None: Updated task if found, None otherwise
    """
    # Primero verificamos si la tarea existe
    existing = get_task_by_id(task_id)
    if existing is None:
        return None

    fields: list[str] = []
    params: list[Any] = []

    if title is not None:
        fields.append("title = ?")
        params.append(title)

    if description is not None:
        fields.append("description = ?")
        params.append(description)

    if status is not None:
        fields.append("status = ?")
        params.append(status)

    # Generamos un timestamp nuevo con más precisión (microsegundos)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    fields.append("updated_at = ?")
    params.append(now)

    set_clause = ", ".join(fields)

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE tasks SET {set_clause} WHERE id = ?",
            (*params, task_id),
        )

        # Volvemos a leer la fila actualizada
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()

    if row is None:
        return None

    return dict(row)


def delete_task(task_id: int) -> bool:
    """
    Delete a task by ID.

    Args:
        task_id: The task ID to delete.

    Returns:
        bool: True if task was deleted, False if not found.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        # rowcount = number of rows affected
        return cursor.rowcount > 0
