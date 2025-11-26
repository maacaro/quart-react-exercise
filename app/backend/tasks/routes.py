"""
Task Routes
API endpoints for task management
"""
from quart import Blueprint, request, jsonify
from backend import tasks as tasks_pkg  # opcional, pero vamos a usar models
from backend.tasks import models

VALID_STATUSES = ["pending", "in_progress", "completed"]

# Create the tasks blueprint
tasks_bp = Blueprint('tasks', __name__)


@tasks_bp.route("/tasks", methods=["POST"])
async def create_task():
    """
    Create a new task.
    """
    # 1. Obtener JSON
    data = await request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    title = data.get("title")
    description = data.get("description")
    status = data.get("status", "pending")

    # 2. Validaciones
    if not title or not str(title).strip():
        return jsonify({"error": "Title is required", "field": "title"}), 400

    if not description or not str(description).strip():
        return jsonify(
            {"error": "Description is required", "field": "description"}
        ), 400

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

    # 3. Crear tarea en la DB (modelo síncrono)
    created_task = models.create_task(
        {
            "title": title.strip(),
            "description": description.strip(),
            "status": status,
        }
    )

    # 4. Devolver JSON con 201
    return jsonify(created_task), 201



@tasks_bp.route('/tasks', methods=['GET'])
async def get_all_tasks():
    """
    Get all tasks

    Returns:
        200: List of all tasks

    TODO: Implement this endpoint
    Hints:
    - Call models.get_all_tasks()
    - Return the list of tasks with status code 200
    """
    pass


@tasks_bp.route('/tasks/<int:task_id>', methods=['GET'])
async def get_task(task_id: int):
    """
    Get a single task by ID

    Args:
        task_id: Task ID from URL path

    Returns:
        200: Task data
        404: Task not found

    TODO: Implement this endpoint
    Hints:
    - Call models.get_task_by_id(task_id)
    - If task is None, return {'error': 'Task not found'} with status 404
    - Otherwise return the task with status 200
    """
    pass


@tasks_bp.route('/tasks/<int:task_id>', methods=['PUT'])
async def update_task(task_id: int):
    """
    Update an existing task

    Args:
        task_id: Task ID from URL path

    Request body (all fields optional):
        {
            "title": "string",
            "description": "string",
            "status": "pending|in_progress|completed"
        }

    Returns:
        200: Updated task
        400: Invalid request data
        404: Task not found

    TODO: Implement this endpoint
    Hints:
    - Use await request.get_json() to get request data
    - Validate status if provided (must be pending, in_progress, or completed)
    - Call models.update_task() with task_id and provided fields
    - If result is None, return {'error': 'Task not found'} with status 404
    - Otherwise return the updated task with status 200
    """
    pass


@tasks_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
async def delete_task(task_id: int):
    """
    Delete a task

    Args:
        task_id: Task ID from URL path

    Returns:
        204: Task deleted successfully
        404: Task not found

    TODO: Implement this endpoint
    Hints:
    - Call models.delete_task(task_id)
    - If result is False, return {'error': 'Task not found'} with status 404
    - If result is True, return empty response with status 204
    - For 204, use: return '', 204
    """
    pass
