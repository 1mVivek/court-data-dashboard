import os
import json
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
load_dotenv()

# Set up PostgreSQL connection
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///queries.db")  # fallback to SQLite for local/dev

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class CaseQuery(Base):
    __tablename__ = "case_queries"

    id = Column(Integer, primary_key=True)
    case_type = Column(String)
    case_number = Column(String)
    filing_year = Column(String)
    result = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create tables if not exist
Base.metadata.create_all(engine)

def log_query(case_type, case_number, filing_year, result):
    """Log a query to the database."""
    session = Session()
    try:
        new_query = CaseQuery(
            case_type=case_type,
            case_number=case_number,
            filing_year=filing_year,
            result=result
        )
        session.add(new_query)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_all_queries():
    """Retrieve all logged queries, sorted by newest first."""
    session = Session()
    try:
        queries = session.query(CaseQuery).order_by(CaseQuery.timestamp.desc()).all()
        return [
            {
                "case_type": q.case_type,
                "case_number": q.case_number,
                "filing_year": q.filing_year,
                "result": q.result,
                "timestamp": q.timestamp.isoformat()
            }
            for q in queries
        ]
    finally:
        session.close()
