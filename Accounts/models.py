from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from database import Base

class ForRegister(Base):
    __tablename__ = 'forregister'
    
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, nullable=True)
    phone = Column(String, unique=True, index=True)
    token = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=15))

class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    sex = Column(Boolean, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, ForeignKey('forregister.phone'), unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    tg_id = Column(Integer, ForeignKey('forregister.tg_id'), nullable=True)
    balance = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    code = Column(String, nullable=True)
    how_online = Column(Boolean, default=False)

class ReportsBalance(Base):
    __tablename__ = 'reportsbalance'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    size = Column(Integer)
    date = Column(DateTime, default=datetime.utcnow)
    bio = Column(String, nullable=True)