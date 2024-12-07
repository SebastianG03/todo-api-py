import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.core.database.database import Base, get_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from src.entities.tables.todo_table import TodoTable


SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
TestEngine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TestEngine)

Base.metadata.create_all(bind=TestEngine)

def override_get_session():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)

class TestTodoAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Ejecutado una vez antes de todas las pruebas"""
        cls.db = TestingSessionLocal()

    @classmethod
    def tearDownClass(cls):
        """Finalizando las pruebas"""
        cls.db.close()

    def setUp(self):
        """Preparar datos antes de cada prueba"""
        self.todo = TodoTable(
            title="Initial Todo", description="Test Description", completed=False
        )
        self.db.add(self.todo)
        self.db.commit()
        self.db.refresh(self.todo)

    def tearDown(self):
        """Limpieza de datos después de cada prueba"""
        self.db.query(TodoTable).delete()
        self.db.commit()

    def test_get_todos(self):
        response = client.get("/todo/all")
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertIsInstance(todos, list)
        self.assertGreater(len(todos), 0)
        self.assertEqual(todos[0]["title"], "Initial Todo")

    def test_create_todo(self):
        payload = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "completed": False
        }
        response = client.post("/todo/create", json=payload)
        self.assertEqual(response.status_code, 201)
        todo = response.json()  
        self.assertEqual(todo["title"], payload["title"])

    def test_update_todo(self):
        payload = {
            "title": "Updated Title",
            "description": "Updated Description",
            "completed": True
        }
        response = client.put(f"/todo/update/1", json=payload)
        self.assertEqual(response.status_code, 200)
        updated_todo = response.json()
        self.assertEqual(updated_todo["title"], payload["title"])

    def test_delete_todo(self):
        response = client.delete(f"/todo/delete/{self.todo.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Todo deleted successfully")

if __name__ == "__main__":
    unittest.main()
