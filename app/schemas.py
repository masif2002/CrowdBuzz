from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel): # Response Model for user
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Post(PostBase): # Response model
    id: int
    created_at: datetime
    user_id: int
    user: UserOut # user relationship  field in models.py

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Token(BaseModel):
    token: str
    token_type: str
    
class Vote(BaseModel): 
    post_id: int
    dir: conint(le=1) # le - less than equal tol dor can onl be less than equal to 1
