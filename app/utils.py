

from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.config import settings

from .errors import ERRORS

pswd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



#  password hashing and verification
def hash_password(password:str) -> str:
    return pswd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pswd_context.verify(plain_password, hashed_password)



# token hashing and verification
def hash_token(token:str)-> str:
    return pswd_context.hash(token)

def verify_token(token:str, hashed_token:str) -> bool:
    return pswd_context.verify(token, hashed_token)


# create consistent format of exceptions
def raise_api_error(error_code:str, **kwargs):
    error=ERRORS.get(error_code)

    if not error:
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error":{
                    "code":"INTERNAL_SERVER_ERROR",
                    "message":f"unkown error code : {error_code}"
                }
            }
        )
    
    message = error["message"].format(**kwargs) if kwargs else error["message"]

    raise HTTPException(
        status_code=error["status_code"],
        detail={
            "error":{
                "code":error_code,
                "message":message
            }
        }
    )
