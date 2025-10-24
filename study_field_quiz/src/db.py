import aiosqlite
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "quiz_responses.db"

async def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                username TEXT,
                question TEXT,
                answer TEXT,
                created_at TEXT
            )
            """
        )
        await db.commit()

async def save_response(user_id: int, username: str, question: str, answer: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO responses (user_id, username, question, answer, created_at) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, question, answer, datetime.utcnow().isoformat()),
        )
        await db.commit()