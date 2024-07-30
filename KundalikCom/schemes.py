from pydantic import BaseModel

# Buy post api uchun serializer
class BuySerializer(BaseModel):
    token: str
    months_count: int
