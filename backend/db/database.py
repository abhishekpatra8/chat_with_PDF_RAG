from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False}, pool_size=20, max_overflow=20)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass


def pdf_db_connect():
    try:
        pdf_db = SessionLocal()
        yield pdf_db
    except:
        pdf_db.close()