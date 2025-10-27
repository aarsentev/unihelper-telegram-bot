import aiosqlite
from bot.config.config import settings


class Database:
    def __init__(self):
        self.path = settings.db_path
        self.conn: aiosqlite.Connection | None = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.path)
        self.conn.row_factory = aiosqlite.Row
        await self.conn.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
        """)
        await self.conn.commit()

    async def close(self):
        if self.conn:
            await self.conn.close()
            self.conn = None


db = Database()
