from aiogram import Router, F
from aiogram.types import Message
from bot.services.rates import RatesService
from bot.stats.stats import stats
import random

router = Router()
service = RatesService()


def get_currency_emoji(currency: str) -> str:
    specific = {
        "USD": "💵",
        "EUR": "💶", 
        "GBP": "💷",
        "CAD": "🇨🇦",
    }
    if currency in specific:
        return specific[currency]
    
    return random.choice(["💰", "💸", "💴"])


@router.message(F.text.startswith("/rate"))
async def rate(message: Message):
    stats.seen_user(message.from_user.id)
    stats.bump("rate")

    parts = (message.text or "").split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Формат: /rate <BASE> <SYM1,SYM2,...>")
        return

    base = parts[1].upper()
    symbols = [s.strip().upper() for s in parts[2].split(",") if s.strip()]

    try:
        rates = await service.get_rates(base, symbols)
    except Exception as e:
        await message.answer(f"Ошибка при получении курсов: {e}")
        return

    if not rates:
        await message.answer(f"Курсы не найдены. Проверьте код валюты '{base}'.")
        return

    base_emoji = get_currency_emoji(base)
    lines = [f"{get_currency_emoji(sym)} {sym}: {rates.get(sym, '—')}" for sym in symbols]
    text = "\n".join(lines)
    await message.answer(f"{base_emoji} База: {base}\n\n{text}")
