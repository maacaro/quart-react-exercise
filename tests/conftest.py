"""
pytest configuration and fixtures
"""
import pytest
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
app_dir = Path(__file__).parent.parent / 'app'
sys.path.insert(0, str(app_dir))

from backend.app import create_app
from backend.core.database import init_db, get_db_path


@pytest.fixture
async def app():
    """
    Create a test application instance

    This fixture creates a fresh app instance for each test
    with a test database.
    """
    # Use a test database
    os.environ['DATABASE_URL'] = 'test_practice_exercise.db'

    # Initialize the database
    init_db()

    app = create_app()

    yield app

    # Cleanup: Remove test database
    db_path = get_db_path()
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
async def client(app):
    """
    Create a test client for making requests

    Usage in tests:
        async def test_something(client):
            response = await client.get('/api/tasks')
            assert response.status_code == 200
    """
    async with app.test_client() as client:
        yield client
