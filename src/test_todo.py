import pytest 

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app
from core.database.database import Base, get_session
from entities.tables.todo_table import TodoTable

# Configuración de la base de datos de prueba
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_db.db"

# Crear motor de base de datos SQLite
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

# Crear sesión de prueba
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Anular la dependencia de la base de datos
def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


# ========================
# FIXTURES
# ========================
@pytest.fixture(scope="function")
def db_session():
    """Configura la sesión de prueba con rollback al final."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Configura el cliente de prueba."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_session] = override_get_db
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def todo_payload():
    """Genera un payload para un Todo."""
    return {
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    }


# ========================
# PRUEBAS UNITARIAS
# ========================

def test_get_todos(test_client, db_session):
    # Crear datos de prueba
    todo = TodoTable(
        title="Initial Todo", 
        description="Test Description", 
        completed=False
    )
    db_session.add(todo)
    db_session.commit()

    # Ejecutar prueba
    response = test_client.get("/todo/all")
    assert response.status_code == 200
    todos = (response.json())['todos']
    assert isinstance(todos, list)
    
    assert len(todos) > 0
    assert todos[0]["title"] == todo.title


def test_create_todo(test_client, todo_payload):
    response = test_client.post("/todo/create", json=todo_payload)
    assert response.status_code == 201
    todo = (response.json())['todo']
    assert todo["title"] == todo_payload["title"]
    assert todo["description"] == todo_payload["description"]


def test_update_todo(test_client, db_session):
    # Crear un Todo para actualizar
    todo = TodoTable(
        title="Old Title", 
        description="Old Description", 
        completed=False
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    payload = {
        "title": "Updated Title",
        "description": "Updated Description",
        "completed": True
    }
    response = test_client.put(f"/todo/update/{todo.id}", json=payload)
    assert response.status_code == 200
    updated_todo = (response.json())['todo']
    assert updated_todo["title"] == payload["title"]
    assert updated_todo["description"] == payload["description"]


def test_delete_todo(test_client, db_session):
    # Crear un Todo para eliminar
    todo = TodoTable(
        title="To Delete", 
        description="To be deleted", 
        completed=False
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    response = test_client.delete(f"/todo/delete/{todo.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Todo deleted successfully"
