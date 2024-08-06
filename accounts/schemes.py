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

<<<<<<< HEAD
# Check user
class CheckUser(BaseModel):
    token: str
=======
# Login user class
class LoginUser(BaseModel):
    username: str
    password: str

# Check Login data and code class
class CheckLogin(BaseModel):
    username: str
    password: str
    code: int
>>>>>>> 78a12182d4fcea9fab5257eac5df6728010108c6

