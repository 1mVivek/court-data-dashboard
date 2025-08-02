import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "court_queries.db")

def init_db():
    """Initialize SQLite database with required table if not exists."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                filing_year TEXT,
                query_time TEXT,
                parties TEXT,
                filing_date TEXT,
                next_hearing TEXT,
                pdf_url TEXT
            )
        """)
        conn.commit()

def log_query(case_type, case_number, filing_year, result):
    """Log the case search and its result into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO queries (
                case_type, case_number, filing_year, query_time,
                parties, filing_date, next_hearing, pdf_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            case_type,
            case_number,
            filing_year,
            datetime.utcnow().isoformat(),
            result.get("parties", "N/A"),
            result.get("filing_date", "N/A"),
            result.get("next_hearing", "N/A"),
            result.get("pdf_url")
        ))
        conn.commit()

# Call this once on app start
init_db()
