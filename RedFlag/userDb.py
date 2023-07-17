import sqlite3
import os


def initialize_database():
    db_filename = 'users.db'
    if os.path.exists(db_filename):
        os.remove(db_filename)

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    cursor.execute('PRAGMA encoding="UTF-8"')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT not null,
            password TEXT not null,
            email TEXT not null,
            age INTEGER not null,
            name TEXT not null,
            login_attempts INTEGER DEFAULT 0,
            lockout_end_time TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


initialize_database()
