# create schemes
from pydantic import BaseModel
from typing import Dict, Any
from fastapi import UploadFile


# Login admin class
class LoginAdmin(BaseModel):
    username: str
    password: str

# check login admin class
class CheckLoginAdmin(BaseModel):
    username: str
    password: str
    code: int

class ResetPasswordRequest(BaseModel):
    username: str

class ResetPassword(BaseModel):
    username: str
    password: str
    reset_code: int

# Create admin class
class CreateAdmin(BaseModel):
    admin_token: str
    full_name: str
    phone: str
    email: str
    username: str
    password: str
    sex: bool
    tg_id: int
    premessions: Dict[str, Any]

# Update admin class
class UpdateAdmin(BaseModel):
    admin_token: str
    full_name: str
    phone: str
    email: str
    username: str
    password: str
    tg_id: int
    active: bool
    premessions: Dict[str, Any]


# Delete admin class
class DeleteAdmin(BaseModel):
    admin_token: str
    username: str


# Add products class
class AddProducts(BaseModel):
    admin_token: str
    name: str
    bio: str
    settings: Dict[str, Any]

# Update products class
class UpdateProducts(BaseModel):
    admin_token: str
    name: str
    bio: str
    settings: Dict[str, Any]

# Delete products class
class DeleteProducts(BaseModel):
    admin_token: str
    name: str

# AddPayment class
class AddPayment(BaseModel):
    admin_token: str
    token: str
    tg_id: int
    payment_number: int
    tulov_summasi: int
    bio: str

