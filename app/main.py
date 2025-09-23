from starlette.middleware.authentication import AuthenticationMiddleware
import fastapi
from fastapi import APIRouter, FastAPI, Depends, Request

from app import models
from app.routers import auth, orders

from .database import  engine
from .routers import users, products,cart
from app.logging_config import setup_logging
from app.logging_middleware import LoggingMiddleware
from app.logging_context import user_id_ctx


logger = setup_logging()


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
def startup_event():
    logger.info("Application starting up")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Application shutting down")



app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)

@app.get("/")
def root():
    return f"Hello e_commerce"










    
