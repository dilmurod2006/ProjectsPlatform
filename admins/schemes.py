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
    username: str


# Add products class
class AddProducts(BaseModel):
    name: str
    bio: str
    settings: Dict[str, Any]

# Update products class
class UpdateProducts(BaseModel):
    name: str
    bio: str
    settings: Dict[str, Any]

# Delete products class
class DeleteProducts(BaseModel):
    name: str

# AddPayment class
class AddPayment(BaseModel):
    token: str
    tg_id: int
    payment_number: int
    tulov_summasi: int
    bio: str

# CreateProjectsData class
class CreateProjectsData(BaseModel):
    name: str
    email: str
    domen: str
    telegram_channel: str
    youtube_channel: str
    telegram_group: str
    telegram_bot: str
    about: str


# UpdateProjectsData class
class UpdateProjectsData(BaseModel):
    name: str
    email: str
    domen: str
    telegram_channel: str
    youtube_channel: str
    telegram_group: str
    telegram_bot: str
    about: str
