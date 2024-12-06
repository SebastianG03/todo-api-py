from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

def test_get_todos():
    response = client.get("/todo/all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_todo():
    payload = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    }
    response = client.post("/todo/create", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]

def test_update_todo():
    payload = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }
    response = client.put("/todo/update/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == payload["title"]

def test_delete_todo():
    response = client.delete("/todo/delete/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"
