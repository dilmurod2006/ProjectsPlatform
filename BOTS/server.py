import requests
from utils import restructure_dict
import pickle
from datetime import datetime
from telebot import TeleBot


class ServerConnection:
    def __init__(self):
        self.asosiy_link = "https://api.projectsplatform.uz/iqromindtest"
    def get_about_user(self):
        if self.token != None:
            data = requests.post("https://api.projectsplatform.uz/accounts/about_account", json={"token": self.token}).json()
            self.isLogined = True
        self.isLogined = False
    def post_request(self, next_link, data):
        return requests.post(self.asosiy_link + next_link, json=data).json()

    def get_request(self, next_link):
        print(f"link: {self.asosiy_link + next_link}")
        return requests.get(self.asosiy_link + next_link).json()
    def get_user_data(self):
        return requests.post("https://api.projectsplatform.uz/accounts/about_account", json={"token": self.token}).json()
    def get_price_months(self, months_count: int):
        return self.post_request("/price_months", {"months_count": months_count})
    def get_have_test_months(self):
        return self.post_request("/get_have_test_months", {"token": self.token})
        # return {"202205": 3, "202204": 2, "202603": 1, "202302": 1,  "202412": 1}
    def get_test_datas_in_month(self, month_date):
        return self.post_request("/get_test_datas_in_month", {"token": self.token, "month_date": month_date})
    def get_test(self, month_date, test_key):
        return requests.post(self.asosiy_link + "/get_test", json={"token": self.token, "month_date": month_date, "test_key": test_key}).json()
    def add_test(self, test_name):
        res = self.post_request("/add_test", {"token": self.token, "test_name": test_name})
        if "how" in res and res["how"]:
            self.edit_token = res["test"]["edit_token"]
            self.current_test = res["key"]
            self.current_month = res["test"]["date"][-4:] + res["test"]["date"][-7:-5]
        self.refresh_datas()
        return res
    def set_test(self, month_date, test_key, javoblar):
        return self.post_request("/set_test", {"token": self.token, "month_date": month_date, "test_key": test_key, "javoblar": javoblar})
    def edit_test(self, month_date, test_key, test_name, bio):
        return self.post_request("/edit_test", {"token": self.token, "month_date": month_date, "test_key": test_key, "test_name": test_name, "bio": bio})
    def delete_test(self, month_date, test_key):
        self.current_test = ""
        return self.post_request("/delete_test", {"token": self.token, "month_date": month_date, "test_key": test_key})
    def get_test_kalitlar(self):
        return self.post_request("/get_test_kalitlar", {"token": self.token, "month_date": self.current_month, "test_key": self.current_test})
    def get_test_tekshirishlar(self):
        return self.post_request("/get_test_tekshirishlar", {"token": self.token, "month_date": self.current_month, "test_key": self.current_test})
    def get_test_edit_token(self, edit_token, month_date, test_key):
        return self.post_request("/get_test_edit_token", {"edit_token": edit_token,"user_id": self.user_id, "month_date": month_date, "test_key": test_key})
    def set_test_edit_token(self, edit_token, month_date, test_key, kalitlar):
        return self.post_request("/set_test_edit_token", {"edit_token": edit_token,"user_id": self.user_id, "month_date": month_date, "test_key": test_key, "kalitlar": kalitlar})
    def set_edu_name(self, edu_name, edu_slogan):
        return self.post_request("/set_edu_name", {"token": self.token, "edu_name": edu_name, "edu_slogan": edu_slogan})
    def get_edu_name(self):
        return self.get_request(f"/get_edu_name/{self.user_id}")
    def set_edu_bot_token(self, edu_bot_token):
        return self.post_request("/set_edu_bot_token", {"token": self.token, "edu_bot_token": edu_bot_token})
    def get_edu_bot_token(self):
        return self.post_request("/get_edu_bot_token", {"token": self.token})
    def get_edu_logo(self, user_id):
        return self.get_request(f"/get_edu_logo/{user_id}")
    def set_edu_logo(self, file_id):
        return self.post_request("/set_edu_logo", {"token": self.token, "edu_logo": file_id})
    def add_natija(self, id_raqam, maj, b1, b2, file_id, ser1, ser2, f1, f2, lang_id):
        return self.post_request("/add_natija", {
            "token": self.token,
            "month_date": self.current_month,
            "test_key": self.current_test,
            "id_raqam": id_raqam,
            "maj": maj,
            "b1": b1,
            "b2": b2,
            "file_id": file_id,
            "ser1": ser1,
            "ser2": ser2,
            "f1": f1,
            "f2": f2,
            "lang": lang_id
        })
    def delete_natija(self, id_raqam):
        return self.post_request("/delete_natija", {
            "token": self.token,
            "month_date": self.current_month,
            "test_key": self.current_test,
            "id_raqam": id_raqam
        })
    def get_natija(self, month_date, test_key, id_raqam):
        return self.post_request("/get_natija", {"user_id": self.user_id, "month_date": month_date, "test_key": test_key, "id_raqam": id_raqam})
    def get_natija_file(self, file_id):
        return self.post_request("/get_natija_file", {"user_id": self.user_id,"file_id": file_id})
    def logout(self):
        self.token = None
        self.isLogined = False
        self.refresh_db()
        self.__init__()
    def check_premium(self):
        res = self.post_request("/check_pc", {
            "token": self.token,
            "device_id": get_device_id()
        })
        if "how" in res:
            self.end_premium_date = res["end_premium_date"]
            self.size = res["size"] if res["size"] > 0 else 0
            return res["size"] > 0
        return False
    def set_kalit(self, key, x):
        if x in " ABCD":
            if x == self.edits[self.current_fan*30+key]:
                self.edits = self.edits[:self.current_fan*30+key] + " " + self.edits[self.current_fan*30+key+1:]
            elif x != self.kalitlar[self.current_fan*30+key]:
                self.edits = self.edits[:self.current_fan*30+key] + x + self.edits[self.current_fan*30+key+1:]
            if self.edits[self.current_fan*30+key] != " ":
                return True
            elif self.kalitlar[self.current_fan*30+key] != " ":
                return None
            else:
                return False
            
        return None
    def save_kalitlar(self):
        res = self.get_test(self.current_month, self.current_test)
        self.edit_token = res.get("edit_token")
        value = self.edits[self.current_fan*30:(self.current_fan+1)*30]
        for i in range(30):
            if value[i] == " ":
                value = value[:i] + self.kalitlar[self.current_fan*30+i] + value[i+1:]
            else:
                self.kalitlar = self.kalitlar[:self.current_fan*30+i] + value[i] + self.kalitlar[self.current_fan*30+i+1:]
            self.edits = self.edits[:self.current_fan*30+i] + " " + self.edits[self.current_fan*30+i+1:]
        return self.set_test_edit_token(self.edit_token[:4]+str(self.current_fan)+self.edit_token[-4:], self.current_month, self.current_test, value)
    def download_bytes(self, file_id):
        # Telegram botdan self.bot orqali yuklab olib keyin bytes formatida qaytarish
        file_info = self.bot.get_file(file_id)  # Fayl haqidagi ma'lumotni olish
        file_bytes = self.bot.download_file(file_info.file_path)  # Faylni yuklash
        return file_bytes
    def download_and_save(self, file_id):
        # Telegram botdan self.bot orqali yuklab olib keyin bytes formatida qaytarish
        file_info = self.bot.get_file(file_id)  # Fayl haqidagi ma'lumotni olish
        file_bytes = self.bot.download_file(file_info.file_path)  # Faylni yuklash
        # Faylni vaqtinchalik saqlab uni path ni qaytarish
        with open("tmp/image.png", "wb") as f:
            f.write(file_bytes)
        return "tmp/image.png"
    def get_post_text(self):
        return self.get_request(f"/get_post_text/{self.user_id}/{self.current_month}/{self.current_test}")
    def get_post_format_text(self):
        return self.get_request(f"/get_post_format_text/{self.user_id}/{self.current_month}/{self.current_test}")
    def get_post_text_html(self):
        return self.get_request(f"/get_post_text_html/{self.user_id}/{self.current_month}/{self.current_test}")
    def set_post_text(self, format_text):
        return self.post_request(f"/set_post_text", {
            "token": self.token,
            "month_date": self.current_month,
            "test_key": self.current_test,
            "post_text": format_text
        })
    def get_post_text_html(self, user_id, month_date, test_key):
        return self.get_request(f"/get_post_text_html/{user_id}/{month_date}/{test_key}")
    
    def change_password(self, old_password: str, new_password: str):
        return requests.post(f"https://api.projectsplatform.uz/accounts/change-password-request?token={self.token}", json={
            "last_password": old_password,
            "new_password": new_password
        }).json()
    def reset_password_request(self, username: str):
        return requests.post(f"https://api.projectsplatform.uz/accounts/reset-password-request", json={
            "username": username,
        }).json()
    def reset_password(self, username: str, new_password: str, reset_code: int):
        return requests.post(f"https://api.projectsplatform.uz/accounts/reset-password", json={
            "username": username,
            "password": new_password,
            "reset_code": reset_code
        }).json()

class ServerTestBot:
    def __init__(self):
        self.asosiy_link = "https://api.projectsplatform.uz/iqromindtestusers"
        self.secret_key = "asaasbnASAJDSABBHJ22131@87899821mnbc$nbsbzhcsczschj908"
    def post_request(self, next_link, data):
        return requests.post(self.asosiy_link + next_link, json=data).json()
    def get_request(self, next_link):
        return requests.get(self.asosiy_link + next_link).json()
    def register(self, first_name, tg_id):
        return self.post_request(f"/register/{self.secret_key}", {"first_name": first_name, "tg_id": tg_id})
    def check_user(self, tg_id):
        return self.get_request(f"/check-user/{tg_id}?bot_secret_key={self.secret_key}")
