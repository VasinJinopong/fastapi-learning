from pydantic import BaseModel,EmailStr
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


    # from_attributes= True คืออนุญาติให้ pydantic read data จาก ORM object
    class Config:
        from_attributes = True



class UserCreate(BaseModel):
    email: EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email: EmailStr
    created_at :datetime


class UserLogin(BaseModel):
    email :EmailStr
    password :str



class Token(BaseModel):
    access_token: str
    token_type  :str


class TokenData(BaseModel):
    id: Optional[str] = None        