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
)

metadata = MetaData()

# ACCOUNTS MODELS START

forregister = Table(
    'forregister',
    metadata,
    Column('id', Integer, primary_key=True, index=True, autoincrement=True),
    Column('tg_id', BigInteger, unique=True, nullable=True),
    Column('phone', String(length=13), unique=True, index=True),
    Column('token', String, unique=True, index=True),
    Column('created_at', DateTime, default=datetime.utcnow),
    Column('expires_at', DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=15))
)

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('full_name', String(25), index=True),
    Column('sex', Boolean),
    Column('email', String, unique=True, index=True),   
    Column('phone', String, unique=True, index=True),
    Column('username', String(length=30), unique=True, index=True),
    Column('password', String(length=260)),
    Column('tg_id', BigInteger, nullable=True, unique=True, index=True),
    Column('balance', BigInteger, default=0),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('last_login', TIMESTAMP, default=datetime.utcnow),
    Column('code', BigInteger, nullable=True),
    Column('reset_code', BigInteger, nullable=True),
    Column('how_online', Boolean, default=False),
    Column('token', String(length=700), unique=True, index=True)
)

# reportsbalance model for users
reportsbalance = Table(
    'reportsbalance',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('balance', Integer, default=0),
    Column('size', Integer),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('bio', String, nullable=True)
)

# Products model for users
products = Table(
    'products',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('name', String, index=True),
    Column('bio', Text, nullable=True),
    Column('price', Integer)
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
    Column('school_number', String),
)

# pckundalikcom model
pckundalikcom = Table(
    'pckundalikcom',
    metadata,
    Column('id', Integer, primary_key=True, index=True,autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id'), index=True),
    Column('token', String),
    Column('start_active_date', TIMESTAMP),
    Column('end_active_date', TIMESTAMP),
    Column('device_id', String),
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
    Column('device_id', String),
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
    Column('id', Integer, primary_key=True, index=True),
    Column('username', String),
    Column('password', String),
    Column('tg_id', BigInteger, unique=True, index=True),
    Column('active', Boolean),
    Column('created_at', TIMESTAMP, default=datetime.utcnow),
    Column('updated_at', TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow),
    Column('token', String),
)
