from sqlalchemy import Column, Integer, String, Boolean, DATETIME
from src.core.database.database import Base

class TodoTable(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(70), index=True)
    description = Column(String(255))
    date_created = Column(String(120), index=True)
    completed = Column(Boolean, index=True)
    
    def __to_dict__(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_created": self.date_created,
            "completed": "Completed" if self.completed else "Pending"
        }