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


class RegisterLoginsSerializer(BaseModel):
    login: str
    parol: str
    capcha_id: str
    capcha_value: str
class SetSchoolSerializer(BaseModel):
    token: str
    viloyat: str
    tuman: str
    school_name: str
# About kundalikpc
class AboutKundalikpcSerializer(BaseModel):
    token: str