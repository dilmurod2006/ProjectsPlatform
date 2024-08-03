import random
import string



def generate_token_for_orregister(length=32):
    """32 ta simvoldan iborat tokenni yaratadi."""
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(length))
    return token