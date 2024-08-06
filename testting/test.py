import os
import base64

def generate_secret_key(length=223):
    """
    Maxfiy kalit yaratadi.

    Args:
        length (int): Kalit uzunligi, standart qiymat 32 bayt.

    Returns:
        str: Yaratilgan maxfiy kalit.
    """
    secret_key = base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8')
    return secret_key

def save_secret_key(file_path, key):
    """
    Maxfiy kalitni faylga yozadi.

    Args:
        file_path (str): Fayl manzili.
        key (str): Yoziladigan maxfiy kalit.
    """
    with open(file_path, 'w') as file:
        file.write(key)

if __name__ == "__main__":
    key = generate_secret_key()
    save_secret_key('secret_key.txt', key)
    print("Maxfiy kalit yaratildi va 'secret_key.txt' faylga saqlandi.")
