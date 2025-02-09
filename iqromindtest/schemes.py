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
    edu_slogan: str
# User edu name get
class GetEduNameSerializer(BaseModel):
    token: str

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

# natija qo'shish uchun
class AddNatijaSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str
    id_raqam: int
    maj: int
    b1: int
    b2: int
    file_id: str
    f1: int
    f2: int
    lang: int

# natija olish uchun
class GetNatijaSerializer(BaseModel):
    user_id: int
    month_date: str
    test_key: str
    id_raqam: int

# All natija
class GetAllNatijalarSerializer(BaseModel):
    user_id: int
    month_date: str
    test_key: str
    page: int

# Search serializer
class SearchOtmSerializer(BaseModel):
    viloyat: str
    text: str

# Get Kirish ballari
class GetKirishballariSerializer(BaseModel):
    viloyat: str
    otm: str
# Natijalarni elon qilish uchun post textini taxrirlash uchun
class SetPostTextSerializer(BaseModel):
    token: str
    month_date: str
    test_key: str
    post_text: str

# Natijalarni elon qilish uchun post textini o'qish uchun
class GetPostTextSerializer(BaseModel):
    user_id: int
    month_date: str
    test_key: str