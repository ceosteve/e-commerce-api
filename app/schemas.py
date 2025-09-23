
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


from app import models
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

class CreateOrderItem(BaseModel):
    product_id: int
    item_quantity: int

class CreateOrder(BaseModel):
    items:List[CreateOrderItem]

class OrderItemOut(CreateOrderItem):
    unit_price: Decimal

    class Config:
        from_attributes=True


class OrderOut(BaseModel):
    id: int
    user_id : int
    status: str
    placed_on: datetime
    total_price: Decimal
    items: List[OrderItemOut]

    class Config:
        from_attributes: True

class OrderItemUpdate(BaseModel):
    items: List[CreateOrderItem]


class OrderStatusUpdate(BaseModel):
    status: models.OrderStatus


class CreateCartItem(BaseModel):
    product_id: int
    quantity: int


class CreateCart(BaseModel):
    items: List[CreateCartItem]

class CartOut(BaseModel):
    id: int
    user_id: int
    created_at : datetime
    updated_at : datetime
    status: str







