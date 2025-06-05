import sqlite3
from typing import Any, List, Tuple, Optional
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'smartpath.db')

# --- Table Schemas ---
SCHEMA = {
    'users': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''',
    'assessments': '''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            skill_level TEXT,
            domain TEXT,
            responses TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''',
    'learning_paths': '''
        CREATE TABLE IF NOT EXISTS learning_paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            milestones TEXT,
            timeline TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''',
    'resources': '''
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path_id INTEGER,
            title TEXT,
            url TEXT,
            type TEXT,
            difficulty TEXT,
            FOREIGN KEY(path_id) REFERENCES learning_paths(id)
        )''',
    'progress': '''
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            completed_items TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )''',
    'notes': '''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            learning_path_id INTEGER,
            milestone_title TEXT,
            note_text TEXT,
            UNIQUE(user_id, learning_path_id, milestone_title),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(learning_path_id) REFERENCES learning_paths(id)
        )''',
}

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = get_connection()
    c = conn.cursor()
    for table, ddl in SCHEMA.items():
        c.execute(ddl)
    conn.commit()
    conn.close()

# --- Basic CRUD Examples ---
def add_user(name: str, email: str) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return user_id

def get_user_by_email(email: str) -> Optional[Tuple]:
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def add_assessment(user_id: int, skill_level: str, domain: str, responses: str) -> int:
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO assessments (user_id, skill_level, domain, responses) VALUES (?, ?, ?, ?)",
              (user_id, skill_level, domain, responses))
    conn.commit()
    assessment_id = c.lastrowid
    conn.close()
    return assessment_id

# Add more CRUD functions as needed for other tables

def get_learning_paths_by_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, milestones, timeline FROM learning_paths WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            'id': row[0],
            'title': row[1],
            'milestones': row[2],
            'timeline': row[3]
        } for row in rows
    ]

def get_progress_by_user(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT completed_items, last_updated FROM progress WHERE user_id = ? ORDER BY last_updated DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [
        {
            'completed_items': json.loads(row[0]),
            'last_updated': row[1]
        } for row in rows
    ]

def save_note(user_id: int, learning_path_id: int, milestone_title: str, note_text: str):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO notes (user_id, learning_path_id, milestone_title, note_text)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(user_id, learning_path_id, milestone_title) DO UPDATE SET note_text=excluded.note_text
    """, (user_id, learning_path_id, milestone_title, note_text))
    conn.commit()
    conn.close()

def get_note(user_id: int, learning_path_id: int, milestone_title: str) -> str:
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT note_text FROM notes WHERE user_id = ? AND learning_path_id = ? AND milestone_title = ?
    """, (user_id, learning_path_id, milestone_title))
    row = c.fetchone()
    conn.close()
    return row[0] if row else ""

if __name__ == "__main__":
    create_tables()
    print("[DB] Tables created successfully.") 