
from passlib.context import CryptContext

from app import schemas

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    return pswd_context.hash(password)

def verify(plain_password, hashed_password):
    return pswd_context.verify(plain_password, hashed_password)

