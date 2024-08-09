from pydantic import BaseModel

class BuySerializer(BaseModel):
    token: str
    months_count: int
    