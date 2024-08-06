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

# Login user class
class LoginUser(BaseModel):
    username: str
    password: str

# Check Login data and code class
class CheckLogin(BaseModel):
    username: str
    password: str
    code: int

