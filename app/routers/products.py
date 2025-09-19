
from itertools import product
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas, models, dependencies
from app.database import get_db
from app.utils import raise_api_error


router = APIRouter(
    prefix="/products",
    tags=['products']
)


# create product in the system
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=List[schemas.ProductOut])
def create_product(products:List[schemas.ProductCreate], db:Session=Depends(get_db), 
                   current_user:models.Users=Depends(dependencies.require_admin)):
    
    new_products=[models.Products(**product.dict()) for product in products ]
    db.add_all(new_products)
    db.commit()

    for product in new_products:
        db.refresh(product)

    return new_products


# get all products from database
@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.ProductOut])
def get_products(db:Session=Depends(get_db),
                  skip:int= Query(0,ge=0),
                  limit:int=Query(10, ge=1),
                  search:Optional[str]=Query(None)):
    
    query=db.query(models.Products)

    if search:
        query=query.filter(models.Products.name.contains(search))
    
    products= query.offset(skip).limit(limit).all()

    return products


# update product information
@router.put("/{id}",status_code=status.HTTP_200_OK, response_model=schemas.ProductOut)
def update_product(id:int, update_info:schemas.ProductUpdate, 
                   db:Session=Depends(get_db), 
                   current_user:models.Users=Depends(dependencies.require_admin)):

    query=db.query(models.Products).filter(models.Products.id==id)
    product=query.first()

    if not product:
        raise raise_api_error("PRODUCT_NOT_FOUND", id=id)
 
    updated_product=update_info.dict(exclude_unset=True)

    query.update(updated_product, synchronize_session=False)
    db.commit()
    db.refresh(product)

    return product



# delete product from database
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int, db:Session=Depends(get_db),
                    current_user:models.Users=Depends(dependencies.require_admin)):

    product=db.query(models.Products).filter(models.Products.id==id).first()

    if not product:
        raise raise_api_error("PRODUCT_NOT_FOUND", id=id)
    
    db.delete(product)
    db.commit()

    return




    

