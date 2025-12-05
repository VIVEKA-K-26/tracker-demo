import sqlite3
from pathlib import Path

DB_NAME = "expenses.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    created = not Path(DB_NAME).exists()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT
    )
    """)
    conn.commit()
    conn.close()
    return created

def add_expense(date, amount, category, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO expenses(date, amount, category, description) VALUES (?, ?, ?, ?)",
                (date, amount, category, description))
    conn.commit()
    conn.close()

def update_expense(expense_id, date, amount, category, description):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE expenses
        SET date=?, amount=?, category=?, description=?
        WHERE id=?
    """, (date, amount, category, description, expense_id))
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
    conn.commit()
    conn.close()

def get_all_expenses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    return rows

def filter_by_category(category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE category=? ORDER BY id ASC", (category,))
    rows = cur.fetchall()
    conn.close()
    return rows

def filter_by_date(start, end):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC", (start, end))
    rows = cur.fetchall()
    conn.close()
    return rows

def count_rows():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM expenses")
    n = cur.fetchone()[0]
    conn.close()
    return n
