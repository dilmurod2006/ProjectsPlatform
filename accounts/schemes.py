from pydantic import BaseModel

class TokenRequest(BaseModel):
    tg_id: int
    phone: str

# Create user class
class CreateUser(BaseModel):
    full_name: str
    sex: bool
    email: str
    username: str
    password: str

class CheckUser(BaseModel):
    token: str