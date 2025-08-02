import sqlite3
import os
from datetime import datetime

# Path to SQLite DB, default is court_queries.db if not set in environment
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

def get_all_queries():
    """Fetch all logged queries from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM queries ORDER BY query_time DESC")
        rows = cursor.fetchall()
    return rows

# Initialize the database on module load
init_db()