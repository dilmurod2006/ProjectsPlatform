# create schemes
from pydantic import BaseModel
from typing import Dict, Any


# Create admin class
class CreateAdmin(BaseModel):
    username: str
    password: str
    tg_id: int
    premessions: Dict[str, Any]

# Update admin class
class UpdateAdmin(BaseModel):
    username: str
    password: str
    tg_id: int
    premessions: Dict[str, Any]


# Delete admin class
class DeleteAdmin(BaseModel):
    username: str