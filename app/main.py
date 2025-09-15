
import fastapi
from fastapi import APIRouter, FastAPI, Depends

from app import models

from .database import Base, engine
from .routers import users


models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(users.router)

@app.get("/")
def root():
    return f"Hello e_commerce"










    
