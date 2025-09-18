
from datetime import date
from pydantic import BaseModel, EmailStr, constr
from typing import Optional

from app.models import GenderEnum



# create users schema
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderEnum
    birth_date: date
    password: str
    


# user response upon creating account
class UserOut(BaseModel):
    email: str
    id : int


# response model for getting one's profile

class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email : str

    class Config:
        fromt_attributes = True

class TokenData(BaseModel):
    id: Optional[int] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str
    refresh_token : str

class RefreshRequest(BaseModel):
    refresh_token: str