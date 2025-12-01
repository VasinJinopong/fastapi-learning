from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# Pydantic Model -> DTO
class PostCreate(BaseModel):
    title:str
    content: str
    published : bool = True ## เซต default เป็น true ถ้าหน้าบ้านไม่ได้มีการกำหนดค่ามาให้

## Pydantic Patch: PostUpdate
class PostUpdate(BaseModel):
    title : Optional[str] = None
    content: Optional[str] = None

## Pydantic Put: Postput
class PostPut(BaseModel):
    title : str
    content  : str    


## Pydantic Response
class PostResponse(PostCreate):
    id:int
    created_at :datetime

    class Config:
        from_attributes = True
