from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from slowapi.middleware import SlowAPIMiddleware

# get the ip address of the client
limiter = Limiter(key_func=get_remote_address)


# custom exception handler
def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail":"Too many requests. Please try again later"},
    )

# attach the middleware and handler to the app
def setup_rate_limiter(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

