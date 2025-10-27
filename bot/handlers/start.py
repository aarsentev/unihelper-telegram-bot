from aiogram import Router, F
from aiogram.types import Message
from bot.stats.stats import stats

router = Router()

TEXT = (
    "👋 Добро пожаловать в UniHelper!\n\n"
    "Что умеет:\n\n"
    "📝 Управление задачами (TODO)\n"
    "🌤️ Прогноз погоды\n"
    "💱 Курсы валют\n"
    "📁 Информация о файлах\n"
    "📊 Статистика использования\n\n"
    "Используйте /help для полного списка команд"
)


@router.message(F.text.startswith("/start"))
async def start_cmd(message: Message) -> None:
    stats.seen_user(message.from_user.id)
    stats.bump("start")
    await message.answer(TEXT)
