"""
Unit tests for task API endpoints

Follow the TDD (Test-Driven Development) approach:
1. RED: Write a failing test
2. GREEN: Write minimal code to make it pass
3. REFACTOR: Improve the code while keeping tests passing

Run tests with: pytest tests/unit/test_tasks.py -v
"""
import pytest


class TestTaskCreation:
    """Tests for creating tasks"""

    @pytest.mark.asyncio
    async def test_create_task_success(self, client):
        """
        Test successful task creation with valid data.
        """
        # Arrange
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "status": "pending",
        }

        # Act
        response = await client.post("/api/tasks", json=task_data)

        # Assert
        assert response.status_code == 201

        data = await response.get_json()
        # ID generado
        assert "id" in data
        assert isinstance(data["id"], int)

        # Campos iguales a lo enviado
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]

        # Timestamps presentes
        assert "created_at" in data
        assert "updated_at" in data
        assert isinstance(data["created_at"], str)
        assert isinstance(data["updated_at"], str)
        assert data["created_at"]
        assert data["updated_at"]


    @pytest.mark.asyncio
    async def test_create_task_missing_title(self, client):
        """
        Test task creation fails when title is missing.

        Steps:
        1. Make POST request to /api/tasks without 'title' in JSON body
        2. Assert response status code is 400
        3. Assert response JSON contains error message about missing title
        """
        # Arrange: falta title
        task_data = {
            "description": "Description without title",
            "status": "pending",
        }

        # Act
        response = await client.post("/api/tasks", json=task_data)

        # Assert
        assert response.status_code == 400
        data = await response.get_json()
        assert "error" in data
        # mensaje menciona title
        assert "title" in data["error"].lower()
        # opcional: campo específico
        assert data.get("field") == "title"


    @pytest.mark.asyncio
    async def test_create_task_invalid_status(self, client):
        """
        Test that task creation fails when status is invalid.

        Valid statuses: pending, in_progress, completed
        """
        # Arrange: status inválido
        task_data = {
            "title": "Task with invalid status",
            "description": "Some description",
            "status": "invalid_status",
        }

        # Act
        response = await client.post("/api/tasks", json=task_data)

        # Assert
        assert response.status_code == 400
        data = await response.get_json()
        assert "error" in data
        assert "status" in data["error"].lower()
        assert data.get("field") == "status"
    


    @pytest.mark.asyncio
    async def test_create_task_missing_description(self, client):
        """
        Test that task creation fails when description is missing.

        In this exercise, we require both title and description.
        """
        # Arrange: falta description
        task_data = {
            "title": "Task without description",
            "status": "pending",
        }

        # Act
        response = await client.post("/api/tasks", json=task_data)

        # Assert
        assert response.status_code == 400
        data = await response.get_json()
        assert "error" in data
        assert "description" in data["error"].lower()
        assert data.get("field") == "description"







class TestTaskRetrieval:
    """Tests for retrieving tasks"""

    @pytest.mark.asyncio
    async def test_get_all_tasks_empty(self, client):
        """
        Test getting all tasks when database is empty

        TODO: Implement this test
        Steps:
        1. Make GET request to /api/tasks
        2. Assert response status is 200
        3. Assert response is an empty list
        """
        pass

    @pytest.mark.asyncio
    async def test_get_all_tasks_with_data(self, client):
        """
        Test getting all tasks when tasks exist

        TODO: Implement this test
        Steps:
        1. Create 2-3 tasks using POST /api/tasks
        2. Make GET request to /api/tasks
        3. Assert response status is 200
        4. Assert response contains all created tasks
        """
        pass

    @pytest.mark.asyncio
    async def test_get_task_by_id_success(self, client):
        """
        Test getting a specific task by ID

        TODO: Implement this test
        Steps:
        1. Create a task
        2. Make GET request to /api/tasks/{id}
        3. Assert response status is 200
        4. Assert response contains correct task data
        """
        pass

    @pytest.mark.asyncio
    async def test_get_task_by_id_not_found(self, client):
        """
        Test getting a task that doesn't exist returns 404

        TODO: Implement this test
        """
        pass







class TestTaskUpdate:
    """Tests for updating tasks"""

    @pytest.mark.asyncio
    async def test_update_task_success(self, client):
        """
        Test updating a task with valid data

        TODO: Implement this test
        Steps:
        1. Create a task
        2. Make PUT request to /api/tasks/{id} with updated data
        3. Assert response status is 200
        4. Assert response contains updated data
        5. Verify updated_at timestamp changed
        """
        pass

    @pytest.mark.asyncio
    async def test_update_task_partial(self, client):
        """
        Test updating only some fields of a task

        TODO: Implement this test
        Hint: Update only status, verify title and description unchanged
        """
        pass

    @pytest.mark.asyncio
    async def test_update_task_not_found(self, client):
        """
        Test updating a task that doesn't exist returns 404

        TODO: Implement this test
        """
        pass

    @pytest.mark.asyncio
    async def test_update_task_invalid_status(self, client):
        """
        Test updating a task with invalid status returns 400

        TODO: Implement this test
        """
        pass







class TestTaskDeletion:
    """Tests for deleting tasks"""

    @pytest.mark.asyncio
    async def test_delete_task_success(self, client):
        """
        Test deleting an existing task

        TODO: Implement this test
        Steps:
        1. Create a task
        2. Make DELETE request to /api/tasks/{id}
        3. Assert response status is 204
        4. Verify task no longer exists (GET returns 404)
        """
        pass

    @pytest.mark.asyncio
    async def test_delete_task_not_found(self, client):
        """
        Test deleting a task that doesn't exist returns 404

        TODO: Implement this test
        """
        pass


# BONUS: Integration tests
class TestTaskWorkflow:
    """Integration tests for complete task workflows"""

    @pytest.mark.asyncio
    async def test_complete_task_lifecycle(self, client):
        """
        Test the complete lifecycle of a task

        TODO: Implement this integration test
        Steps:
        1. Create a task with status 'pending'
        2. Update status to 'in_progress'
        3. Update status to 'completed'
        4. Verify task history at each step
        5. Delete the task
        6. Verify it's gone
        """
        pass
