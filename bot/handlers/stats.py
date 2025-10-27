import os
from aiogram import Router, F
from aiogram.types import Message

from bot.stats.stats import stats
from bot.services.db import db
from bot.utils.time_formatter import time_formatter

router = Router()


@router.message(F.text.startswith("/stats"))
async def cmd_stats(message: Message) -> None:
    stats.seen_user(message.from_user.id)
    stats.bump("stats")

    try:
        db_size_kb = os.path.getsize(db.path) // 1024
    except Exception:
        db_size_kb = 0

    # commands breakdown
    commands_text = "\n".join(
        f"  /{cmd}: {count}" for cmd, count in stats.commands.most_common()
    ) or "  —"

    text = (
        "Статистика бота\n"
        f"Аптайм: {time_formatter(stats.uptime_seconds)}\n"
        f"Уникальных пользователей: {len(stats.user_ids)}\n"
        "Команды:\n"
        f"{commands_text}\n"
        f"Размер БД: {db_size_kb} КБ"
    )

    await message.answer(text)
