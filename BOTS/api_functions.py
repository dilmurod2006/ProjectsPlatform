import requests


url = "https://api.projectsplatform.uz/iqromindtestusers"

BOT_Secret_key="asaasbnASAJDSABBHJ22131@87899821mnbc$nbsbzhcsczschj908"


# create user api function
def create_user(first_name:str,tg_id:int):
    data = {
        "first_name": first_name,
        "tg_id": tg_id
    }
    r = requests.post(f"{url}/register/{BOT_Secret_key}",data=data)
    return r

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