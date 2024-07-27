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


# Create Login user
class LoginUser(BaseModel):
    username: str
    password: str
