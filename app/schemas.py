from datetime import datetime
from pydantic import BaseModel, EmailStr

# user's model
class UserBase(BaseModel):
    email: EmailStr


class UserCreateModel(UserBase):
    username: str
    password: str


class UserResponseModel(UserBase):
    username: str
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True


class UserUpdateModel(BaseModel):
    username: str


class TokenData(BaseModel):
    access_token: str
    token_type: str
    
    class Config:
        orm_mode = True

class TokenPayload(BaseModel):
    id: str
    exp: datetime
    

class Task(BaseModel):
    task: str
    time_due: datetime
    remind_me: bool
    repeat: bool
    

class TaskResponseModel(Task):
    is_active: bool
    id: str
    user: UserResponseModel

    class Config:
        orm_mode = True
