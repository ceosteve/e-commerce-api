
from datetime import datetime, timedelta
import secrets
from fastapi import Depends
from passlib.context import CryptContext
from app.config import settings

from app import config, models, schemas

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password:str) -> str:
    return pswd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pswd_context.verify(plain_password, hashed_password)


# generates a high entropy random token and sends it back to the client
def generate_raw_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_token(token:str)-> str:
    return pswd_context.hash(token)

def verify_token(token:str, hashed_token:str) -> bool:
    return pswd_context.verify(token, hashed_token)


# creating new record of refresh token in the database by calling the generate_raw_refresh_token function
def make_refresh_record(db, user_id:int, days: int=settings.refresh_token_expiration_days):
    raw = generate_raw_refresh_token()
    hashed = hash_token(raw)
    expires= datetime.utcnow()+ timedelta(days=days)
    db_token = models.RefreshToken(user_id=user_id, hashed_token=hashed, expires_at=expires)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return raw
