import datetime
from fastapi.responses import JSONResponse
from fastapi import status

from entities.notes.todo_model import TodoModel, TodoUpdate
from entities.tables.todo_table import TodoTable
from core.database.database import Session

def create_todo(todo: TodoModel, session: Session):
    try:
        todo_db = TodoTable()
        todo_db.title = todo.title
        todo_db.description = todo.description
        todo_db.date_created = datetime.datetime.now()  
        todo_db.completed = todo.completed
        
        session.add(todo_db)
        session.commit()
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Todo created successfully",
                "Todo Data": todo_db.__to_dict__()
                }
        )
          
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )

def get_todos(session: Session):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Todos": [todo.__to_dict__() for todo in session.query(TodoTable)]
        }
    )

def update_todo(id: int, todo: TodoUpdate, session: Session):
    try:
        original_todo = session.query(TodoTable).filter(TodoTable.id == id).first()
        
        todo_db = _check_todo_data(new_todo=todo, original_todo=original_todo)
        
        session.commit()
        session.refresh(todo_db)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Todo updated successfully",
                "Todo Data": todo_db.__to_dict__()
                }
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )

def delete_todo(id: int, session: Session):
    try:
        todo = session.query(TodoTable).filter(TodoTable.id == id).first()

        if not todo:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Todo not found"}
            )

        session.delete(todo)
        session.commit()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Todo deleted successfully"}
        )
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": str(e)}
        )

def _check_todo_data(new_todo: TodoUpdate, original_todo: TodoTable) -> TodoTable:
    
    if (new_todo.new_todo is not None and
        new_todo.title.strip('') != "" and
        original_todo.title != new_todo.title 
        ):
        original_todo.title = new_todo.title
        
    if (new_todo.description is not None and
        new_todo.description.strip('') != "" and
        original_todo.description != new_todo.description):
        original_todo.description = new_todo.description
        
    if original_todo.completed != new_todo.completed:
        original_todo.completed = new_todo.completed
        
    original_todo.date_created = datetime.datetime.now()
    
    updated_todo = TodoTable()
    updated_todo.id = original_todo.id
    updated_todo.title = original_todo.title
    updated_todo.description = original_todo.description
    updated_todo.date_created = original_todo.date_created
    updated_todo.completed = original_todo.completed
    
    return update_todo