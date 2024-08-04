import random
import string


# generate token for forregister
def generate_token_for_forregister(length=32):
    """32 ta simvoldan iborat tokenni yaratadi."""
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token

# generate token for users
def generate_token_for_users(length=64):
    """64 ta simvoldan iborat tokenni yaratadi."""
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token