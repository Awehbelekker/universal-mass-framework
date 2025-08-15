import pytest
from universal_mass_framework.app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    """Test the hello world endpoint."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Hello, World from MASS Backend!' in response.data
