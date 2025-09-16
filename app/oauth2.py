from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from app import models, schemas
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db
from sqlalchemy.orm import Session




oauth2_scheme= OAuth2PasswordBearer("login")

SECRET_KEY = "f3c9c55e7f844a9f92a3b0f91a7b1d4a87f134dba23f68c92de51e82a45c7c9a"
ALGORITHM = "HS256"
EXPIRATION_TIME = 60

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload=jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                           detail="Could not verify credentials", 
                                          headers={"WWW-Authenticate":"Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user= db.query(models.Users).filter(models.Users.id==token_data.id).first()
    if not user:
        raise credentials_exception
    return user

