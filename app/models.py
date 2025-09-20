
import enum

from .database import Base
from sqlalchemy import DATETIME, Column, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, TIMESTAMP, func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text




class GenderEnum(str,enum.Enum):
    M = "M"
    F = "F"

class UserRole(str, enum.Enum):
    admin = "admin"
    customer="customer"

class OrderStatus(str,enum.Enum):
    pending="pending"
    paid="paid"
    shipped ="shipped"
    cancelled= "cancelled"

# users sqlalchemy model
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable = False)
    email = Column(String, nullable=False, unique=True)
    gender = Column(Enum(GenderEnum), nullable=False)
    birth_date= Column(Date,nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(UserRole), server_default=UserRole.customer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    


    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")
    orders = relationship("Order", back_populates="user")


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hashed_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates= "refresh_tokens")


class Products(Base):
    __tablename__="products"
    id=Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description =Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Numeric(8,2), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    order_items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__="orders"
    id = Column(Integer,primary_key=True, index=True) 
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    placed_on = Column(DateTime, server_default=func.now(), nullable=False)
    total_price = Column(Numeric(10,2), nullable=False)
    status = Column(Enum(OrderStatus), default= OrderStatus.pending, nullable=False)
    
    user = relationship("Users", back_populates="orders")
    items = relationship("OrderItem",back_populates="order")

    def recalc_total(self):
        self.total_price = sum(item.item_quantity * item.unit_price for item in self.items)
        


class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"),nullable=False)
    item_quantity = Column(Integer,nullable=False)
    unit_price = Column(Numeric(10,2), nullable=False)

    order = relationship("Order",back_populates="items")
    product= relationship("Products", back_populates="order_items")