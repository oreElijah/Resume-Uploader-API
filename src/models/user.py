from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict

class Role(Enum):
    """Enum for role types"""
    worker="worker"
    hirer="hirer"

class UserIn(BaseModel):    
    """UserIn model definition"""
    first_name: str
    last_name: str
    username: str
    role: Role
    email: str
    password: str   

class User(UserIn):
    """User model definition"""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]=None

class UserLogin(BaseModel):    
    """UserLogIn model definition"""
    email: str
    password: str      
    id: Optional[int]=None
