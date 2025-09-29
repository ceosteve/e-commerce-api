import logging
from venv import logger
from fastapi import APIRouter, Depends, HTTPException, status

from ..authentication import oauth2 
from ..database import get_db
from sqlalchemy.orm import Session
from app import dependencies, schemas, models, utils,dependencies
from ..utils import raise_api_error


logger = logging.getLogger("ecommerce")


router = APIRouter(
    prefix="/users",
    tags= ['users']
)

# create new user account
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user_account(user:schemas.UserCreate, db:Session=Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"user with email {new_user.email} created account")


    return new_user


# retrieve profile details
@router.get("/{id}", response_model=schemas.UserResponse)
def get_profile (id:int, db:Session=Depends(get_db), current_user:int=Depends(dependencies.get_current_user)):

    user=db.query(models.Users).filter(models.Users.id==id).first()

    if not user:
        raise raise_api_error("USER_NOT_FOUND",id=id)
    
    if user.id != current_user.id:
        raise raise_api_error("INVALID_CREDENTIALS")

    return user


# edit user profile
@router.put("/edit/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_profile(id:int, data:schemas.UserUpdate,
                   db:Session=Depends(get_db), 
                   current_user:int=Depends(dependencies.get_current_user)):
    
    query=db.query(models.Users).filter(models.Users.id==id)
    user=query.first()

    if not user:
        raise raise_api_error("USER_NOT_FOUND",id=id)
    
    if current_user.id!= user.id:
        raise raise_api_error("INVALID_CREDENTIALS")
    
    update_data= data.dict()

    if "password" in update_data and update_data['password']:
        update_data['password']=utils.hash_password(update_data['password'])

    query.update(update_data, synchronize_session=False)
    db.commit()

    logger.info(f"user {user.id} updated their data")

    return query.first()



# delete user as admin
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session=Depends(get_db), 
                current_user:models.Users=Depends(dependencies.get_current_user)):
    
    user=db.query(models.Users).filter(models.Users.id==id).first()

    if not user:
        raise raise_api_error("USER_NOT_FOUND", id=id)
    
    logger.warning(f"user {user.id} not found in database")
    
    if current_user.role == models.UserRole.admin:
        db.delete(user)
        db.commit()

    if current_user.role == models.UserRole.customer and current_user.id==id:
        db.delete(user)
        db.commit()
    else:
        raise raise_api_error("FORBIDDEN")

    logger.info(f"user {user.id} deleted from database")

    return {"message":"user deleted from database"}


    

