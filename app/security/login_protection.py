from fastapi import Request
from datetime import date, datetime, timedelta
from collections import defaultdict
from ..logging_config import logging

logger = logging.getLogger("ecommerce")
# ensuring that the login endpoint is protected from Brute force attacks

failed_attempts= defaultdict(list)
BLOCK_TIME_MINUTES = 5


def record_failed_attempts(ip:str):
    failed_attempts[ip].append(datetime.utcnow())


def is_captcha_required(ip:str):
    failed_attempts[ip] = [
        t for t in failed_attempts[ip]
        if t > datetime.utcnow()- timedelta(BLOCK_TIME_MINUTES)
    ]
    if len(failed_attempts[ip])>=3:
        logger.warning(f"CAPTCHA triggered for IP {ip} due to repeated failed login attempts.")
        return True
    return False

def reset_attempts(ip:str):
    failed_attempts[ip].clear()


