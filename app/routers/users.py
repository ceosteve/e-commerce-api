
from fastapi import APIRouter, Depends, HTTPException, status

from ..authentication import oauth2 
from ..database import get_db
from sqlalchemy.orm import Session
from app import dependencies, schemas, models, utils,dependencies



router = APIRouter(
    prefix="/users",
    tags= ['users']
)

# create new user account
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user_account(user:schemas.UserCreate, db:Session=Depends(get_db)):

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# retrieve profile details
@router.get("/{id}", response_model=schemas.UserResponse)
def get_profile (id:int, db:Session=Depends(get_db), current_user:int=Depends(dependencies.get_current_user)):

    user=db.query(models.Users).filter(models.Users.id==id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"user with id {id} not found")
    
    if user.id != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials")

    return user


# edit user profile
@router.put("/edit/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def update_profile(id:int, data:schemas.UserUpdate,
                   db:Session=Depends(get_db), 
                   current_user:int=Depends(dependencies.get_current_user)):
    
    query=db.query(models.Users).filter(models.Users.id==id)
    user=query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id{id} not found")
    
    if current_user.id!= user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
    
    update_data= data.dict()

    if "password" in update_data and update_data['password']:
        update_data['password']=utils.hash_password(update_data['password'])

    query.update(update_data, synchronize_session=False)
    db.commit()

    return query.first()



# delete user as admin
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int, db:Session=Depends(get_db), 
                current_user:models.Users=Depends(dependencies.get_current_user)):
    
    user=db.query(models.Users).filter(models.Users.id==id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with id{id} not found")
    
    if current_user.role == models.UserRole.admin:
        db.delete(user)
        db.commit()

    if current_user.role == models.UserRole.customer and current_user.id==id:
        db.delete(user)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cannot delete this account")

    return {"message":"user deleted from database"}


    

