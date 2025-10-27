from aiogram import Router, F
from aiogram.types import Message
from bot.services.weather import WeatherService
from bot.stats import stats

router = Router()
service = WeatherService()


@router.message(F.text.startswith("/weather"))
async def weather(message: Message):
    stats.seen_user(message.from_user.id)
    stats.bump("weather")

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Формат: /weather <город>")
        return
    city = parts[1].strip()

    try:
        wx = await service.by_city(city)
    except Exception:
        await message.answer("Ошибка при получении погоды.")
        return

    feels = f" (ощущается {wx['feels']}°C)" if wx.get("feels") else ""
    wind = f"\nВетер: {wx.get('wind')} км/ч" if wx.get("wind") else ""
    await message.answer(f"{wx['place']}\nТемпература: {wx['temp']}°C{feels}{wind}")
