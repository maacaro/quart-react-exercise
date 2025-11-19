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
        Test creating a task with valid data

        TODO: Implement this test
        Steps:
        1. Make POST request to /api/tasks with valid task data
        2. Assert response status is 201
        3. Assert response contains task with correct data
        4. Assert task has an id, created_at, and updated_at
        """
        pass

    @pytest.mark.asyncio
    async def test_create_task_missing_title(self, client):
        """
        Test creating a task without a title returns 400

        TODO: Implement this test
        """
        pass

    @pytest.mark.asyncio
    async def test_create_task_missing_description(self, client):
        """
        Test creating a task without a description returns 400

        TODO: Implement this test
        """
        pass

    @pytest.mark.asyncio
    async def test_create_task_invalid_status(self, client):
        """
        Test creating a task with invalid status returns 400

        TODO: Implement this test
        Hint: Test with status like 'invalid_status'
        """
        pass


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
