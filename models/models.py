from datetime import datetime, timedelta
from sqlalchemy import (
    Table,
    Column, 
    Integer,
    BigInteger, 
    String, 
    Text,
    Boolean, 
    ForeignKey, 
    MetaData,
    TIMESTAMP,
    DateTime,
    LargeBinary
)
import random
import string
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import BaseModel, Field
from typing import List, Optional




def generate_token(length=8):
    # Token uchun raqamlar, harflar va maxsus belgilarni tanlash
    characters = string.ascii_letters + string.digits  # harflar va raqamlar
    token = ''.join(random.choice(characters) for _ in range(length))
    return token







metadata = MetaData()

# ACCOUNTS MODELS START

users = Table(
    'users',
    metadata,
    Column('id', BigInteger, primary_key=True, index=True,autoincrement=True),
    Column('full_name', String(25), index=True),
    Column('sex', Boolean),
    Column('email', String, unique=True, index=True),   
    Column('phone', String, unique=True, index=True),
    Column('username', String(length=30), unique=True, index=True),
    Column('password', String(length=260)),
    Column('tg_id', BigInteger, nullable=True, unique=True, index=True),
    Column('balance', BigInteger, default=0),
    Column('ref_id', BigInteger),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('last_login', TIMESTAMP, default=datetime.utcnow),
    Column('code', BigInteger, nullable=True),
    Column('reset_code', BigInteger, nullable=True),
    Column('how_online', Boolean, default=False),
    Column('is_active', Boolean, default=False),
    Column('activation_token', String(length=700), nullable=True, unique=True, index=True),
    Column('token', String(length=700), unique=True, index=True)
)


# Payment model for admin
payment_admin = Table(
    'payment',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column("admin_id", Integer, ForeignKey('admins.id'), index=True),
    Column("user_id", Integer, ForeignKey('users.id'), index=True),
    Column("tulov_summasi", BigInteger),
    Column("payment_chek_img", String(length=700), nullable=True),
    Column("bio", Text, nullable=True),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
)

# reportsbalance model for users
reportsbalance = Table(
    'reportsbalance',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('payment_number', BigInteger, index=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('balance', BigInteger),
    Column('tulov_summasi', BigInteger),
    Column('bio', String, nullable=True),
    Column('created_at', TIMESTAMP, default=datetime.utcnow)
)

# Products model for users
products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('name', String, index=True),
    Column('bio', Text, nullable=True),
    Column('logo', LargeBinary, nullable=True),
    Column('settings', JSONB, nullable=True),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
)


# ACCOUNTS MODELS END

# KUNDALIKCOM MODELS START

# school data model
school_data = Table(
    'school_data',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('viloyat', String),
    Column('tuman', String),
    Column('school_name', String)
)

# pckundalikcom model
pckundalikcom = Table(
    'pckundalikcom',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('start_active_date', TIMESTAMP),
    Column('end_active_date', TIMESTAMP),
    Column('device_id', String, nullable=True),
    Column('end_use_date', TIMESTAMP),
)

# mobilekundalikcom model
mobilekundalikcom = Table(
    'mobilekundalikcom',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('start_active_date', TIMESTAMP),
    Column('end_active_date', TIMESTAMP),
    Column('device_id', String, nullable=True),
    Column('end_use_date', TIMESTAMP),
)

# LOGINSDATA MODEL
loginsdata = Table(
    'loginsdata',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('login', String),
    Column('password', String),
)

# MajburiyObuna model
majburiyobuna = Table(
    'majburiyobuna',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('device_id', String),
)

# KUNDALIKCOM MODELS END

# IQRO MIND TEST MODELS START

# iqromindtest model
iqromindtest = Table(
    'iqromindtest',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('device_id', String, nullable=True),
    Column('testlar', JSONB, default={}),
    Column('edit_token', String, default=generate_token),
    Column('edu_name', String, nullable=True),
    Column('edu_logo', String, nullable=True),
    Column('edu_slogan', String, nullable=True),
    Column('edu_bot_token', String, nullable=True),
    Column('end_premium_date', TIMESTAMP),
    Column('end_use_date', TIMESTAMP),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
)

# Kirish ballari model
kirishballari = Table(
    'kirishballari',
    metadata,
    Column('viloyat', String),
    Column('otm', String, unique=True),
    Column('yil', String),
    Column('data', JSONB)
)

# IQRO MIND TEST MODELS END


# ADMIN PANEL MODELS START

# admins model
admins = Table(
    'admins',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('full_name', String(25), index=True),
    Column('phone', String, unique=True, index=True),
    Column('email', String, unique=True, index=True),
    Column('username', String),
    Column('password', String),
    Column('sex', Boolean, default=True),
    Column('tg_id', BigInteger, unique=True, index=True),
    Column('is_active', Boolean, default=True),
    Column('premessions', JSONB, nullable=True, index=True),
    Column('token', String(length=700), unique=True, index=True),
    Column("code", BigInteger, nullable=True),
    Column("reset_code", BigInteger, nullable=True),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP),
)

# ADMIN PANEL MODELS END


# IQROMINDTESTUSERS MODELS START

#  Create User model
class User(BaseModel):
    first_name: str = Field(..., max_length=50)
    tg_id: int = Field(..., max_length=13)

# Test ma'lumotlari uchun model
class Test(BaseModel):
    user_id: str
    titul_id: str = Field(..., max_length=4)
    qiymat: Optional[List[str]]
    sana: str = Field(..., max_length=10)
