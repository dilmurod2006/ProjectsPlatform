import secrets
from datetime import datetime
import random

# generate token
def generate_token(length=16):
    """Tasodifiy token generatsiya qilish."""
    return secrets.token_urlsafe(length)

# cheack token valid or not
def is_token_valid(expiry_time: datetime):
    """Token muddati tugaganligini tekshirish."""
    return datetime.utcnow() < expiry_time

# random code for login user
