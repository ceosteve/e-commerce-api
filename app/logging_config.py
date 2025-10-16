import logging
from logging.config import dictConfig
from app.logging_context import UserContextFilter



# logging configurations in form of a dict so that its re usable
def setup_logging():
    logging_config = {
        "version":1,
        "disable_existing_loggers":False,
        "formatters":{
            "default":{
                "format":"[%(asctime)s] [user=%(user_id)s] %(levelname)s in %(module)s:%(message)s"
            },
            "detailed":{
                "format": "[%(asctime)s] [user=%(user_id)s] %(levelname)s [%(name)s:%(lineno)d] %(message)s"
            },
        },
        "filters":{
            "user_context":{
                "()":UserContextFilter,
            },
        },
        # where log mesaages go
        # prints log info to the terminal
        "handlers":{
            "console":{
                "class":"logging.StreamHandler",
                "formatter":"default",
                "filters":["user_context"]
            },
        
        # writes log messages into a file
            "file":{
                "class":"logging.handlers.RotatingFileHandler",
                "formatter":"detailed",
                "filename":"logs/app.log",
                "encoding":"utf-8",
                "maxBytes": 1048576,
                "backupCount": 7,    # will keep logs for 7 days
            },
        },
        "root":{
            "level":"DEBUG",
            "handlers":["console","file"],
        },
    }
   
    dictConfig(logging_config)
    return logging.getLogger("ecommerce")


