"""
Unit tests for task API endpoints.

Seguimos el enfoque TDD:
1. RED: escribir un test que falle
2. GREEN: escribir el mínimo código para que pase
3. REFACTOR: mejorar manteniendo los tests en verde

Se ejecutan con:
    pytest tests/unit/test_tasks.py -m unit -v
"""

import pytest


class TestTaskCreation:
    """Tests para la creación de tareas (POST /api/tasks)."""

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_task_success(self, client):
        """
        Creación exitosa con datos válidos.
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
    @pytest.mark.unit
    async def test_create_task_missing_title(self, client):
        """
        Debe fallar si falta el título.
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
        assert "title" in data["error"].lower()
        assert data.get("field") == "title"

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_task_invalid_status(self, client):
        """
        Debe fallar si el status es inválido.
        Status válidos: pending, in_progress, completed.
        """
        task_data = {
            "title": "Task with invalid status",
            "description": "Some description",
            "status": "invalid_status",
        }

        response = await client.post("/api/tasks", json=task_data)

        assert response.status_code == 400
        data = await response.get_json()
        assert "error" in data
        assert "status" in data["error"].lower()
        assert data.get("field") == "status"

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_task_missing_description(self, client):
        """
        Debe fallar si falta la descripción.
        (En este ejercicio requerimos título y descripción.)
        """
        task_data = {
            "title": "Task without description",
            "status": "pending",
        }

        response = await client.post("/api/tasks", json=task_data)

        assert response.status_code == 400
        data = await response.get_json()
        assert "error" in data
        assert "description" in data["error"].lower()
        assert data.get("field") == "description"

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_create_task_default_status(self, client):
        """
        Si no se envía 'status', debe quedar en 'pending' por defecto.
        """
        task_data = {
            "title": "Task without explicit status",
            "description": "Some description",
            # sin campo "status"
        }

        response = await client.post("/api/tasks", json=task_data)

        assert response.status_code == 201
        data = await response.get_json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == "pending"


class TestTaskRetrieval:
    """Tests for retrieving tasks (GET /api/tasks, GET /api/tasks/{id})."""

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_all_tasks_empty(self, client):
        """
        Cuando la BD está vacía, debe devolver lista vacía.
        """
        response = await client.get("/api/tasks")

        assert response.status_code == 200
        data = await response.get_json()
        assert isinstance(data, list)
        assert data == []

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_all_tasks_with_data(self, client):
        """
        Obtener todas las tareas cuando existen registros.
        """
        # Arrange: crear 2 tareas
        task_1 = {
            "title": "Task 1",
            "description": "Description 1",
            "status": "pending",
        }
        task_2 = {
            "title": "Task 2",
            "description": "Description 2",
            "status": "completed",
        }

        resp1 = await client.post("/api/tasks", json=task_1)
        assert resp1.status_code == 201
        resp2 = await client.post("/api/tasks", json=task_2)
        assert resp2.status_code == 201

        # Act
        resp = await client.get("/api/tasks")

        # Assert
        assert resp.status_code == 200
        data = await resp.get_json()
        assert isinstance(data, list)

        titles = {t["title"] for t in data}
        assert "Task 1" in titles
        assert "Task 2" in titles

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_task_by_id_success(self, client):
        """
        Obtener una tarea específica por ID.
        """
        # Arrange
        task = {
            "title": "Single Task",
            "description": "Some description",
            "status": "in_progress",
        }

        resp_create = await client.post("/api/tasks", json=task)
        assert resp_create.status_code == 201
        created = await resp_create.get_json()
        task_id = created["id"]

        # Act
        resp = await client.get(f"/api/tasks/{task_id}")

        # Assert
        assert resp.status_code == 200
        data = await resp.get_json()
        assert data["id"] == task_id
        assert data["title"] == task["title"]
        assert data["description"] == task["description"]
        assert data["status"] == task["status"]

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_task_by_id_not_found(self, client):
        """
        Debe devolver 404 si la tarea no existe.
        """
        resp = await client.get("/api/tasks/999999")
        assert resp.status_code == 404
        data = await resp.get_json()
        assert "error" in data
        assert "not found" in data["error"].lower()


