from aiogram import Router, F
from aiogram.types import Message
from bot.stats.stats import stats

router = Router()

HELP = (
    "Справка по командам:\n"
    "/todo add <текст>\n"
    "/todo list\n"
    "/todo done <id>\n"
    "/weather <город>\n"
    "/rate <BASE> <SYM1,SYM2,...>\n"
    "/fileinfo\n"
    "/stats"
)


@router.message(F.text.startswith("/help"))
async def help_cmd(message: Message) -> None:
    stats.seen_user(message.from_user.id)
    stats.bump("help")
    await message.answer(HELP)
