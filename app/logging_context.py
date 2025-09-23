import logging
import contextvars

# context variable stores user id per request

user_id_ctx = contextvars.ContextVar("user_id", default="-")

class UserContextFilter(logging.Filter):
    def filter(self, record):
        record.user_id = user_id_ctx.get()
        return 



    