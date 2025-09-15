
from pydantic import BaseModel, EmailStr



# create users schema
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
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