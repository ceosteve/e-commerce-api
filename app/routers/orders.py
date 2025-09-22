
from logging import info
from math import prod
from fastapi import APIRouter, status, Depends

from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.utils import raise_api_error
from .. import models, schemas
from .. import dependencies
from datetime import datetime


router = APIRouter(
    prefix="/orders",
    tags=['orders']
)



# user to create an order
@router.post("/create/",status_code=status.HTTP_201_CREATED, response_model=schemas.OrderOut)
def create_order(order:schemas.CreateOrder, 
                 db:Session=Depends(get_db), 
                 current_user:int=Depends(dependencies.get_current_user)):
    try:
        new_order = models.Order(
            user_id=current_user.id,
            placed_on= datetime.utcnow(),
            status="pending",
            total_price=0
        )

        db.add(new_order)
        db.flush()

        total_price = 0
        order_items = []

        for item in order.items:

            product_exists= db.query(models.Products).filter(models.Products.id==item.product_id).first()

            if not product_exists:
                raise raise_api_error("PRODUCT_NOT_FOUND", id=item.product_id)

            if product_exists.stock<item.item_quantity:
                raise raise_api_error("INSUFFICIENT_STOCK")
        
            product_exists.stock -= item.item_quantity

            new_order_item = models.OrderItem(
                order_id=new_order.id,
                product_id = item.product_id,
                item_quantity = item.item_quantity,
                unit_price = product_exists.price

            )

            db.add(new_order_item)
            order_items.append(new_order_item)


            total_price+=new_order_item.unit_price*item.item_quantity

        new_order.total_price=total_price
        db.commit()
        db.refresh(new_order)

        return{
            "order_id": new_order.id,
            "user_id": new_order.user_id,
            "status": new_order.status,
            "placed_on": new_order.placed_on,
            "total_price": new_order.total_price,
            "items": order_items
        }

    except Exception as e:
        db.rollback()
        raise e



# view orders
@router.get("/",status_code=status.HTTP_200_OK, response_model=List[schemas.OrderOut])
def get_orders(db:Session=Depends(get_db), current_user:int=Depends(dependencies.get_current_user)):

    orders=db.query(models.Order).filter(models.Order.user_id==current_user.id).all()

    if not orders:
        raise raise_api_error("ORDER_NOT_FOUND")
    
    return orders


# update order items
@router.put("/update/{id}/items", status_code=status.HTTP_200_OK, response_description=schemas.OrderOut)
def update_order_item(id:int, update_data:schemas.OrderItemUpdate, db:Session=Depends(get_db), 
                      current_user:int=Depends(dependencies.get_current_user)):

    query=db.query(models.Order).filter(models.Order.id==id)
    order = query.first()

    if not order:
        raise raise_api_error("ORDER_ID_NOT_FOUND", id=id)
    
     
    if order.status != models.OrderStatus.pending:
        raise raise_api_error("ORDER_ALREADY_FINALIZED")


    for item in update_data.items:
         product = db.query(models.Products).filter(models.Products.id==item.product_id).first()
         if not product:
             raise raise_api_error("PRODUCT_NOT_FOUND", id=item.product_id)
         

         order_item = db.query(models.OrderItem).filter(models.OrderItem.order_id==order.id).first()
         if not order_item:
             raise raise_api_error("ORDER_ID_NOT_FOUND", id=item.product_id)
        
         if product.stock < item.item_quantity:
             raise raise_api_error("INSUFFICIENT STOCK")
         
        
         product.stock -= (item.item_quantity- order_item.item_quantity)
         order_item.item_quantity = item.item_quantity
         order_item.unit_price = product.price
    
    order.recalc_total()

    db.add(order)
    db.commit()
    db.refresh(order)

    return order


#  update order status
@router.put("/update/{id}/status", status_code=status.HTTP_200_OK, response_model=schemas.OrderOut)
def update_order_status(id:int, update_data:schemas.OrderStatusUpdate, 
                        db:Session=Depends(get_db),
                        current_user:models.UserRole=Depends(dependencies.require_admin)):


    query=db.query(models.Order).filter(models.Order.id==id)
    order = query.first()

    if not order:
        raise raise_api_error("ORDER_ID_NOT_FOUND", id=id)
    
    
    order.status = update_data.status


    db.commit()
    db.refresh(order)

    return order







    
    