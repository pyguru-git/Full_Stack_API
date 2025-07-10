from datetime import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr, conint


class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class User(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass 

class Post(PostBase):
    id: int
    created_at: datetime
    user_id : int
    user : User

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True




class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)