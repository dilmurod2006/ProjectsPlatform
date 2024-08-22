from pydantic import BaseModel

class TokenRequest(BaseModel):
    secret_key: str
    tg_id: int
    phone: str

# Create user class
class CreateUser(BaseModel):
    token: str
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

# Reset Password
class ChangePassword(BaseModel):
    last_password: str
    new_password: str

# Reset Password
class ResetPasswordRequest(BaseModel):
    username: str

class ResetPassword(BaseModel):
    username: str
    password: str
    reset_code: int

# AboutAccount
class AboutAccount(BaseModel):
    token: str
