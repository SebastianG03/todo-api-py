from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Create an instance of SQLite engine
engine = create_engine("sqlite:///employeesdb.db", echo=True)

# Create an instance of DeclarativeMeta
Base = declarative_base()

# Create the SessionLocal class from sessionmaker factory
SessionLocal: sessionmaker[Session] = sessionmaker(bind=engine, expire_on_commit=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()