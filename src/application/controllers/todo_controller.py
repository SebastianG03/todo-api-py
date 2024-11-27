from fastapi import APIRouter, Depends

from core.database.database import get_session, Session
import core.datasource.todo_datasource as ds

from entities.notes.todo_model import TodoModel, TodoUpdate

todo_router = APIRouter(prefix="/todo", tags=["todo"])

@todo_router.get("/")
def get_todos(session: Session = Depends(get_session)):
    return ds.get_todos(session=session)

@todo_router.post("/")
def create_todo(todo: TodoModel, session: Session = Depends(get_session)):
    return ds.create_todo(todo=todo, session=session)

@todo_router.put("/{id}")
def update_todo(id: int, todo: TodoUpdate, session: Session = Depends(get_session)):
    return ds.update_todo(id=id, todo=todo, session=session)

@todo_router.delete("/{id}")
def delete_todo(id: int, session: Session = Depends(get_session)):
    return ds.delete_todo(id=id, session=session)