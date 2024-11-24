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

from sqlalchemy.dialects.postgresql import JSONB

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
    Column("payment_chek_img", LargeBinary, nullable=True),
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