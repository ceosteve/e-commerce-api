
from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils, oauth2

router = APIRouter(
    tags= ['login']

)


@router.post("/login", response_model=schemas.TokenOut)
def login(user_credentials:OAuth2PasswordRequestForm= Depends(), db:Session=Depends(get_db)):
    
    query=db.query(models.Users).filter(models.Users.email==user_credentials.username)
    user = query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = oauth2.create_access_token({"user_id":user.id})
    refresh_raw = utils.make_refresh_record(db, user_id=user.id)

    return {"access_token":access_token, "token_type":"bearer", "refresh_token":refresh_raw}



@router.post("/token/refresh", response_model=schemas.TokenOut)
def refresh_token(request:schemas.RefreshRequest, db:Session=Depends(get_db)):

    raw_refresh_token=request.refresh_token
    hashed_token = utils.hash_token(raw_refresh_token)

    db_token = db.query(models.RefreshToken).filter(models.RefreshToken.hashed_token==hashed_token
                                                    ).filter(models.RefreshToken.expires_at > datetime.utcnow()).first()
    
    if not db_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    
    #rotate refresh token
    user_id = db_token.user_id
    db.delete(db_token)
    db.commit()

    new_raw_refresh_token = utils.make_refresh_record(db,user_id=user_id, days=7)

    new_access_token = oauth2.create_access_token({"user_id": user_id})

    return {"acess_token":new_access_token, "token_type":"bearer", "refresh_token":new_raw_refresh_token}


