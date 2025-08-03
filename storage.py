import sqlite3
from datetime import datetime

DB_FILE = "case_queries.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_number TEXT,
            filing_year TEXT,
            parties TEXT,
            filing_date TEXT,
            next_hearing TEXT,
            pdf_url TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_query(case_type, case_number, filing_year, result):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO queries (
            case_type, case_number, filing_year,
            parties, filing_date, next_hearing, pdf_url,
            timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        case_type, case_number, filing_year,
        result.get("parties", "N/A"),
        result.get("filing_date", "N/A"),
        result.get("next_hearing", "N/A"),
        result.get("pdf_url"),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_all_queries():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM queries ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows
