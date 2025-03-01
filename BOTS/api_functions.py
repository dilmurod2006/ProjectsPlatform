import requests


url = "https://api.projectsplatform.uz/iqromindtestusers"

BOT_Secret_key="asaasbnASAJDSABBHJ22131@87899821mnbc$nbsbzhcsczschj908"



def check_user(tg_id: int) -> dict:
    """Foydalanuvchi ro‘yxatdan o‘tganligini tekshiradi."""
    try:
      r = requests.get(f"{url}/check-user/{tg_id}", params={"bot_secret_key": BOT_Secret_key})  # params to‘g‘ri

      if r.status_code == 200:
          return r.json() # To‘g‘ri kalit nomi
      else:
          return False  # Xato bo‘lsa, False qaytarish
    except:
        pass

# create user api functionsssss
def create_user(first_name: str, tg_id: int):
    data = {
        "first_name": first_name,
        "tg_id": tg_id
    }
    r = requests.post(f"{url}/register/{BOT_Secret_key}", json=data)  # json=data bo'lishi kerak
    return r.json()["user_id"]  # .json() orqali dictionary olish kerak


# add test api function
def add_test(user_id:str,titul_id:str,qiymat:str,sana:str):
    data = {
  "user_id": user_id,
  "titul_id": titul_id,
  "qiymat": [
    qiymat
  ],
  "sana": sana
    }
    r = requests.post(f"{url}/addtest/{user_id}",data=data)
    return r


# get tests for user
def get_tests(user_id:str):
    r = requests.get(f"{url}/tests/{user_id}")
    return r