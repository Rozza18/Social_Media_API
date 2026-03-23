from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime

#automatically performing type validation
class PostBase(BaseModel): #to be  used as a body schema for post create request
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config: #that is to convert the orm to dictionary
        from_attributes = True


#brand new class for the response
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config: #that is to convert the orm to dictionary
        from_attributes = True

class PostWithVote(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


#pydantic model for users
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

#token data schema
class TokenData(BaseModel):
    id: int


class Vote(BaseModel):#request body to create/remove vote
    post_id: int
    dir: conint(le=1) #type: ignore

class GetVote(BaseModel):
    post_id: int

