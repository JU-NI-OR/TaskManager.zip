import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def connect():
    return sqlite3.connect('database.db')

def init_db():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                            content TEXT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(id))''')
        conn.commit()

def register_user(username, email, password):
    try:
        with connect() as conn:
            cursor = conn.cursor()
            hashed_pw = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (username, email, hashed_pw))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def validate_login(username, password):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            return {"id": user[0], "username": user[1]}
        return None

def get_tasks_by_user(user_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, content FROM tasks WHERE user_id = ?", (user_id,))
        return cursor.fetchall()

def add_task(user_id, task):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (user_id, content) VALUES (?, ?)", (user_id, task))
        conn.commit()

def delete_task(user_id, task_id):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        conn.commit()

def edit_task(user_id, task_id, new_content):
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET content = ? WHERE id = ? AND user_id = ?",
                       (new_content, task_id, user_id))
        conn.commit()
