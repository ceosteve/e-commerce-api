

from passlib.context import CryptContext
from app.config import settings

from app import config, models, schemas

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pswd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pswd_context.verify(plain_password, hashed_password)



def hash_token(token:str)-> str:
    return pswd_context.hash(token)

def verify_token(token:str, hashed_token:str) -> bool:
    return pswd_context.verify(token, hashed_token)

