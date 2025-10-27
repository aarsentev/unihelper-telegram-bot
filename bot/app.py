import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from bot.config.config import settings
from bot.config.logging_config import setup_logging
from bot.services.db import db
from bot.handlers import start, help, todo, weather, rates, file_info, stats
from bot.handlers.weather import service as weather_service


async def main():
    setup_logging()
    logging.info("Bot starting...")

    await db.connect()
    await weather_service.start()

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(todo.router)
    dp.include_router(weather.router)
    dp.include_router(rates.router)
    dp.include_router(file_info.router)
    dp.include_router(stats.router)
    dp.include_router(help.router)

    try:
        await dp.start_polling(bot)
    finally:
        await db.close()
        await weather_service.close()


if __name__ == "__main__":
    asyncio.run(main())
