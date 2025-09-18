from fastapi import Depends, HTTPException, status
from .authentication.oauth2 import oauth2_scheme, verify_access_token
from .database import get_db
from sqlalchemy.orm import Session
from app import models

def get_current_user(token: str=Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                           detail="Could not verify credentials", 
                                          headers={"WWW-Authenticate":"Bearer"})

    token_data = verify_access_token(token, credentials_exception)

    user= db.query(models.Users).filter(models.Users.id==token_data.id).first()
    if not user:
        raise credentials_exception
    return user


def require_admin(current_user:models.Users= Depends(get_current_user)):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized to perform operation")
    
    return current_user