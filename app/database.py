from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker



Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://postgres:postgres254@localhost:5432/ecommerce"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)




def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()