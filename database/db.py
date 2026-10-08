import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "expense_tracker.db")

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL NOT NULL,
            category    TEXT NOT NULL,
            date        TEXT NOT NULL,
            description TEXT,
            created_at  TEXT DEFAULT (datetime('now'))
        );
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", generate_password_hash("demo123")),
    )
    user_id = cursor.lastrowid

    month = date.today().strftime("%Y-%m")
    expenses = [
        (250.0, "Food", 2, "Groceries"),
        (120.0, "Transport", 4, "Metro card recharge"),
        (1800.0, "Bills", 5, "Electricity bill"),
        (450.0, "Health", 9, "Pharmacy"),
        (399.0, "Entertainment", 12, "Movie tickets"),
        (1299.0, "Shopping", 15, "New shoes"),
        (180.0, "Food", 18, "Lunch with friends"),
        (75.0, "Other", 22, None),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)",
        [(user_id, amount, category, f"{month}-{day:02d}", desc) for amount, category, day, desc in expenses],
    )
    conn.commit()
    conn.close()
