from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.services.db import db
from bot.repositories.todo_repository import TodoRepository
from bot.stats.stats import stats

router = Router()
PER_PAGE = 10


def todo_pages_keyboard(page: int, total: int, per_page: int) -> InlineKeyboardMarkup:
    last_page = max(0, (total - 1) // per_page)
    prev_page = max(0, page - 1)
    next_page = min(last_page, page + 1)

    kb = InlineKeyboardBuilder()
    kb.row(
        InlineKeyboardButton(text="⬅️", callback_data=f"todo_page:{prev_page}"),
        InlineKeyboardButton(text=f"{page+1}/{last_page+1}", callback_data="noop"),
        InlineKeyboardButton(text="➡️", callback_data=f"todo_page:{next_page}"),
    )
    return kb.as_markup()


def parse_todo_args(text: str):
    parts = text.strip().split(maxsplit=2)
    if len(parts) < 2:
        return None, ""
    return parts[1], (parts[2] if len(parts) == 3 else "")


@router.message(F.text.startswith("/todo"))
async def todo_entry(message: Message) -> None:
    stats.seen_user(message.from_user.id)
    stats.bump("todo")

    sub, arg = parse_todo_args(message.text or "")
    repo = TodoRepository(db.conn)
    user_id = message.from_user.id

    if sub == "add":
        text = arg.strip()
        if not text:
            await message.answer("Укажите текст: /todo add <текст>")
            return
        todo_id = await repo.add(user_id, text)
        await message.answer(f"✅ Добавлено (id={todo_id})")
        return

    if sub == "done":
        if not arg.isdigit():
            await message.answer("Укажите id: /todo done <id>")
            return
        ok = await repo.mark_done(user_id, int(arg))
        await message.answer("Отмечено выполненной" if ok else "Не найдено")
        return

    await send_page(message, 0)


async def send_page(message: Message, page: int) -> None:
    repo = TodoRepository(db.conn)
    user_id = message.from_user.id
    total = await repo.count(user_id)
    offset = page * PER_PAGE
    rows = await repo.list_page(user_id, PER_PAGE, offset)

    if not rows:
        await message.answer("Список пуст. Добавьте: /todo add <текст>")
        return

    lines = [f"{t.id}. [{'x' if t.done else ' '}] {t.text}" for t in rows]
    await message.answer("\n".join(lines), reply_markup=todo_pages_keyboard(page, total, PER_PAGE))


@router.callback_query(F.data.startswith("todo_page:"))
async def todo_page_cb(cb: CallbackQuery) -> None:
    try:
        page = int(cb.data.split(":", 1)[1])
    except Exception:
        await cb.answer()
        return
    await cb.answer()
    await send_page(cb.message, page)
