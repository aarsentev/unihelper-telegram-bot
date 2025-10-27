from aiogram import Router, F
from aiogram.types import Message
from bot.services.weather import WeatherService
from bot.stats.stats import stats

router = Router()
service = WeatherService()


def get_weather_emoji(kind: str | None, temp: int) -> str:
    if not kind:
        return "🌡️"
    
    kind_lower = kind.lower()
    if "clear" in kind_lower or "sunny" in kind_lower:
        return "☀️"
    elif "partly cloudy" in kind_lower:
        return "⛅"
    elif "cloudy" in kind_lower or "overcast" in kind_lower:
        return "☁️"
    elif "rain" in kind_lower or "drizzle" in kind_lower:
        return "🌧️"
    elif "snow" in kind_lower:
        return "❄️"
    elif "thunder" in kind_lower or "storm" in kind_lower:
        return "⛈️"
    elif "fog" in kind_lower or "mist" in kind_lower:
        return "🌫️"
    else:
        return "🌡️"


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
    except Exception as e:
        await message.answer(f"Ошибка при получении погоды: {e}")
        return

    emoji = get_weather_emoji(wx.get("kind"), wx.get("temperature", 0))

    location_parts = [wx["location"]]
    if wx.get("region") and wx["region"] != wx["location"]:
        location_parts.append(wx["region"])
    if wx.get("country"):
        location_parts.append(wx["country"])
    
    header = f"{emoji} {', '.join(location_parts)}"

    temp = wx["temperature"]
    feels = wx.get("feels_like")
    feels_text = f" (ощущается как {feels}°C)" if feels is not None else ""
    
    description = wx.get("description", "")
    
    temp_section = f"🌡️ {temp}°C{feels_text}"
    if description:
        temp_section += f"\n💭 {description}"

    conditions = []
    
    if wx.get("humidity") is not None:
        conditions.append(f"💧 Влажность: {wx['humidity']}%")
    
    if wx.get("wind_speed") is not None:
        conditions.append(f"💨 Ветер: {wx['wind_speed']} м/с")
    
    if wx.get("visibility") is not None:
        conditions.append(f"👁️ Видимость: {wx['visibility']} км")
    
    if wx.get("pressure") is not None:
        conditions.append(f"🔽 Давление: {wx['pressure']:.0f} мбар")
    
    if wx.get("precipitation") is not None and wx["precipitation"] > 0:
        conditions.append(f"🌧️ Осадки: {wx['precipitation']} мм")

    response_parts = [header, temp_section]
    if conditions:
        response_parts.append("\n" + "\n".join(conditions))
    
    await message.answer("\n".join(response_parts))
