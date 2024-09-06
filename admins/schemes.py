# create schemes
from pydantic import BaseModel
from typing import Dict, Any, Optional
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
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
    admin_token: str
>>>>>>> dilmurod006
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
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
    admin_token: str
>>>>>>> dilmurod006
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
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
    admin_token: str
>>>>>>> dilmurod006
    username: str


# Add products class
class AddProducts(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
    admin_token: str
>>>>>>> dilmurod006
    name: str
    bio: str
    settings: Dict[str, Any]

# Update products class
class UpdateProducts(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
    admin_token: str
>>>>>>> dilmurod006
    name: str
    bio: str
    settings: Dict[str, Any]

# Delete products class
class DeleteProducts(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
    admin_token: str
>>>>>>> dilmurod006
    name: str

# AddPayment class
class AddPayment(BaseModel):
<<<<<<< HEAD
<<<<<<< HEAD
    admin_token: str
=======
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
    token: str
=======
    admin_token: str
>>>>>>> dilmurod006
    tg_id: int
    tulov_summasi: int
    payment_chek_img: Optional[bytes] = None
    bio: Optional[str] = None

<<<<<<< HEAD
<<<<<<< HEAD
=======
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
>>>>>>> 340a437b1ce802d8b37f0b8f3be24dddc7446c85
=======
# Get Data class
class GetData(BaseModel):
    admin_token: str
>>>>>>> dilmurod006
