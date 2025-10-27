from aiogram import Router, F
from aiogram.types import Message
from bot.stats import stats

router = Router()

TEXT = (
    "Добро пожаловать в УниПомощник.\n"
    "Команды:\n"
    "/todo add <текст>\n"
    "/todo list\n"
    "/todo done <id>\n"
    "/weather <город>\n"
    "/rate <BASE> <SYM1,SYM2,...>\n"
    "/fileinfo\n"
    "/stats\n"
    "/help"
)


@router.message(F.text.startswith("/start"))
async def start_cmd(message: Message) -> None:
    stats.seen_user(message.from_user.id)
    stats.bump("start")
    await message.answer(TEXT)
