from aiogram import Router, F
from aiogram.types import Message
from bot.stats.stats import stats

router = Router()

HELP = (
    "📋 Справка по командам:\n\n"
    "📝 /todo add <текст> - добавить задачу\n"
    "📋 /todo - показать список задач\n"
    "✅ /todo done <id> - отметить выполненной\n\n"
    "🌤️ /weather <город> - погода\n"
    "💱 /rate <BASE> <SYM1,SYM2,...> - курсы валют\n"
    "📁 /fileinfo - информация о файле\n"
    "📊 /stats - статистика бота"
)


@router.message(F.text.startswith("/help"))
async def help_cmd(message: Message) -> None:
    stats.seen_user(message.from_user.id)
    stats.bump("help")
    await message.answer(HELP)


@router.message(F.text.startswith("/"))
async def unknown_command(message: Message) -> None:
    command = (message.text or "").split()[0]
    await message.answer(
        f"❓ Неизвестная команда: {command}\n\n"
        f"Используйте /help для списка доступных команд."
    )
