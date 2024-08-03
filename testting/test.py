import re

def is_valid_uzbek_phone_number(phone_number):
    """O'zbek telefon raqamini tekshiradi."""
    # Telefon raqam uchun regex pattern
    pattern = r'^\+998[1-9][0-9]{8}$'
    
    # Telefon raqamni tekshirish
    if re.match(pattern, phone_number):
        return True
    return False

phone_number = "+998906754406"
print(len(phone_number))
if is_valid_uzbek_phone_number(phone_number):
    print(f"{phone_number} - To'g'ri raqam")
else:
    print(f"{phone_number} - Noto'g'ri raqam")



