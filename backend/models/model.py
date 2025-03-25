from sqlalchemy import Column, Integer, String, DateTime
from db.database import Base
from pydantic import BaseModel


class Insert_PDF_Record(Base):
    __tablename__ = "pdfs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, default=None)
    embedding_id = Column(String, default=None)
    uploaded_on = Column(DateTime, default=None)


class Model_Resp(BaseModel):
    id: int
    filename: str
    embedding_id: str
    uploaded_on: str