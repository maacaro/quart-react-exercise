"""
pytest configuration and fixtures (global for tests/)
"""

import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio

# === Rutas / imports ===
# tests/conftest.py -> tests -> (subes un nivel) -> raíz del repo
ROOT_DIR = Path(__file__).resolve().parents[1]
APP_DIR = ROOT_DIR / "app"

# Añadimos la carpeta app/ al PYTHONPATH para poder hacer `from backend...`
sys.path.insert(0, str(APP_DIR))

from backend.app import create_app
from backend.core.database import init_db, get_db_path


# === Fixtures async ===

@pytest_asyncio.fixture
async def app():
    """
    Crea una instancia de la app para cada test (con BD de pruebas).
    """
    # Usar una base de datos de test
    os.environ["DATABASE_URL"] = "test_practice_exercise.db"

    # Inicializar el esquema de la BD (función SINCRONA)
    init_db()

    app = create_app()

    yield app

    # Limpiar BD de test al terminar
    db_path = get_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest_asyncio.fixture
async def client(app):
    """
    Cliente de test para hacer requests async.

    Ejemplo de uso en tests:
        async def test_algo(client):
            response = await client.get('/api/tasks')
            assert response.status_code == 200
    """
    async with app.test_client() as test_client:
        yield test_client
