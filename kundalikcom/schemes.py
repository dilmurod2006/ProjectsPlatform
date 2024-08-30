
from pydantic import BaseModel

class BuySerializer(BaseModel):
    token: str
    months_count: int
class PriceSerializer(BaseModel):
    months_count: int
class CheckPcSerializer(BaseModel):
    device_id: str
    token: str
class RegisterLoginsSerializer(BaseModel):
    login: str
    password: str
class SetSchoolSerializer(BaseModel):
    token: str
    viloyat: str
    tuman: str
    school_name: str
class GetSchoolSerializer(BaseModel):
    token: str
