# storage.py
import os
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///local.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class QueryLog(Base):
    __tablename__ = "query_log"
    id = Column(Integer, primary_key=True)
    case_type = Column(String(50))
    case_number = Column(String(50))
    filing_year = Column(String(10))
    result = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

def log_query(case_type, case_number, filing_year, result):
    session = SessionLocal()
    entry = QueryLog(
        case_type=case_type,
        case_number=case_number,
        filing_year=filing_year,
        result=str(result)
    )
    session.add(entry)
    session.commit()
    session.close()

def get_all_queries():
    session = SessionLocal()
    queries = session.query(QueryLog).order_by(QueryLog.timestamp.desc()).all()
    session.close()
    return queries
