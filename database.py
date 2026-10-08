"""
database.py
===========
Handles all SQLite database interactions for COURTFLOW.
Provides functions to:
  - Create tables and seed sample data
  - CRUD operations for cases and case_history

The 'cases' table stores all case details.
The 'case_history' table stores events (linked-list nodes) per case,
with a foreign key back to cases.
"""

import sqlite3
import os
import shutil

# On Vercel / serverless environment, use writable /tmp directory
if os.environ.get("VERCEL"):
    DB_PATH = "/tmp/court_cases.db"
    source_db = os.path.join(os.path.dirname(__file__), "court_cases.db")
    if not os.path.exists(DB_PATH) and os.path.exists(source_db):
        try:
            shutil.copy2(source_db, DB_PATH)
        except Exception:
            pass
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "court_cases.db")


def get_db():
    """Return a new database connection with row_factory for dict-like rows."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # allows row['column_name'] access
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# --------------------------------------------------------------------------
# Schema creation + seed
# --------------------------------------------------------------------------
def init_db():
    """Create tables if they don't exist and seed sample data."""
    conn = get_db()
    c = conn.cursor()

    # --- cases table ---
    c.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            case_id     TEXT PRIMARY KEY,
            plaintiff   TEXT NOT NULL,
            defendant   TEXT NOT NULL,
            case_type   TEXT NOT NULL,
            description TEXT,
            priority    TEXT NOT NULL DEFAULT 'Low',
            filing_date TEXT NOT NULL,
            hearing_date TEXT,
            judge       TEXT,
            lawyer      TEXT,
            status      TEXT NOT NULL DEFAULT 'Pending'
        )
    """)

    # --- case_history table ---
    c.execute("""
        CREATE TABLE IF NOT EXISTS case_history (
            entry_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            case_id     TEXT NOT NULL,
            action      TEXT NOT NULL,
            action_date TEXT NOT NULL,
            note        TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """)

    conn.commit()

    # Seed data only if the table is empty
    count = c.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    if count == 0:
        _seed_data(conn)

    conn.close()


def _seed_data(conn):
    """Insert 8 sample cases and initial history entries."""
    cases = [
        ("C001", "Rahul",   "Kumar",  "Civil",    "Dispute over land boundary in Sector 7",      "High",   "2025-01-10", "2026-02-14", "Justice Mehta",   "Adv. Sharma",  "Pending"),
        ("C002", "Priya",   "Arun",   "Criminal", "Assault and battery case near MG Road",       "High",   "2025-01-15", "2026-02-20", "Justice Verma",   "Adv. Kapoor",  "Pending"),
        ("C003", "Suresh",  "Ravi",   "Property", "Illegal construction dispute in Township",    "Medium", "2025-02-01", "2026-03-05", "Justice Nair",    "Adv. Pillai",  "Pending"),
        ("C004", "Anitha",  "Meena",  "Family",   "Child custody and alimony settlement",        "Low",    "2025-02-10", "2026-03-18", "Justice Reddy",   "Adv. Rao",     "Pending"),
        ("C005", "Karthik", "Sanjay", "Civil",    "Contract breach in supply chain agreement",   "Medium", "2025-03-01", "2026-04-02", "Justice Singh",   "Adv. Iyer",    "Pending"),
        ("C006", "Divya",   "Raj",    "Property", "Property ownership fraud in South Block",     "High",   "2025-03-12", "2026-04-10", "Justice Joshi",   "Adv. Desai",   "Pending"),
        ("C007", "Hari",    "Mohan",  "Family",   "Inheritance dispute after father's demise",   "Low",    "2025-04-05", "2026-05-01", "Justice Kumar",   "Adv. Menon",   "Pending"),
        ("C008", "Arjun",   "Vijay",  "Criminal", "Financial fraud and embezzlement charges",    "Medium", "2025-04-20", "2026-05-15", "Justice Patel",   "Adv. Gupta",   "Pending"),
    ]

    conn.executemany("""
        INSERT INTO cases (case_id, plaintiff, defendant, case_type, description,
                           priority, filing_date, hearing_date, judge, lawyer, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, cases)

    # Seed initial history for each case
    history = [
        ("C001", "Case Filed",     "2025-01-10", "Case C001 registered in the system."),
        ("C001", "Notice Issued",  "2025-01-20", "Notice sent to defendant Kumar."),
        ("C002", "Case Filed",     "2025-01-15", "Case C002 registered in the system."),
        ("C002", "Evidence Submitted", "2025-02-01", "Prosecution submitted FIR and medical reports."),
        ("C003", "Case Filed",     "2025-02-01", "Case C003 registered in the system."),
        ("C004", "Case Filed",     "2025-02-10", "Case C004 registered in the system."),
        ("C004", "Mediation Ordered", "2025-03-01", "Court ordered mediation between parties."),
        ("C005", "Case Filed",     "2025-03-01", "Case C005 registered in the system."),
        ("C006", "Case Filed",     "2025-03-12", "Case C006 registered in the system."),
        ("C006", "FIR Lodged",     "2025-03-15", "FIR lodged with local police station."),
        ("C007", "Case Filed",     "2025-04-05", "Case C007 registered in the system."),
        ("C008", "Case Filed",     "2025-04-20", "Case C008 registered in the system."),
        ("C008", "Chargesheet Filed", "2025-05-01", "Chargesheet submitted by prosecution."),
    ]

    conn.executemany("""
        INSERT INTO case_history (case_id, action, action_date, note)
        VALUES (?, ?, ?, ?)
    """, history)

    conn.commit()


# --------------------------------------------------------------------------
# Case CRUD
# --------------------------------------------------------------------------
def get_all_cases():
    conn = get_db()
    rows = conn.execute("SELECT * FROM cases ORDER BY filing_date").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_case_by_id(case_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM cases WHERE case_id = ?", (case_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def insert_case(data):
    conn = get_db()
    conn.execute("""
        INSERT INTO cases (case_id, plaintiff, defendant, case_type, description,
                           priority, filing_date, hearing_date, judge, lawyer, status)
        VALUES (:case_id, :plaintiff, :defendant, :case_type, :description,
                :priority, :filing_date, :hearing_date, :judge, :lawyer, 'Pending')
    """, data)
    conn.commit()
    conn.close()


def update_case(data):
    conn = get_db()
    conn.execute("""
        UPDATE cases SET
            plaintiff=:plaintiff, defendant=:defendant, case_type=:case_type,
            description=:description, priority=:priority, filing_date=:filing_date,
            hearing_date=:hearing_date, judge=:judge, lawyer=:lawyer, status=:status
        WHERE case_id=:case_id
    """, data)
    conn.commit()
    conn.close()


def delete_case(case_id):
    conn = get_db()
    conn.execute("DELETE FROM cases WHERE case_id = ?", (case_id,))
    conn.commit()
    conn.close()


def mark_completed(case_id):
    conn = get_db()
    conn.execute("UPDATE cases SET status='Completed' WHERE case_id=?", (case_id,))
    conn.commit()
    conn.close()


# --------------------------------------------------------------------------
# Case History CRUD
# --------------------------------------------------------------------------
def get_history(case_id):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM case_history WHERE case_id=? ORDER BY action_date, entry_id",
        (case_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_history():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM case_history ORDER BY case_id, action_date, entry_id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def insert_history(case_id, action, action_date, note=""):
    conn = get_db()
    conn.execute(
        "INSERT INTO case_history (case_id, action, action_date, note) VALUES (?,?,?,?)",
        (case_id, action, action_date, note)
    )
    conn.commit()
    conn.close()


def delete_history_entry(entry_id):
    conn = get_db()
    conn.execute("DELETE FROM case_history WHERE entry_id=?", (entry_id,))
    conn.commit()
    conn.close()


def get_stats():
    """Return dashboard statistics."""
    conn = get_db()
    total    = conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0]
    pending  = conn.execute("SELECT COUNT(*) FROM cases WHERE status='Pending'").fetchone()[0]
    completed= conn.execute("SELECT COUNT(*) FROM cases WHERE status='Completed'").fetchone()[0]
    high     = conn.execute("SELECT COUNT(*) FROM cases WHERE priority='High' AND status='Pending'").fetchone()[0]
    today    = conn.execute(
        "SELECT COUNT(*) FROM cases WHERE hearing_date=date('now') AND status='Pending'"
    ).fetchone()[0]
    conn.close()
    return {
        "total": total, "pending": pending, "completed": completed,
        "high_priority": high, "today_hearings": today
    }
