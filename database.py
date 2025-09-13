# database.py
import sqlite3

def init_db():
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    con.commit()
    con.close()
    print("Database initialized.")
if __name__=="__main__":
    init_db()
 