from pydantic import BaseModel

class BuySerializer(BaseModel):
    token: str
    months_count: int
class PriceSerializer(BaseModel):
    months_count: int
class CheckPcSerializer(BaseModel):
    device_id: str
    token: str


# Testlarni o'qish uchun serializer
class GetHaveTestMonthsSerializer(BaseModel):
    token: str


# 1 oylik testlarni qaytaruvchi serializer
class GetTestDatasInMonthSerializer(BaseModel):
    token: str
    month_date: str


# Testni o'qish
class GetTestSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str

# Delete test
class DeleteTestSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str


# Testni qo'shish uchun
class AddTestSerializer(BaseModel):
    token: str
    test_name: str

# Testni taxrirlash uchun
class SetTestSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str
    javoblar: str

class EditTestSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str
    test_name: str
    bio: str

# Tekshirishlarni olish
class GetTestTekshirishlarSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str

# Testni kalilarini olish uchun
class GetTestKalitlarSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str

# Test javoblarini edit token bilan olish
class GetTestEditTokenSerializer(BaseModel):
    user_id: int
    edit_token: str
    month_date: str
    test_key: str

# GetTestEditTokenSerializer
class SetTestEditTokenSerializer(BaseModel):
    user_id: int
    edit_token: str
    month_date: str
    test_key: str
    kalitlar: str

# User edu name set
class SetEduNameSerializer(BaseModel):
    token: str
    edu_name: str

# User edu bot set
class SetEduBotTokenSerializer(BaseModel):
    token: str
    edu_bot_token: str

# User edu logo set
class SetEduLogoSerializer(BaseModel):
    token: str
    edu_logo: str

# Bot tokinni olish
class GetEduBotTokenSerializer(BaseModel):
    token: str