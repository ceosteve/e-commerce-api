
from datetime import date
from turtle import st
from pydantic import BaseModel, EmailStr, constr
from typing import Optional

from app.models import GenderEnum, UserRole



# create users schema
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderEnum
    birth_date: date
    role: UserRole
    password: str

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    gender: GenderEnum
    birth_date: date


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
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[int] = None

class TokenOut(BaseModel):
    access_token: str
    token_type: str
    refresh_token : str

class RefreshRequest(BaseModel):
    refresh_token: str

class ProductCreate(BaseModel):
    name: str
    description: str
    brand: str
    price: int
    stock: int

class ProductOut(ProductCreate):
    pass

    class Config:
        from_attributes = True

class ProductUpdate(ProductCreate):
    pass

    class Config:
        from_atrributes=True



