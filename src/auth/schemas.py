
from sqlmodel import SQLModel
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    username:str = Field(max_length=15)
    email:str = Field(max_length=40)
    password:str = Field(min_length=6)
    first_name:str = Field(max_length=10)
    last_name:str=Field(max_length=10)
    
    
class UserModel(BaseModel):
    uid:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool
    hash_password:str
    created_at: datetime 
    updated_at: datetime
    
    
class UserLoginModel(BaseModel):
    email:str = Field(max_length=40)
    password:str = Field(min_length=6)