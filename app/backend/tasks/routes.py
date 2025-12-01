"""
Task Routes
API endpoints for task management
"""
from quart import Blueprint, request, jsonify
from backend.tasks import models

VALID_STATUSES = ["pending", "in_progress", "completed"]

# Create the tasks blueprint
tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/tasks", methods=["POST"])
async def create_task():
    """
    Create a new task.
    """
    data = await request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "pending")

    # Validaciones
    if not title or not str(title).strip():
        return jsonify({"error": "Title is required", "field": "title"}), 400

    if not description or not str(description).strip():
        return (
            jsonify(
                {"error": "Description is required", "field": "description"}
            ),
            400,
        )

    if status not in VALID_STATUSES:
        return (
            jsonify(
                {
                    "error": (
                        "Invalid status. Must be one of: "
                        + ", ".join(VALID_STATUSES)
                    ),
                    "field": "status",
                }
            ),
            400,
        )

    created_task = models.create_task(
        {
            "title": title.strip(),
            "description": description.strip(),
            "status": status,
        }
    )

    return jsonify(created_task), 201


@tasks_bp.route("/tasks", methods=["GET"])
async def get_all_tasks():
    """
    Get all tasks.

    Returns:
        200: List of all tasks.
    """
    tasks = models.get_all_tasks()
    return jsonify(tasks), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["GET"])
async def get_task(task_id: int):
    """
    Get a single task by ID.

    Returns:
        200: Task data
        404: Task not found
    """
    task = models.get_task_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["PUT"])
async def update_task(task_id: int):
    """
    Update an existing task.

    Request body (all fields optional):
        {
            "title": "string",
            "description": "string",
            "status": "pending|in_progress|completed"
        }
    """
    data = await request.get_json() or {}

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")

    # Validar status solo si viene en el body
    if status is not None and status not in VALID_STATUSES:
        return (
            jsonify(
                {
                    "error": (
                        "Invalid status. Must be one of: "
                        + ", ".join(VALID_STATUSES)
                    ),
                    "field": "status",
                }
            ),
            400,
        )

    # (Opcional) Si no se manda nada, podemos rechazar
    if title is None and description is None and status is None:
        return (
            jsonify({"error": "No fields to update"}),
            400,
        )

    updated = models.update_task(
        task_id,
        title=title,
        description=description,
        status=status,
    )

    if updated is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(updated), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
async def delete_task(task_id: int):
    """
    Delete a task.

    Returns:
        204: Task deleted successfully
        404: Task not found
    """
    deleted = models.delete_task(task_id)

    if not deleted:
        return jsonify({"error": "Task not found"}), 404

    # Respuesta vacía con 204
    return "", 204