class TestTaskUpdate:
    """Tests for updating tasks (PUT /api/tasks/{id})."""

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_task_success(self, client):
        """
        Actualizar todos los campos de una tarea con datos válidos.
        """
        # Arrange: crear tarea
        task = {
            "title": "Old title",
            "description": "Old description",
            "status": "pending",
        }
        resp_create = await client.post("/api/tasks", json=task)
        assert resp_create.status_code == 201
        created = await resp_create.get_json()
        task_id = created["id"]
        original_updated_at = created["updated_at"]

        # Act: actualizar
        update_data = {
            "title": "New title",
            "description": "New description",
            "status": "completed",
        }
        resp_update = await client.put(f"/api/tasks/{task_id}", json=update_data)

        # Assert
        assert resp_update.status_code == 200
        updated = await resp_update.get_json()
        assert updated["id"] == task_id
        assert updated["title"] == update_data["title"]
        assert updated["description"] == update_data["description"]
        assert updated["status"] == update_data["status"]
        assert updated["updated_at"] != original_updated_at

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_task_partial(self, client):
        """
        Actualizar solo algunos campos (ej: solo el status).
        """
        task = {
            "title": "Keep this title",
            "description": "Keep this description",
            "status": "pending",
        }
        resp_create = await client.post("/api/tasks", json=task)
        assert resp_create.status_code == 201
        created = await resp_create.get_json()
        task_id = created["id"]

        # Act: solo cambiamos el status
        resp_update = await client.put(
            f"/api/tasks/{task_id}", json={"status": "in_progress"}
        )

        assert resp_update.status_code == 200
        updated = await resp_update.get_json()
        assert updated["id"] == task_id
        assert updated["status"] == "in_progress"
        # título y descripción deben mantenerse
        assert updated["title"] == task["title"]
        assert updated["description"] == task["description"]

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_task_not_found(self, client):
        """
        Debe devolver 404 si se intenta actualizar una tarea inexistente.
        """
        resp_update = await client.put(
            "/api/tasks/999999",
            json={"title": "Does not matter"},
        )

        assert resp_update.status_code == 404
        data = await resp_update.get_json()
        assert "error" in data
        assert "not found" in data["error"].lower()

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_task_invalid_status(self, client):
        """
        Debe devolver 400 si el status enviado es inválido.
        """
        # Arrange: crear tarea válida
        task = {
            "title": "Task with bad update",
            "description": "Desc",
            "status": "pending",
        }
        resp_create = await client.post("/api/tasks", json=task)
        assert resp_create.status_code == 201
        created = await resp_create.get_json()
        task_id = created["id"]

        # Act: intentar actualizar con status inválido
        resp_update = await client.put(
            f"/api/tasks/{task_id}",
            json={"status": "not_a_valid_status"},
        )

        # Assert
        assert resp_update.status_code == 400
        data = await resp_update.get_json()
        assert "error" in data
        assert "invalid status" in data["error"].lower()
        assert data.get("field") == "status"


class TestTaskDeletion:
    """Tests for deleting tasks (DELETE /api/tasks/{id})."""

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_task_success(self, client):
        """
        Eliminar una tarea existente.
        """
        # Arrange: crear tarea
        task = {
            "title": "To be deleted",
            "description": "Delete me",
            "status": "pending",
        }
        resp_create = await client.post("/api/tasks", json=task)
        assert resp_create.status_code == 201
        created = await resp_create.get_json()
        task_id = created["id"]

        # Act: borrar
        resp_delete = await client.delete(f"/api/tasks/{task_id}")

        # Assert
        assert resp_delete.status_code == 204

        # Verificar que ya no existe
        resp_get = await client.get(f"/api/tasks/{task_id}")
        assert resp_get.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_task_not_found(self, client):
        """
        Debe devolver 404 al intentar borrar una tarea inexistente.
        """
        resp_delete = await client.delete("/api/tasks/999999")
        assert resp_delete.status_code == 404
        data = await resp_delete.get_json()
        assert "error" in data
        assert "not found" in data["error"].lower()


# BONUS: Integration tests
class TestTaskWorkflow:
    """Integration tests for complete task workflows."""

    @pytest.mark.asyncio
    async def test_complete_task_lifecycle(self, client):
        """
        Ciclo de vida completo:
        crear -> in_progress -> completed -> borrar.
        (Test de integración, sin marcar como 'unit'.)
        """
        # 1. Crear tarea en pending
        task_data = {
            "title": "Lifecycle task",
            "description": "Testing full lifecycle",
            "status": "pending",
        }
        resp_create = await client.post("/api/tasks", json=task_data)
        assert resp_create.status_code == 201
        created = await resp_create.get_json()
        task_id = created["id"]

        # 2. Cambiar a in_progress
        resp_update_1 = await client.put(
            f"/api/tasks/{task_id}", json={"status": "in_progress"}
        )
        assert resp_update_1.status_code == 200
        data_1 = await resp_update_1.get_json()
        assert data_1["status"] == "in_progress"

        # 3. Cambiar a completed
        resp_update_2 = await client.put(
            f"/api/tasks/{task_id}", json={"status": "completed"}
        )
        assert resp_update_2.status_code == 200
        data_2 = await resp_update_2.get_json()
        assert data_2["status"] == "completed"

        # 4. Borrar la tarea
        resp_delete = await client.delete(f"/api/tasks/{task_id}")
        assert resp_delete.status_code == 204

        # 5. Verificar que ya no existe
        resp_get = await client.get(f"/api/tasks/{task_id}")
        assert resp_get.status_code == 404
