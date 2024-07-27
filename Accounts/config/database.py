from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

DATABASE_URL = "sqlite:///../ACCOUNTS.db"

database = Database(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# SQLAlchemy sessiyasini yaratish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
