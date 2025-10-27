from aiogram import Router, F
from aiogram.types import Message
from bot.utils.hashing import sha256_hex
from bot.stats.stats import stats

router = Router()


@router.message(F.document | F.photo | F.video | F.audio | F.voice)
async def fileinfo(message: Message):
    stats.seen_user(message.from_user.id)
    stats.bump("fileinfo")

    file = message.document or getattr(message, "photo", [None])[-1] or message.video or message.audio or message.voice
    if not file:
        await message.answer("Пришлите файл.")
        return

    tg_file = await message.bot.get_file(file.file_id)
    stream = await message.bot.download_file(tg_file.file_path)
    chunks = iter(lambda: stream.read(65536), b"")
    digest = sha256_hex(chunks)
    size = getattr(file, "file_size", 0)
    await message.answer(f"Размер: {size} байт\nSHA-256: {digest}")
