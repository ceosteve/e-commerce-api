from datetime import datetime, timedelta
import secrets
from fastapi import Depends
from app import models
from ..utils import hash_token
from app.config import settings



# generates a high entropy random token and sends it back to the client
def generate_raw_refresh_token() -> str:
    return secrets.token_urlsafe(64)



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
