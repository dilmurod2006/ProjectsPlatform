from sqlalchemy import Column, create_engine
from sqlalchemy import Integer, String, DateTime, JSON
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# database path
db_url = "sqlite:///admin.db"

# create engine
engine = create_engine(db_url)
Base = declarative_base()

# Table create
class Admins(Base):
    __tablename__ = "SchoolData"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    tg_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    token = Column(String)
    

class Products(Base):
    __tablename__ = "PcKundalikCom"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    about = Column(String)
    settings = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()
