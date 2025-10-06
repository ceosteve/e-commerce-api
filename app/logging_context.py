import logging
from contextvars import ContextVar


# context variable stores user id per request



user_id_ctx = ContextVar("user_id", default="-")

class UserContextFilter(logging.Filter):
    def filter(self, record):
        try:
            user_id = user_id_ctx.get()
        except Exception as e:
            user_id = "-"
        setattr(record, "user_id", user_id or "-")
        return True