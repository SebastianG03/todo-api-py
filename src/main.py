from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from src.core.database.database import Base, engine

from src.application.controllers.todo_controller import todo_router 

Base.metadata.create_all(bind = engine)

def create_app() -> FastAPI:
    application = FastAPI()
    application.add_middleware(GZipMiddleware)
    application.include_router(todo_router)
    return application


app = create_app()

