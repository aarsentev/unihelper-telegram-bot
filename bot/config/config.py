import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    db_path: str = os.getenv("DB_PATH", "todo.sqlite3")


settings = Settings()

if not settings.bot_token:
    raise RuntimeError("BOT_TOKEN is not set. Add it to .env or environment.")
