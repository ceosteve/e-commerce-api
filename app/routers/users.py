

from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from sqlalchemy.orm import Session
from app import schemas, models, utils



router = APIRouter(
    tags= ['users']
)

# create new user account
@router.post("/users/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user_account(user:schemas.UserCreate, db:Session=Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_profile (id:int, db:Session=Depends(get_db)):

    user=db.query(models.Users).filter(models.Users.id==id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
    return user

