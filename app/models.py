
from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql.expression import text



# users sqlalchemy model
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable = False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    @property 
    def full_name(self):
        return f"{self.fist_name} {self.last_name}"
    