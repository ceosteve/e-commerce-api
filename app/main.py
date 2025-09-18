
import fastapi
from fastapi import APIRouter, FastAPI, Depends

from app import models
from app.routers import auth

from .database import Base, engine
from .routers import users


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return f"Hello e_commerce"










    
