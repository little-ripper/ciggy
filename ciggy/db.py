import sqlite3
from ciggy.config import DATABASE


conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        url TEXT PRIMARY KEY,
        status INTEGER
    )
""")
conn.commit()
