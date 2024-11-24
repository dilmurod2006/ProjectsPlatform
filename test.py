import requests

from settings import *
# api: http://127.0.0.1:8000/accounts/create_user


# data = {
#     "secret_key": CREATE_USER_SECRET_KEY,
#     "full_name": "b",
#     "sex": True,
#     "email": "b@gmail.com",
#     "username": "b",
#     "password": "b",
#     "ref": 1
# }

# response = requests.post("http://127.0.0.1:8000/accounts/create_user", json=data)

# print(response.json())



# import requests
# from settings import API_ACTIVATION_ACCOUNT_SECRET_KEY

# # api: http://127.0.0.1:8000/accounts/activation_account

# token = "50631b342-5167-414b-95eb-6f0b9183b460"

# data = {
#   "secret_key": API_ACTIVATION_ACCOUNT_SECRET_KEY,
#   "token": token,
#   "tg_id": 5652456552,
#   "phone": "+998912106339"
# }

# response = requests.post("http://127.0.0.1:8000/accounts/activation_account", json=data)

# print(response.json())




# login api test
# import requests

# api : http://127.0.0.1:8000/accounts/login

# data = {
#   "username": "b",
#   "password": "b"
# }

# response = requests.post("http://127.0.0.1:8000/accounts/login", json=data)

# print(response.json())


# cheack login code api
# import requests

# # api : http://127.0.0.1:8000/accounts/check-login-code

# data = {
#   "username": "test1",
#   "password": "test",
#   "code": "857393"
# }

# response = requests.post("http://127.0.0.1:8000/accounts/check-login-code", json=data)

# print(response.json())


# cheack user api
# import requests
# from typing import Dict
# from settings import CHEACK_USER_FOR_BOT
# def check_user(tg_id: int) -> Dict:
#     """Foydalanuvchi ro'yxatdan o'tganligini tekshiradi."""
#     response = requests.get(f"http://127.0.0.1:8000/accounts/check_user?KeySecret={CHEACK_USER_FOR_BOT}&tg_id={tg_id}")
    
#     if response.status_code == 200:
#         return response.json()  # Foydalanuvchi ma'lumotlarini qaytaradi
#     elif response.status_code == 400:
#         raise Exception(response.json().get("detail"))
#     else:
#         raise Exception("Noma'lum xatolik yuz berdi.")

# natija = check_user(5420071824)
# print(natija)


# menga telebot orqali cheack user qilsin yani faqat startni bosganda foydalanuvchi
# api: http://127.0.0.1:8000/accounts/check_user
# shu api ga secret_key va tg_id yuborilsin
# qaytgan ma'lumotlarni foydalanuvchiga yuborsin
# va menga telebot orqali activation account qilib ber:
# https://t.me/projectsplatformbot?start={activation_token} 
# shu linkni bosganda foydalanuvchini activation_token, tg_id va phone raqamini olsin va
# menga buni tekshirish uchun http://127.0.0.1:8000/accounts/activation_account apiga muroat qilsin
# api data: {
#   "secret_key": "string",
#   "token": "string",
#   "tg_id": 0,
#   "phone": "string"
# }

# shunday bo'ladi shunga post sifatida datalarni yubor qaytgan ma'lumotlarni foydalanuvchiga yuborsin





# payment api
# api: http://127.0.0.1:8000/accounts/payment

# admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNvZnR3ZXJlX2VuZ2luZWVyMDA2IiwicGFzc3dvcmQiOiJQcm9qZWN0c1BsYXRmb3JtQWRtaW5ARGlsbXVyb2QxOTQ1JjE5NTciLCJ0Z19pZCI6NTQyMDA3MTgyNCwiZXhwIjoxNzk1NjIzNDQ5fQ.gwI5k8u1pWtiAnv3xr2Uzr7ztV-RfsYQFpXfE46gd5A"

# import requests

# url = "http://127.0.0.1:8000/admin/payment"

# admin_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlNvZnR3ZXJlX2VuZ2luZWVyMDA2IiwicGFzc3dvcmQiOiJQcm9qZWN0c1BsYXRmb3JtQWRtaW5ARGlsbXVyb2QxOTQ1JjE5NTciLCJ0Z19pZCI6NTQyMDA3MTgyNCwiZXhwIjoxNzk1NjIzNDQ5fQ.gwI5k8u1pWtiAnv3xr2Uzr7ztV-RfsYQFpXfE46gd5A"

# # Form ma'lumotlari
# form_data = {
#     "admin_token": admin_token,
#     "tg_id": 5420071824,
#     "tulov_summasi": 100000,
#     "bio": "test"
# }

# # Faylni qo'shish
# files = {
#     "payment_chek_img": open("Logo.jpg", "rb")  # Faylni binar rejimda ochish
# }

# # Form-data va faylni yuborish
# response = requests.post(url, data=form_data, files=files)

# # Javobni tekshirish
# print(response.status_code)
# print(response.json())

