import datetime
from typing import Optional
from pydantic import BaseModel


class TodoModel(BaseModel):
    title: str
    description: str
    completed: bool
    
    class Config():
        orm_mode = True
        from_attributes = True
        
    
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False
    
    class Config():
        orm_mode = True
        from_attributes = True
    