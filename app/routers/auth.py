
from jose import jwt
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, utils

router = APIRouter(
    tags= ['login']

)

@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    
    query=db.query(models.Users).filter(models.Users.email==user_credentials.username)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = jwt.encode("data":"users_id")

    return {"access_token":access_token, "token_type":"bearer"}

    
    

