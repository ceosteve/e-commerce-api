
from pyexpat import model
from fastapi import APIRouter, Response, status, Depends
from datetime import datetime
import logging 

from ..utils import raise_api_error
from app import dependencies
from app.database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session


logger = logging.getLogger("ecommerce")


router = APIRouter(
    prefix="/cart",
    tags=['cart']
)


#  adding new item to the cart 
@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.CartOut)
def add_to_cart(order_items:schemas.CreateCart, 
                db:Session=Depends(get_db),
                current_user:int=Depends(dependencies.get_current_user)):

    active_cart=db.query(models.Cart).filter(models.Cart.user_id==current_user.id, models.Cart.status=="active").first()
    
    if not active_cart:
        active_cart = models.Cart(
            user_id = current_user.id, 
            created_at = datetime.utcnow(),
            status = "active"
            )

        db.add(active_cart)
        db.flush()
    
  
    for item in order_items.items:

            product_exists= db.query(models.Products).filter(models.Products.id==item.product_id).first()

            if not product_exists:
                raise raise_api_error("PRODUCT_NOT_FOUND", id=item.product_id)

            if product_exists.stock<item.item_quantity:
                raise raise_api_error("INSUFFICIENT_STOCK")
            
            
            cart_item=db.query(models.CartItem).filter(models.CartItem.cart_id==active_cart.id,
                                             models.CartItem.product_id==item.product_id).first()
            
            if cart_item:
                 cart_item.item_quantity = cart_item.item_quantity+ item.item_quantity
                 cart_item.unit_price = product_exists.price

            else:
                new_cart_item = models.CartItem(
                    cart_id = active_cart.id,
                    product_id = item.product_id,
                    item_quantity = item.item_quantity,
                    unit_price = product_exists.price
                    )
                
                db.add(new_cart_item)

    active_cart.updated_at=datetime.utcnow()       
    db.commit()
    db.refresh(active_cart)
    
    logger.info(f"user {current_user.id} created new cart with {active_cart.id}")
    
    return active_cart


# get cart from database
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model = schemas.CartOut)
def get_cart(id:int, db:Session=Depends(get_db), current_user:int=Depends(dependencies.get_current_user)):
    cart=db.query(models.Cart).filter(models.Cart.id==id).first()

    if not cart:
        raise raise_api_error("CART_NOT_FOUND")
    if cart.user_id != current_user.id:
        raise raise_api_error("FORBIDDEN")
    return cart



# cart items checkout
@router.post("/checkout", status_code=status.HTTP_200_OK, response_model=schemas.OrderOut)
def checkout (db:Session=Depends(get_db),
               current_user:int=Depends(dependencies.get_current_user)):
    
    active_cart=db.query(models.Cart).filter(
         models.Cart.user_id==current_user.id, 
         models.Cart.status=="active").first()
    

    if not active_cart or not active_cart.items:
         raise raise_api_error("CART_EMPTY")
    

    new_order = models.Order(
            user_id=current_user.id,
            placed_on= datetime.utcnow(),
            status="pending",
            total_price=0
            ) 
    db.add(new_order)
    db.flush()   # get order id

    total_price = 0  

    for item in active_cart.items:

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

            total_price += product_exists.price * item.item_quantity

    active_cart.status = "checked_out"
    active_cart.updated_at = datetime.utcnow()

            
    db.commit()
    db.refresh(new_order)
    
    logger.info(f"user {current_user.id} checked out {active_cart.id}")
    
    return new_order
           



# update order items in cart
@router.put("/update/{id}/items", status_code=status.HTTP_200_OK, response_model=schemas.CartOut)
def update_order_item(id:int, update_data:schemas.OrderItemUpdate, db:Session=Depends(get_db), 
                      current_user:int=Depends(dependencies.get_current_user)):

    query=db.query(models.Cart).filter(models.Cart.id==id)
    cart = query.first()

    if not cart:
        raise raise_api_error("CART_NOT_FOUND", id=id)
    
     
    if cart.status == models.CartStatus.checked_out:
        logger.warning(f"user with {current_user.id} tried changing a checked out cart with id {cart.id}")
        raise raise_api_error("ALREADY_CHECKED_OUT")

    for item in update_data.items:
         product = db.query(models.Products).filter(models.Products.id==item.product_id).first()
         if not product:
             raise raise_api_error("PRODUCT_NOT_FOUND", id=item.product_id)
         

         cart_item = db.query(models.CartItem).filter(models.CartItem.cart_id==cart.id,
                                                      models.CartItem.product_id==item.product_id).first()

         if not cart_item:
             raise raise_api_error("PRODUCT_NOT_FOUND", id=item.product_id)
        
         if product.stock < item.item_quantity:
             raise raise_api_error("INSUFFICIENT STOCK")
         
        
         product.stock -= (item.item_quantity-cart_item.item_quantity)
         cart_item.item_quantity = item.item_quantity
         cart_item.unit_price = product.price


    db.commit()
    db.refresh(cart)
    
    logger.info(f"user {current_user.id} updated cart {cart.id}")
    return cart



# delete entire cart 
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id:int, db:Session=Depends(get_db),current_user:int=Depends(dependencies.get_current_user)):
     
    cart=db.query(models.Cart).filter(models.Cart.id==id).first()

    if not cart:
         raise raise_api_error("CART_NOT_FOUND", id=id)

    if cart.status == models.CartStatus.checked_out:
         raise raise_api_error("ALREADY_CHECKED_OUT")
    
    db.delete(cart)
    db.commit()
    
    
    logger.info(f"user {current_user.id} deleted cart {cart.id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# delete one item from cart
@router.delete("/delete/cart/{cart_id}/product/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_from_cart(cart_id:int, item_id:int, db:Session=Depends(get_db), 
                             current_user:int=Depends(dependencies.get_current_user)):
    
    cart_item = db.query(models.CartItem).join(models.Cart).filter(
         models.CartItem.product_id==item_id,
         models.Cart.id==cart_id,
         models.Cart.user_id==current_user.id).first()

    if not cart_item:
         raise raise_api_error("PRODUCT_NOT_FOUND")
    
    db.delete(cart_item)
    db.commit()
    
    
    logger.info(f"user {current_user.id} deleted cart item {cart_item.id}")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
