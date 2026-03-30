from pydantic import BaseModel
from typing import Optional

class MessageResponse(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str
    message: str

# Authentication Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    role: str = "doctor"  # doctor, lab_tech, or admin

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

