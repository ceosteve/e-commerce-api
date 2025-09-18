
import enum
from .database import Base
from sqlalchemy import Column, Date, DateTime, Enum, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text




class GenderEnum(str,enum.Enum):
    M = "M"
    F = "F"

class UserRole(str, enum.Enum):
    admin = "admin"
    customer="customer"

    
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

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hashed_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("Users", back_populates= "refresh_tokens")
    