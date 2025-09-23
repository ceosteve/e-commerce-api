

from starlette.middleware.base import BaseHTTPMiddleware
from app.logging_context import user_id_ctx
from fastapi import Request
from jose import jwt, JWTError
from app.config import settings



SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm


# define a logging middleware in form of a python class 

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request:Request, call_next):
        user_id_ctx.set("-")

        # extract jwt token from authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

            try:
                pay_load = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = pay_load.get("user_id")
                if user_id:
                    user_id_ctx.set(user_id)
            except JWTError:
                pass
        
        # proceed to process the request

        response = await call_next(request)

        # reset context to avoid leaking user_id across requests

        user_id_ctx.set("-")
        return response

