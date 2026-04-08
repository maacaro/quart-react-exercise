"""
End-to-end tests for task management UI.

Estas pruebas usan Playwright (vía pytest) para simular interacciones reales
del usuario en el navegador.

IMPORTANTE (TDD):
- En este momento estos tests se van a romper (RED) porque todavía NO existe
  la página /tasks ni los data-testid que usamos aquí.
- En la Task 2.2 construiremos la UI de React para que estos tests pasen (GREEN).
"""

import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5173"


@pytest.mark.e2e
def test_view_tasks_page(page: Page):
    """Como usuario quiero ver una lista de mis tareas al abrir /tasks."""

    # 1. Navegar a la página de tareas
    page.goto(f"{BASE_URL}/tasks")

    # 2. Verificar que el título principal aparece
    #    (Luego en React pondremos un <h1>Tasks</h1>)
    heading = page.get_by_role("heading", name="Tasks")
    expect(heading).to_be_visible()

    # 3. Verificar que existe el contenedor de la lista
    expect(page.locator('[data-testid="task-list"]')).to_be_visible()

    # 4. Verificar que al menos hay una tarjeta de tarea (semilla o mock)
    first_card = page.locator('[data-testid="task-card"]').first
    expect(first_card).to_be_visible()


@pytest.mark.e2e
def test_create_task_flow(page: Page):
    """Flujo completo de creación de tarea desde la UI.

    Historia de usuario:
    Como usuario quiero crear una nueva tarea para poder seguir mi trabajo.

    Pasos:
    1. Ir a /tasks
    2. Click en "New Task"
    3. Rellenar título y descripción
    4. Elegir estado "pending"
    5. Click en "Create"
    6. Ver mensaje de éxito
    7. Ver la tarea en la lista
    """

    page.goto(f"{BASE_URL}/tasks")

    # Abrir formulario de nueva tarea
    page.click('[data-testid="new-task-btn"]')

    # Rellenar formulario
    page.fill('[data-testid="task-title-input"]', "Test Task")
    page.fill('[data-testid="task-description-input"]', "Test Description")
    page.select_option('[data-testid="task-status-select"]', "pending")

    # Enviar formulario
    page.click('[data-testid="create-task-btn"]')

    # Verificar mensaje de éxito
    expect(page.locator('[data-testid="success-message"]')).to_be_visible()

    # Verificar que la nueva tarea aparece en la lista
    task_card = page.locator('[data-testid="task-card"]').filter(
    has_text="Test Task",
        ).first

    expect(task_card).to_be_visible()
    expect(task_card).to_contain_text("Test Description")


@pytest.mark.e2e
def test_create_task_validation(page: Page):
    """Validación del formulario de creación de tarea.

    Historia:
    Como usuario, si intento crear una tarea inválida,
    quiero ver mensajes de error y que NO se cree la tarea.
    """

    page.goto(f"{BASE_URL}/tasks")

    # Abrir formulario
    page.click('[data-testid="new-task-btn"]')

    # Dejar el título vacío y hacer submit
    title_input = page.locator('[data-testid="task-title-input"]')
    title_input.fill("")  # nos aseguramos de que esté vacío

    page.click('[data-testid="create-task-btn"]')

    # Ver mensaje de error
    error = page.locator('[data-testid="error-message"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Title is required")


@pytest.mark.e2e
def test_update_task_status(page: Page):
    """Actualizar el estado de una tarea desde la UI.

    Historia:
    Como usuario quiero poder cambiar el estado de una tarea
    (por ejemplo de 'pending' a 'in_progress').
    """

    page.goto(f"{BASE_URL}/tasks")

    # Tomamos la primera tarjeta de tarea
    task_card = page.locator('[data-testid="task-card"]').first
    expect(task_card).to_be_visible()

    status_select = task_card.locator('[data-testid="task-status-select"]')

    # (Más adelante, cuando la UI exista, podemos comprobar que inicialmente es "pending")
    # expect(status_select).to_have_value("pending")

    # Cambiar a "in_progress"
    status_select.select_option("in_progress")

    # Guardar cambios
    task_card.locator('[data-testid="task-save-btn"]').click()

    # Verificar que el estado cambió en la UI
    expect(status_select).to_have_value("in_progress")


@pytest.mark.e2e
def test_delete_task(page: Page):
    """Eliminar una tarea desde la UI.

    Historia:
    Como usuario quiero poder eliminar una tarea completada.
    """

    page.goto(f"{BASE_URL}/tasks")

    # 1️⃣ Crear una tarea que luego vamos a borrar
    page.click('[data-testid="new-task-btn"]')
    page.fill('[data-testid="task-title-input"]', "Task to delete")
    page.fill('[data-testid="task-description-input"]', "Temporary task")
    page.select_option('[data-testid="task-status-select"]', "completed")
    page.click('[data-testid="create-task-btn"]')

    # 2️⃣ Localizar la tarjeta de esa tarea
    cards = page.locator('[data-testid="task-card"]')
    task_card = cards.filter(has_text="Task to delete").first

    expect(task_card).to_be_visible()

    # 3️⃣ Click en eliminar
    task_card.locator('[data-testid="task-delete-btn"]').click()

    # 4️⃣ Confirmar en el diálogo
    page.click('[data-testid="confirm-delete-btn"]')

    # 5️⃣ Verificar que ya no se ve esa tarjeta
    expect(task_card).not_to_be_visible()
