from pydantic import BaseModel

class BuySerializer(BaseModel):
    token: str
    months_count: int
class PriceSerializer(BaseModel):
    months_count: int