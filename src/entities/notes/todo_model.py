from typing import Optional
from pydantic import BaseModel, ConfigDict


class TodoModel(BaseModel):
    title: str
    description: str
    completed: bool
    
    model_config = ConfigDict(
        from_attributes=True
        )
    
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False
    
    model_config = ConfigDict(
        from_attributes=True
    )