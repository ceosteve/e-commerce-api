from contextlib import asynccontextmanager
from starlette.middleware.authentication import AuthenticationMiddleware
import fastapi
from fastapi import APIRouter, FastAPI, Depends, Request, Response

from app import models
from app.routers import auth, orders

from .database import  engine
from .routers import users, products, cart
from app.logging_config import setup_logging
from app.logging_middleware import LoggingMiddleware
from app.logging_context import user_id_ctx
from fastapi.middleware.cors import CORSMiddleware

logger = setup_logging()


models.Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app:FastAPI):
    logger.info("Application starting up")
    yield
    
    logger.info("Application shutting down")

app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggingMiddleware)

origins = ['http://localhost:8000']

"""restrict which domains can make api calls and the requests they can send"""
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers = ["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(cart.router)

@app.get("/")
def root():
    return f"Hello e_commerce"










    
