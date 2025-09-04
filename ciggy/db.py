import aiohttp
import sqlite3
from ciggy.config import DATABASE
from contextlib import asynccontextmanager


conn = sqlite3.connect(DATABASE)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        url TEXT PRIMARY KEY,
        status INTEGER
    )
""")
conn.commit()


@asynccontextmanager
async def async_session_context():
    async with aiohttp.ClientSession() as session:
        yield session
