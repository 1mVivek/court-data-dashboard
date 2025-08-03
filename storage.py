# storage.py
import os
import json
import sqlite3
from datetime import datetime

DB_PATH = os.getenv("DB_PATH", "queries.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_type TEXT,
                case_number TEXT,
                filing_year TEXT,
                result_json TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()

def log_query(case_type, case_number, filing_year, result):
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO queries (case_type, case_number, filing_year, result_json, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (
            case_type,
            case_number,
            filing_year,
            json.dumps(result),
            datetime.now().isoformat()
        ))
        conn.commit()

def get_all_queries():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("""
            SELECT case_type, case_number, filing_year, result_json, timestamp
            FROM queries
            ORDER BY id DESC
        """)
        rows = cursor.fetchall()

    # Convert to list of dicts
    queries = []
    for row in rows:
        result_data = json.loads(row[3])
        queries.append({
            "case_type": row[0],
            "case_number": row[1],
            "filing_year": row[2],
            "result": result_data,
            "timestamp": row[4]
        })

    return queries
