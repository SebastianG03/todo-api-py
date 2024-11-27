from sqlalchemy import Column, Integer, String, Boolean, DATETIME
from core.database.database import Base

class TodoTable(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(70), index=True)
    description = Column(String(255), index=True)
    date_created = Column(DATETIME, index=True)
    completed = Column(Boolean, index=True)
    
    def __to_dict__(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_created": self.date_created,
            "completed": "Completed" if self.completed else "Pending"
        }