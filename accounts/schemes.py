from pydantic import BaseModel
from typing import Optional


# Create user
class CreateUser(BaseModel):
    secret_key: str
    full_name: str
    sex : Optional[bool]
    email: str
    username: str
    password: str
    ref: int
# Activation account
class ActivationAccount(BaseModel):
    secret_key: str
    token: str
    tg_id: int
    phone: str


# Login
class LoginUser(BaseModel):
    username: str
    password: str

# cheack login code
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

# ReportsAccount
class GetUserReports(BaseModel):
    token: str
