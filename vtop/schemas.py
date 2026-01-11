from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional



class user(BaseModel):
    name: str
    password: str
    role: str
    
class UserLogin(BaseModel):
    email: str
    password: str

class SelectSubjectRequest(BaseModel):
    subject_id: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token :str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] =None

class UserCreate(BaseModel):
    email:EmailStr
    password: str