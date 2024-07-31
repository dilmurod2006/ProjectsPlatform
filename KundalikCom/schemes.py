from pydantic import BaseModel

# Buy post api uchun serializer
class Buy(BaseModel):
    token: str
    months_count: int
# Kundalik Com oylik obuna narxi
class PriceMonths(BaseModel):
    months_count: int