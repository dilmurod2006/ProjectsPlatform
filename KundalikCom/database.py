from sqlalchemy import Column, create_engine
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

# database path
db_url = "sqlite:///kundalik.db"

# create engine
engine = create_engine(db_url)
Base = declarative_base()

# Table create
class SchoolData(Base):
    __tablename__ = "SchoolData"
    user_id = Column(Integer, primary_key=True)
    viloyat = Column(String)
    tuman = Column(String)
    school_number = Column(String)

class PcKundalikCom(Base):
    __tablename__ = "PcKundalikCom"
    user_id = Column(Integer, primary_key=True)
    token = Column(String)
    start_active_date = Column(DateTime, default=datetime.now)
    end_active_date = Column(DateTime)
    device_id = Column(String)

class LoginsData(Base):
    __tablename__ = "LoginsData"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    login = Column(String)
    password = Column(String)

class MajburiyObuna(Base):
    __tablename__ = "MajburiyObuna"
    id = Column(Integer, primary_key=True)
    device_id = Column(String)


Base.metadata.create_all(engine)

