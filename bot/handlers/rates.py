from aiogram import Router, F
from aiogram.types import Message
from bot.services.rates import RatesService
from bot.stats.stats import stats

router = Router()
service = RatesService()


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
    except Exception:
        await message.answer("Ошибка при получении курсов.")
        return

    if not rates:
        await message.answer("Пустой ответ.")
        return

    text = "\n".join([f"{sym}: {rates.get(sym, '—')}" for sym in symbols])
    await message.answer(f"База: {base}\n{text}")
