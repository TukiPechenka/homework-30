from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_status_code_recipes():
    response = client.get('/recipes/')
    assert response.status_code == 200