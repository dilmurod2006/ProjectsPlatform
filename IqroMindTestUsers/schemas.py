from pydantic import BaseModel

class AbuturentUsers(BaseModel):
    first_name: str
    tg_id: int

class TestSchema(BaseModel):
    titul_id: str
    qiymat: str
    sana: str

