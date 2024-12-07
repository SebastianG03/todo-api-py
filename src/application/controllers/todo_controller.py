from fastapi import APIRouter, Depends

from core.database.database import get_session, Session
from core.services.logger_service import logger

import core.datasource.todo_datasource as ds

from entities.notes.todo_model import TodoModel, TodoUpdate

todo_router = APIRouter(prefix="/todo", tags=["todo"])

@todo_router.get("/all", status_code=200)
def get_todos(session: Session = Depends(get_session)):
    return ds.get_todos(session=session)

@todo_router.post("/create", status_code=201)
def create_todo(todo: TodoModel, session: Session = Depends(get_session)):
    return ds.create_todo(todo=todo, session=session)

@todo_router.put("/update/{id}", status_code=200)
def update_todo(id: int,
                todo: TodoUpdate, 
                session: Session = Depends(get_session)):
    logger.info("Updating todo with id: %s", id)
    return ds.update_todo(id=id, todo=todo, session=session)

@todo_router.delete("/delete/{id}", status_code=200)
def delete_todo(id: int, session: Session = Depends(get_session)):
    return ds.delete_todo(id=id, session=session)