from datetime import datetime, timezone
from bot.models.todo import Todo
import aiosqlite


class TodoRepository:
    def __init__(self, conn: aiosqlite.Connection):
        self.conn = conn

    async def add(self, user_id: int, text: str) -> int:
        now = datetime.now(timezone.utc).isoformat()
        cur = await self.conn.execute(
            "INSERT INTO todo (user_id, text, created_at) VALUES (?, ?, ?)",
            (user_id, text, now),
        )
        await self.conn.commit()
        return cur.lastrowid

    async def list_page(self, user_id: int, limit: int, offset: int):
        cur = await self.conn.execute(
            "SELECT * FROM todo WHERE user_id=? ORDER BY id DESC LIMIT ? OFFSET ?",
            (user_id, limit, offset),
        )
        rows = await cur.fetchall()
        return [Todo.from_row(r) for r in rows]

    async def count(self, user_id: int):
        cur = await self.conn.execute("SELECT COUNT(*) FROM todo WHERE user_id=?", (user_id,))
        (n,) = await cur.fetchone()
        return int(n)

    async def mark_done(self, user_id: int, todo_id: int):
        cur = await self.conn.execute(
            "UPDATE todo SET done=1 WHERE id=? AND user_id=?", (todo_id, user_id)
        )
        await self.conn.commit()
        return cur.rowcount > 0
